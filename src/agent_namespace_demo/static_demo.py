import logging

from agent_namespace_demo.tools.git import GitTool
from agent_namespace_demo.tools.skills import SkillsTool
from agent_namespace_demo.tools.tasks import TasksTool
from agent_namespace_demo.tools.wiki import WikiTool

logger = logging.getLogger(__name__)

_SEP = "-" * 60


def _show(label: str, result: str) -> None:
    print(f"\n\033[33m>>> {label}\033[0m")
    print(result)
    print(_SEP)


def run(wiki: WikiTool, tasks: TasksTool, git: GitTool, skills: SkillsTool) -> None:
    print("Tool Namespace Pattern — static demo\n" + _SEP)

    # Scenario 01: list tasks
    _show("tasks list --assignee=me", tasks.execute("list", {"assignee": "me"}))

    # Scenario 02: task details
    _show("tasks get --id=TASK-1", tasks.execute("get", {"id": "TASK-1"}))

    # Scenario 03: help discovery before using an unfamiliar command
    _show("git pr --help", git.execute("pr", {"help": True}))

    # Scenario 04: create PR from task info
    _show(
        "git pr --action=create --branch=feature/auth --title='Implement auth'",
        git.execute("pr", {"action": "create", "branch": "feature/auth", "title": "Implement auth"}),
    )

    # Scenario 05: wiki search + read
    _show("wiki search --query=deploy", wiki.execute("search", {"query": "deploy"}))
    _show("wiki read --page_id=deploy-guide", wiki.execute("read", {"page_id": "deploy-guide"}))

    # Scenario 06: skills
    _show("skills list", skills.execute("list", {}))
    _show("skills get --name=create_pr_for_task", skills.execute("get", {"name": "create_pr_for_task"}))

    # Scenario 07: save a new skill, then reuse it
    _show(
        "skills save --name=update_task_after_review",
        skills.execute(
            "save",
            {
                "name": "update_task_after_review",
                "description": "Merge PR and mark the task as done",
                "steps": [
                    "1. Call git(command='pr', args={'action': 'merge', 'id': PR_ID}).",
                    "2. Call tasks(command='save', args={'id': TASK_ID, 'state': 'done'}).",
                    "3. Confirm to the user.",
                ],
            },
        ),
    )
    _show("skills get --name=update_task_after_review", skills.execute("get", {"name": "update_task_after_review"}))
