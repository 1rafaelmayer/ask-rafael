"""Corpus loading. Ported from the professional_MCP suite, which is where these
cases were first worked out — plus one that guards the real documents."""

from pathlib import Path

import pytest

from api.tools import CorpusError, load_index

REPO_ROOT = Path(__file__).resolve().parent.parent


def write(root: Path, rel: str, body: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    return path


def doc(when_to_use: str = "When you need the thing.", body: str = "Content.") -> str:
    return f"---\nwhen_to_use: {when_to_use}\n---\n\n# Heading\n\n{body}\n"


def test_slug_derives_from_nested_path(tmp_path):
    write(tmp_path, "projetos/agentes-hospital.md", doc())

    assert list(load_index(tmp_path)) == ["projetos/agentes-hospital"]


def test_title_falls_back_to_filename(tmp_path):
    write(tmp_path, "skills/genai-agentic.md", doc())
    write(tmp_path, "skills/idiomas.md", "---\ntitle: Languages\nwhen_to_use: Levels.\n---\n\nBody.\n")

    index = load_index(tmp_path)

    assert index["skills/genai-agentic"].title == "Genai Agentic"
    assert index["skills/idiomas"].title == "Languages"


def test_document_without_when_to_use_is_excluded(tmp_path, capsys):
    write(tmp_path, "good.md", doc())
    write(tmp_path, "orphan.md", "# No frontmatter at all\n")
    write(tmp_path, "blank.md", '---\nwhen_to_use: "   "\n---\n\nBody.\n')

    index = load_index(tmp_path)

    assert list(index) == ["good"]
    stderr = capsys.readouterr().err
    assert "orphan.md" in stderr and "blank.md" in stderr


def test_dot_prefixed_directories_are_skipped(tmp_path):
    write(tmp_path, "kept.md", doc())
    write(tmp_path, ".git/hooks/notes.md", doc())
    write(tmp_path, ".obsidian/scratch.md", doc())

    assert list(load_index(tmp_path)) == ["kept"]


def test_non_directory_root_raises(tmp_path):
    with pytest.raises(CorpusError, match="not a directory"):
        load_index(tmp_path / "nope")


def test_render_puts_header_before_body(tmp_path):
    write(tmp_path, "cargos/distrito.md", doc(when_to_use="Current role.", body="AI Factory."))

    rendered = load_index(tmp_path)["cargos/distrito"].render()

    header, _, body = rendered.partition("\n---\n\n")
    assert header.startswith("---\n")
    assert '"cargos/distrito"' in header
    assert '"Current role."' in header
    assert body.startswith("# Heading")
    assert "AI Factory." in body


def test_body_is_read_fresh_from_disk(tmp_path):
    path = write(tmp_path, "perfil.md", doc(body="Old text."))
    document = load_index(tmp_path)["perfil"]

    path.write_text(doc(body="New text."), encoding="utf-8")

    assert "New text." in document.read_body()


def test_oversized_document_warns_but_loads(tmp_path, capsys):
    write(tmp_path, "huge.md", doc(body="x" * (60 * 1024)))

    assert "huge" in load_index(tmp_path)
    assert "huge.md" in capsys.readouterr().err


def test_empty_corpus_warns(tmp_path, capsys):
    assert load_index(tmp_path) == {}
    assert "no usable documents" in capsys.readouterr().err


def test_the_real_corpus_loads_clean(capsys):
    """The one test that would actually catch a broken document before deploy.

    Silence on stderr is the assertion that matters: a document that lost its
    `when_to_use` is skipped rather than refused, so without this it would go
    missing from the catalog and nothing would fail.
    """
    index = load_index(REPO_ROOT / "docs")

    assert len(index) >= 20
    assert "perfil" in index
    assert all(d.when_to_use for d in index.values())
    assert capsys.readouterr().err == ""
