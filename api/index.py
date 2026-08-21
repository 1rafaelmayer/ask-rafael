"""HTTP surface: one streaming chat endpoint, plus the page itself in local dev.

Everything here is stateless. The browser owns the conversation and sends it
back on every request; this module's only jobs are to refuse what it should not
serve and to turn the graph's output into a stream the page can render as it
arrives.
"""

from __future__ import annotations

import asyncio
import json
import os
import time
from collections import defaultdict, deque
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel, Field

from .agent import build_graph

ROOT = Path(__file__).resolve().parent.parent

# Twenty questions is a long conversation for a CV page and a natural place to
# stop paying for one visitor. Tool traffic is dropped from the history before
# it is counted, so reading six documents does not cost anybody a question.
MAX_USER_MESSAGES = 20
MAX_QUESTION_CHARS = 500
MAX_HISTORY_MESSAGES = MAX_USER_MESSAGES * 2

# Ceiling on agent turns, so a model that keeps calling the tool cannot bill an
# unbounded loop. Two documents plus a final answer fits comfortably.
RECURSION_LIMIT = 12

# Best-effort, per instance: serverless gives every cold start a fresh dict, so
# this thins abuse rather than stopping it. The hard stop is the spend cap on
# the OpenAI account, which is the only limit that cannot be routed around.
RATE_WINDOW_SECONDS = 60 * 10
RATE_LIMIT_PER_IP = 25
RATE_LIMIT_GLOBAL = 400

_hits: dict[str, deque[float]] = defaultdict(deque)
_global: deque[float] = deque()

app = FastAPI(title="ask-rafael", docs_url=None, redoc_url=None)

# Built lazily: an import-time failure on Vercel surfaces as an opaque 500,
# while a first-request failure can be reported as itself.
_graph = None
_graph_lock = asyncio.Lock()


async def graph():
    global _graph
    if _graph is None:
        async with _graph_lock:
            if _graph is None:
                _graph = build_graph()
    return _graph


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[Message] = Field(default_factory=list)


def _client_ip(request: Request) -> str:
    # Vercel terminates TLS upstream, so the socket peer is always the proxy.
    forwarded = request.headers.get("x-forwarded-for", "")
    return forwarded.split(",")[0].strip() or (request.client.host if request.client else "unknown")


def _prune(bucket: deque[float], now: float) -> None:
    while bucket and now - bucket[0] > RATE_WINDOW_SECONDS:
        bucket.popleft()


def _rate_limited(ip: str) -> str | None:
    now = time.monotonic()

    _prune(_global, now)
    if len(_global) >= RATE_LIMIT_GLOBAL:
        return "This page is getting more traffic than it can answer right now. Please try again later."

    bucket = _hits[ip]
    _prune(bucket, now)
    if len(bucket) >= RATE_LIMIT_PER_IP:
        return (
            "You have reached the question limit for now. To keep talking, "
            "reach Rafael directly: https://www.linkedin.com/in/rafael-alves-mayer/"
        )

    bucket.append(now)
    _global.append(now)
    return None


def _count_questions(messages: list[Message]) -> int:
    """How many questions the client claims to have asked.

    Counted on the raw payload, before any trimming. Counting the trimmed
    history instead would make the ceiling unreachable: the trim drops the
    oldest messages, so a conversation one question past the limit arrives
    looking exactly like one at the limit.
    """
    return sum(1 for m in messages if m.role == "user" and m.content.strip())


def _to_langchain(messages: list[Message]) -> list:
    """Trust nothing from the client except user and assistant text.

    Tool calls and system messages are dropped rather than rejected: a client
    replaying them would be either a stale page or an injection attempt, and
    neither deserves an error page. The trim is a token-cost guard, independent
    of the question ceiling: a client is free to claim one question and a
    thousand answers.
    """
    out = []
    for msg in messages[-MAX_HISTORY_MESSAGES:]:
        text = msg.content.strip()[:MAX_QUESTION_CHARS]
        if not text:
            continue
        if msg.role == "user":
            out.append(HumanMessage(text))
        elif msg.role == "assistant":
            out.append(AIMessage(text))
    return out


def _sse(event: str, data: dict) -> str:
    return f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.post("/api/chat")
async def chat(request: Request, body: ChatRequest):
    history = _to_langchain(body.messages)

    if not history or not isinstance(history[-1], HumanMessage):
        return JSONResponse({"error": "The last message must be a question."}, status_code=400)

    if _count_questions(body.messages) > MAX_USER_MESSAGES:
        return JSONResponse(
            {
                "error": (
                    f"This conversation reached its {MAX_USER_MESSAGES}-question limit. "
                    "Reload the page to start over, or reach Rafael on LinkedIn."
                )
            },
            status_code=429,
        )

    if not os.environ.get("OPENAI_API_KEY"):
        return JSONResponse({"error": "The agent is not configured yet."}, status_code=503)

    if (message := _rate_limited(_client_ip(request))) is not None:
        return JSONResponse({"error": message}, status_code=429)

    compiled = await graph()

    async def stream():
        # Announced before the first token so the page can show its thinking
        # state without guessing whether the request got through.
        yield _sse("start", {})
        sent = False
        try:
            async for mode, payload in compiled.astream(
                {"messages": history},
                stream_mode=["updates", "messages"],
                config={"recursion_limit": RECURSION_LIMIT},
            ):
                if mode == "messages":
                    chunk, meta = payload
                    # Only the agent node's tokens are the answer. Without this
                    # filter the tools node streams too, and every document the
                    # agent reads arrives on the page in full before the real
                    # reply — which is exactly what it did.
                    if meta.get("langgraph_node") != "agent":
                        continue
                    if text := getattr(chunk, "content", ""):
                        sent = True
                        yield _sse("token", {"t": text})
                elif mode == "updates":
                    # The agent node's update carries the tool calls it just
                    # decided on — which is exactly when the page should say
                    # which document is being opened.
                    for update in payload.values():
                        for msg in (update or {}).get("messages", []):
                            for call in getattr(msg, "tool_calls", None) or []:
                                yield _sse("doc", {"slug": call["args"].get("slug", "")})
        except Exception as exc:  # noqa: BLE001 — the stream is already open
            # The status line is long gone by now, so the only way to report a
            # failure is inside the stream itself.
            print(f"[ERROR] chat stream failed: {exc!r}")
            yield _sse("error", {"message": "Something broke while answering. Please try again."})
        else:
            # A completed run that emitted nothing is the token budget being
            # spent entirely on reasoning. Silence looks like a hung page, so
            # say so instead of closing an empty bubble.
            if not sent:
                print("[ERROR] chat stream produced no answer tokens")
                yield _sse("error", {"message": "The answer came back empty. Please try asking again."})
        yield _sse("done", {})

    return StreamingResponse(
        stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache, no-transform", "X-Accel-Buffering": "no"},
    )


@app.get("/api/health")
async def health():
    from . import tools as corpus

    return {"documents": len(corpus.get_index()), "model": os.environ.get("OPENAI_MODEL", "default")}


# --- local development -------------------------------------------------------
#
# In production Vercel serves the page and the photo statically and only routes
# /api/* here. Mounting them too means `uvicorn api.index:app` is the whole
# stack locally, with no second server and no CORS.

if (ROOT / "public").is_dir():
    app.mount("/public", StaticFiles(directory=ROOT / "public"), name="public")


@app.get("/")
async def page():
    return FileResponse(ROOT / "index.html")
