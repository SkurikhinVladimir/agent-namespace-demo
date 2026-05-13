import pytest

from agent_namespace_demo.tools.git import GitTool


@pytest.fixture()
def git() -> GitTool:
    return GitTool()


def test_pr_list(git: GitTool) -> None:
    result = git.execute("pr", {"action": "list"})
    assert "PR-1" in result
    assert "PR-2" in result


def test_pr_list_by_state(git: GitTool) -> None:
    result = git.execute("pr", {"action": "list", "state": "merged"})
    assert "PR-3" in result
    assert "PR-1" not in result


def test_pr_create(git: GitTool) -> None:
    result = git.execute("pr", {"action": "create", "branch": "feat/x", "title": "My PR"})
    assert "created" in result
    assert "My PR" in result


def test_pr_merge(git: GitTool) -> None:
    git.execute("pr", {"action": "create", "branch": "feat/x", "title": "My PR"})
    result = git.execute("pr", {"action": "merge", "id": "PR-4"})
    assert "merged" in result


def test_pr_merge_missing(git: GitTool) -> None:
    result = git.execute("pr", {"action": "merge", "id": "PR-999"})
    assert "not found" in result


def test_issue_list(git: GitTool) -> None:
    result = git.execute("issue", {"action": "list"})
    assert "ISS-1" in result


def test_issue_create(git: GitTool) -> None:
    result = git.execute("issue", {"action": "create", "title": "Bug X"})
    assert "created" in result


def test_repo_list(git: GitTool) -> None:
    result = git.execute("repo", {"action": "list"})
    assert "backend" in result


def test_instances_are_isolated() -> None:
    g1 = GitTool()
    g2 = GitTool()
    g1.execute("pr", {"action": "create", "branch": "b", "title": "t"})
    result = g2.execute("pr", {"action": "list"})
    assert "PR-4" not in result


def test_help(git: GitTool) -> None:
    result = git.execute("pr", {"help": True})
    assert "action" in result


def test_unknown_command(git: GitTool) -> None:
    result = git.execute("bogus", {})
    assert "Unknown" in result
