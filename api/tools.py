"""The document corpus: loading, modelling, and the two functions the agent calls.

Ported from the professional_MCP server, minus the MCP protocol layer. The
split that mattered there still matters here: everything that can actually
break lives in this module, so the tests never have to stand a server — or an
LLM — up.

Retrieval is *routing*, not search. There is no chunking, no embeddings, no
vector store. Every document declares in its frontmatter when it should be
read, the agent gets that catalog up front, and it picks a slug itself. At 26
documents and ~13k words the whole corpus fits in a context window several
times over, so the expensive machinery would buy nothing.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import frontmatter

# Soft limits. Crossing either is a warning, never fatal.
MAX_DOCUMENTS = 50
MAX_DOCUMENT_BYTES = 50 * 1024

# The corpus ships inside the deployment bundle, one level up from this file.
# DOCS_PATH overrides it, which is what lets the local MCP server and this app
# read the very same directory.
DEFAULT_DOCS_PATH = Path(__file__).resolve().parent.parent / "docs"


class CorpusError(Exception):
    """A defect that makes the corpus unservable. Aborts startup."""


@dataclass(frozen=True)
class Document:
    slug: str          # "projetos/agentes-whatsapp-hospital" — mirrors the folders
    path: Path         # absolute path on disk
    title: str         # display only; carries no routing weight
    when_to_use: str   # the routing signal the agent reads

    def read_body(self) -> str:
        """Body only, frontmatter stripped."""
        return frontmatter.load(self.path).content.strip()

    def render(self) -> str:
        """What `read_document` returns: a short header, then the body.

        The header re-emits the corpus's own frontmatter format and keeps the
        document's declared scope — especially its "does not cover" clause — in
        front of the agent while it reads, not only while it chooses.
        """
        header = "\n".join(
            f"{key}: {json.dumps(value, ensure_ascii=False)}"
            for key, value in (
                ("slug", self.slug),
                ("title", self.title),
                ("when_to_use", self.when_to_use),
            )
        )
        return f"---\n{header}\n---\n\n{self.read_body()}"


def _warn(message: str) -> None:
    print(f"[WARN] {message}", file=sys.stderr)


def load_index(root: Path) -> dict[str, Document]:
    """Build the catalog from every well-formed markdown file under `root`."""
    if not root.is_dir():
        raise CorpusError(f"docs path is not a directory: {root}")

    index: dict[str, Document] = {}
    skipped: list[str] = []

    for file in sorted(root.rglob("*.md")):
        rel = file.relative_to(root)

        # Keeps .git/, .obsidian/ and friends out when the corpus is a checkout.
        if any(part.startswith(".") for part in rel.parts):
            continue

        slug = rel.with_suffix("").as_posix()

        # Only reachable on a case-insensitive mount, since we glob *.md alone —
        # kept because shadowing one document with another breaks routing in a
        # way that is near-impossible to diagnose from the outside.
        if slug in index:
            raise CorpusError(f"duplicate slug: {slug}")

        post = frontmatter.load(file)
        when_to_use = str(post.get("when_to_use") or "").strip()

        # No routing signal means no reason to be in the catalog. Serving it with
        # a placeholder would add noise while appearing to work.
        if not when_to_use:
            skipped.append(rel.as_posix())
            continue

        size = file.stat().st_size
        if size > MAX_DOCUMENT_BYTES:
            _warn(f"{rel} is {size // 1024} KB; large documents flood the agent's context")

        index[slug] = Document(
            slug=slug,
            path=file,
            title=str(post.get("title") or file.stem.replace("-", " ").title()),
            when_to_use=when_to_use,
        )

    if skipped:
        _warn(f"excluded, no 'when_to_use': {', '.join(skipped)}")

    if len(index) > MAX_DOCUMENTS:
        _warn(
            f"{len(index)} documents; past ~{MAX_DOCUMENTS} the catalog itself gets "
            "expensive to read and hand-written routing starts to degrade"
        )

    if not index:
        _warn(f"no usable documents found in {root}")

    return index


@lru_cache(maxsize=1)
def get_index() -> dict[str, Document]:
    """The process-wide corpus, loaded once per serverless instance.

    Cached because a cold start already costs enough without re-walking the
    bundle on every request, and the bundle is read-only in production anyway.
    """
    raw = os.environ.get("DOCS_PATH", "").strip()
    root = Path(raw).expanduser().resolve() if raw else DEFAULT_DOCS_PATH
    return load_index(root)


# --- the agent's surface -----------------------------------------------------
#
# `list_documents` is not exposed as a tool: its whole output is ~1.5k tokens,
# so it goes into the system prompt instead and saves a round trip on every
# single question. It stays a function because the prompt is built from it.


def list_documents(index: dict[str, Document] | None = None) -> list[dict]:
    """The catalog: what exists, and when to read each one."""
    index = get_index() if index is None else index
    return [
        {"slug": d.slug, "title": d.title, "when_to_use": d.when_to_use}
        for d in index.values()
    ]


def read_document(slug: str, index: dict[str, Document] | None = None) -> str:
    """Read one document in full.

    A dict lookup, never a path join: an agent-supplied slug never reaches the
    filesystem, so "../../etc/passwd" is a miss rather than a traversal.
    """
    index = get_index() if index is None else index
    doc = index.get(slug)
    if doc is None:
        # Listing every slug here would make the error longer than the catalog
        # it is pointing at — and the catalog is already in the system prompt.
        raise ValueError(f"unknown slug: {slug!r}. Use one of the slugs in the catalog.")
    return doc.render()
