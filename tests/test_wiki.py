import pytest

from agent_namespace_demo.tools.wiki import WikiTool


@pytest.fixture()
def wiki() -> WikiTool:
    return WikiTool()


def test_list(wiki: WikiTool) -> None:
    result = wiki.execute("list", {})
    assert "deploy-guide" in result
    assert "onboarding" in result


def test_search_hit(wiki: WikiTool) -> None:
    result = wiki.execute("search", {"query": "deploy"})
    assert "deploy-guide" in result


def test_search_miss(wiki: WikiTool) -> None:
    result = wiki.execute("search", {"query": "zzznomatch"})
    assert "No pages found" in result


def test_read_existing(wiki: WikiTool) -> None:
    result = wiki.execute("read", {"page_id": "deploy-guide"})
    assert "Deployment Guide" in result


def test_read_missing(wiki: WikiTool) -> None:
    result = wiki.execute("read", {"page_id": "does-not-exist"})
    assert "not found" in result


def test_help(wiki: WikiTool) -> None:
    result = wiki.execute("search", {"help": True})
    assert "query" in result


def test_unknown_command(wiki: WikiTool) -> None:
    result = wiki.execute("bogus", {})
    assert "Unknown" in result
