"""The two functions the agent's world is made of."""

import pytest

from api.tools import list_documents, load_index, read_document

CORPUS = """---
when_to_use: Routing hint for the agent.
title: Current Role
---

# Distrito

AI Factory.
"""


@pytest.fixture
def index(tmp_path):
    (tmp_path / "cargos").mkdir()
    (tmp_path / "cargos" / "distrito.md").write_text(CORPUS, encoding="utf-8")
    return load_index(tmp_path)


def test_catalog_carries_the_routing_signal(index):
    assert list_documents(index) == [
        {
            "slug": "cargos/distrito",
            "title": "Current Role",
            "when_to_use": "Routing hint for the agent.",
        }
    ]


def test_read_document_returns_header_and_body(index):
    out = read_document("cargos/distrito", index)

    assert '"cargos/distrito"' in out
    assert "AI Factory." in out


def test_unknown_slug_is_a_recoverable_error(index):
    with pytest.raises(ValueError, match="unknown slug"):
        read_document("cargos/nope", index)


def test_traversal_is_a_lookup_miss_not_a_read(index):
    """The slug never reaches the filesystem, so this can only ever be a miss."""
    for hostile in ("../../etc/passwd", "/etc/passwd", "cargos/../../../secrets"):
        with pytest.raises(ValueError, match="unknown slug"):
            read_document(hostile, index)
