"""Static dialogue — demonstrates namespace tools without a real LLM."""

from agent.tools.git import git_tool
from agent.tools.skills import skills_tool
from agent.tools.tasks import tasks_tool
from agent.tools.wiki import wiki_tool

SEPARATOR = "-" * 60


def show(label: str, result: str) -> None:
    print(f"\n\033[33m>>> {label}\033[0m")
    print(result)
    print(SEPARATOR)


def main() -> None:
    print("Tool Namespace Pattern — static demo\n" + SEPARATOR)

    # Scenario 1: list tasks
    show(
        "tasks(command='list', args={'assignee': 'me'})",
        tasks_tool.execute("list", {"assignee": "me"}),
    )

    # Scenario 2: get task details
    show(
        "tasks(command='get', args={'id': 'TASK-1'})",
        tasks_tool.execute("get", {"id": "TASK-1"}),
    )

    # Scenario 3: help discovery
    show(
        "git(command='pr', args={'help': True})",
        git_tool.execute("pr", {"help": True}),
    )

    # Scenario 4: create PR
    show(
        "git(command='pr', args={'action': 'create', 'branch': 'feature/auth', 'title': 'Implement auth'})",
        git_tool.execute("pr", {"action": "create", "branch": "feature/auth", "title": "Implement auth"}),
    )

    # Scenario 5: wiki search
    show(
        "wiki(command='search', args={'query': 'deploy'})",
        wiki_tool.execute("search", {"query": "deploy"}),
    )

    # Scenario 6: read wiki page
    show(
        "wiki(command='read', args={'page_id': 'deploy-guide'})",
        wiki_tool.execute("read", {"page_id": "deploy-guide"}),
    )

    # Scenario 7: list skills
    show(
        "skills(command='list', args={})",
        skills_tool.execute("list", {}),
    )

    # Scenario 8: get skill
    show(
        "skills(command='get', args={'name': 'create_pr_for_task'})",
        skills_tool.execute("get", {"name": "create_pr_for_task"}),
    )

    # Scenario 9: save new skill
    show(
        "skills(command='save', args={...})",
        skills_tool.execute(
            "save",
            {
                "name": "update_task_after_review",
                "description": "Update task state to done after PR is merged",
                "steps": [
                    "1. Call git(command='pr', args={'action': 'merge', 'id': PR_ID}).",
                    "2. Call tasks(command='save', args={'id': TASK_ID, 'state': 'done'}).",
                    "3. Confirm to the user.",
                ],
            },
        ),
    )

    # Scenario 10: tasks help
    show(
        "tasks(command='save', args={'help': True})",
        tasks_tool.execute("save", {"help": True}),
    )


if __name__ == "__main__":
    main()
