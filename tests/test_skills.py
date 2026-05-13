import pytest

from agent_namespace_demo.tools.skills import SkillsTool


@pytest.fixture()
def skills() -> SkillsTool:
    return SkillsTool()


def test_list_preseeded(skills: SkillsTool) -> None:
    result = skills.execute("list", {})
    assert "create_pr_for_task" in result


def test_get_existing(skills: SkillsTool) -> None:
    result = skills.execute("get", {"name": "create_pr_for_task"})
    assert "Steps" in result
    assert "tasks" in result


def test_get_missing(skills: SkillsTool) -> None:
    result = skills.execute("get", {"name": "does_not_exist"})
    assert "not found" in result


def test_save_and_get(skills: SkillsTool) -> None:
    skills.execute("save", {"name": "my_skill", "description": "do X", "steps": ["step 1"]})
    result = skills.execute("get", {"name": "my_skill"})
    assert "do X" in result
    assert "step 1" in result


def test_save_missing_name(skills: SkillsTool) -> None:
    result = skills.execute("save", {"description": "no name"})
    assert "required" in result


def test_delete(skills: SkillsTool) -> None:
    skills.execute("save", {"name": "temp", "description": "x", "steps": []})
    skills.execute("delete", {"name": "temp"})
    result = skills.execute("get", {"name": "temp"})
    assert "not found" in result


def test_delete_missing(skills: SkillsTool) -> None:
    result = skills.execute("delete", {"name": "ghost"})
    assert "not found" in result


def test_instances_are_isolated() -> None:
    s1 = SkillsTool()
    s2 = SkillsTool()
    s1.execute("save", {"name": "x", "description": "y", "steps": []})
    result = s2.execute("get", {"name": "x"})
    assert "not found" in result


def test_help(skills: SkillsTool) -> None:
    result = skills.execute("list", {"help": True})
    assert "list" in result


def test_unknown_command(skills: SkillsTool) -> None:
    result = skills.execute("bogus", {})
    assert "Unknown" in result
