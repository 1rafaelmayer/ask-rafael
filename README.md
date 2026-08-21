# ask-rafael

An interactive one-page CV. At the top, an agent answers questions about my work
from a corpus of documents I wrote about myself. Below it, the static summary.

Live at **ask-rafael.vercel.app** · [LinkedIn](https://www.linkedin.com/in/rafael-alves-mayer/)

## The design

No database, no vector store, no MCP server, no long-running process. The
documents ship inside the deployment bundle.

```
ask-rafael/
├─ docs/              26 markdown documents — the knowledge base, and the
│                     single source of truth for everything the agent says
├─ api/
│  ├─ index.py        FastAPI: POST /api/chat as SSE, plus the guards
│  ├─ tools.py        corpus loading, and the two functions the agent uses
│  └─ agent.py        the LangGraph graph, the persona, the system prompt
├─ public/rafael.jpg
├─ index.html         the whole page: no build, no framework, no CDN
└─ tests/
```

**Retrieval is routing, not search.** Every document declares in its YAML
frontmatter *when it should be read*:

```yaml
---
when_to_use: >
  Multi-agent system for hospital services over WhatsApp: routing
  architecture, the check-in state machine, state in PostgreSQL, and the
  trade-offs taken. Does not cover the academic coaching agent.
---
```

That catalog — 26 titles and their `when_to_use` lines, about 2.8k tokens — goes
into the system prompt at startup. The agent picks a slug from it and calls
`read_document(slug)` to get the document whole. There is no chunking, no
embedding, no similarity threshold to tune, and no index to rebuild when a
document changes.

This is the right shape only because the corpus is small: 26 documents, ~13k
words, the whole thing several times over inside one context window. The moment
that stops being true, this becomes the wrong design.

**The catalog is in the prompt rather than behind a `list_documents` tool** on
purpose: it costs ~2.8k cached tokens once and saves a full model round trip on
every single question, which on a page where somebody is watching a cursor blink
is the difference that matters.

**State lives in the browser.** The page holds the conversation and sends it back
with each request; the server keeps nothing between requests. It validates a
ceiling of 20 questions and drops anything that is not plain user or assistant
text, so a client cannot replay fabricated tool output or inject a system
message.

**Answers are grounded or absent.** The agent may only assert what it read in a
document. Everything else — compensation, availability, anything the corpus does
not cover — is redirected to LinkedIn rather than guessed at.

## Local development

Requires [uv](https://docs.astral.sh/uv/) and Python 3.12.

```bash
uv sync --all-groups
cp .env.example .env          # then put a real OPENAI_API_KEY in it
uv run uvicorn api.index:app --reload --port 8000
```

Open <http://localhost:8000>. The same process serves the page, the photo and the
API, so there is no second server and no CORS to configure. In production Vercel
serves the static files itself and only routes `/api/*` to Python.

```bash
uv run pytest        # 25 tests, no network, no model, ~1s
uv run ruff check .
```

The suite covers corpus loading (ported from the MCP server this grew out of),
the two agent-facing functions including slug traversal, and the endpoint with
the graph replaced by a script: the question ceiling, the per-visitor rate limit,
history sanitisation, a failure mid-stream, and the node filter on the token
stream — without which every document the agent reads is pasted into the reply.

## Environment

| Variable | Required | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | yes | Without it the endpoint answers 503 instead of failing at import. |
| `OPENAI_MODEL` | no | Defaults to `gpt-5-mini`. Swap models without touching code. |
| `MAX_OUTPUT_TOKENS` | no | Caps one completion. Default 2000 — on a reasoning model this budget also covers reasoning tokens, so setting it near the answer length returns an empty reply. |
| `OPENAI_REASONING_EFFORT` | no | Default `low`; reading a document and summarising it is not reasoning-heavy, and effort is latency the visitor watches. Blank to omit the parameter. |
| `LANGSMITH_TRACING` | no | `true` to trace. The questions visitors ask are the most useful signal this page produces. |
| `LANGSMITH_API_KEY` | no | Needed when tracing. |
| `LANGSMITH_PROJECT` | no | e.g. `ask-rafael`. |
| `DOCS_PATH` | no | Points the corpus somewhere other than `./docs`. |

## Deploying

1. Push this repo to GitHub.
2. On [vercel.com/new](https://vercel.com/new), import it. Framework preset
   **Other**; leave the build and output settings empty — there is no build.
3. Add the environment variables above under **Settings → Environment
   Variables**, for Production *and* Preview.
4. Deploy. `/api/health` reports the document count and the active model, which
   is the fastest way to confirm the corpus made it into the bundle.

One thing worth knowing before changing `vercel.json`: the rewrite **replaces**
the request path, so the function is always invoked with `/api/index` regardless
of the URL the visitor asked for. Every endpoint is therefore registered twice in
`api/index.py` — at its public path, which is what the page calls and what
uvicorn serves locally, and at `/api/index`, which is what production delivers.
Registering only the public path makes the deployed function answer FastAPI's own
404 to every request, and nothing about that failure points at routing.

**Set a monthly spend cap on the OpenAI account.** The endpoint is public and
unauthenticated. The in-process rate limit thins abuse, but every cold start gets
a fresh counter, so it cannot be the last line of defence — the spend cap is.

If the Vercel build cannot resolve dependencies from `pyproject.toml`, export a
lockfile it will definitely read:

```bash
uv export --no-dev --no-emit-project > requirements.txt
```

## Editing the content

`docs/` is the source of truth for what the agent says. Add or edit a markdown
file, make sure it has a `when_to_use`, and push — a document without one is
silently skipped, which `tests/test_corpus.py::test_the_real_corpus_loads_clean`
exists to catch.

The static section below the fold is hand-written in `index.html`, in English and
Portuguese, and does not read `docs/`. That is deliberate: it is a curated
distillation, not a dump. When the corpus changes materially, it needs editing
too.

## Prior art in this repo's lineage

The corpus loader and its tests come from
[professional_MCP](https://github.com/1rafaelmayer/professional_MCP), an MCP
server over the same documents. Point that server's `DOCS_PATH` at this repo's
`docs/` and both read the same directory — the corpus is not duplicated, and the
same documents are available to a local Claude session and to this page.

## License

MIT.
