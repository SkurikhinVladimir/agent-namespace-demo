import pytest

from agent_namespace_demo.tools.tasks import TasksTool


@pytest.fixture()
def tasks() -> TasksTool:
    return TasksTool()


def test_list_all(tasks: TasksTool) -> None:
    result = tasks.execute("list", {})
    assert "TASK-1" in result
    assert "TASK-2" in result
    assert "TASK-3" in result


def test_list_by_assignee(tasks: TasksTool) -> None:
    result = tasks.execute("list", {"assignee": "me"})
    assert "TASK-1" in result
    assert "TASK-3" not in result


def test_list_by_state(tasks: TasksTool) -> None:
    result = tasks.execute("list", {"state": "done"})
    assert "TASK-3" in result
    assert "TASK-1" not in result


def test_list_no_results(tasks: TasksTool) -> None:
    result = tasks.execute("list", {"assignee": "nobody"})
    assert "No tasks found" in result


def test_get_existing(tasks: TasksTool) -> None:
    result = tasks.execute("get", {"id": "TASK-1"})
    assert "Implement auth" in result
    assert "feature/auth" in result


def test_get_missing(tasks: TasksTool) -> None:
    result = tasks.execute("get", {"id": "TASK-999"})
    assert "not found" in result


def test_save_creates_new(tasks: TasksTool) -> None:
    result = tasks.execute("save", {"title": "New task"})
    assert "created" in result


def test_save_updates_existing(tasks: TasksTool) -> None:
    tasks.execute("save", {"id": "TASK-1", "state": "done"})
    result = tasks.execute("get", {"id": "TASK-1"})
    assert "done" in result


def test_instances_are_isolated() -> None:
    t1 = TasksTool()
    t2 = TasksTool()
    t1.execute("save", {"id": "TASK-1", "state": "done"})
    result = t2.execute("get", {"id": "TASK-1"})
    assert "done" not in result


def test_help_list(tasks: TasksTool) -> None:
    result = tasks.execute("list", {"help": True})
    assert "assignee" in result


def test_help_save(tasks: TasksTool) -> None:
    result = tasks.execute("save", {"help": True})
    assert "state" in result


def test_unknown_command(tasks: TasksTool) -> None:
    result = tasks.execute("bogus", {})
    assert "Unknown" in result
