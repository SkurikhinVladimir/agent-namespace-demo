import logging
from copy import deepcopy

from agent_namespace_demo.tools.base import NamespaceTool

logger = logging.getLogger(__name__)

_HELP: dict[str, str] = {
    "list": "list [--assignee=me|user_id] [--state=started|in_review|done]",
    "get": "get --id=ID — get a task by ID (e.g. TASK-1)",
    "save": "save [--id=ID] [--title=TEXT] [--state=STATE] — create or update a task",
}

_SEED: dict[str, dict[str, str]] = {
    "TASK-1": {
        "id": "TASK-1",
        "title": "Implement auth",
        "state": "started",
        "assignee": "me",
        "branch": "feature/auth",
        "description": "Add JWT-based authentication to the API.",
    },
    "TASK-2": {
        "id": "TASK-2",
        "title": "Fix bug in API",
        "state": "in_review",
        "assignee": "me",
        "branch": "fix/api-bug",
        "description": "Null pointer exception when request body is empty.",
    },
    "TASK-3": {
        "id": "TASK-3",
        "title": "Update README",
        "state": "done",
        "assignee": "alice",
        "branch": "docs/readme",
        "description": "Add setup instructions and screenshots.",
    },
}


class TasksTool(NamespaceTool):
    def __init__(self) -> None:
        self._tasks: dict[str, dict[str, str]] = deepcopy(_SEED)
        self._counter: int = len(_SEED)

    def _get_help(self, command: str) -> str:
        if command in _HELP:
            return _HELP[command]
        return "Available commands:\n" + "\n".join(f"  {v}" for v in _HELP.values())

    def _execute_command(self, command: str, args: dict[str, object]) -> str:
        logger.debug("tasks %s args=%s", command, args)
        if command == "list":
            return self._list(
                assignee=str(args["assignee"]) if "assignee" in args else None,
                state=str(args["state"]) if "state" in args else None,
            )
        if command == "get":
            return self._get(str(args.get("id", "")))
        if command == "save":
            return self._save(args)
        return f"Unknown command '{command}'. Use tasks(command='list', args={{'help': true}}) for help."

    def _list(self, assignee: str | None, state: str | None) -> str:
        tasks = list(self._tasks.values())
        if assignee:
            tasks = [t for t in tasks if t["assignee"] == assignee]
        if state:
            tasks = [t for t in tasks if t["state"] == state]
        if not tasks:
            return "No tasks found."
        return "\n".join(f"- {t['id']}: {t['title']} ({t['state']})" for t in tasks)

    def _get(self, task_id: str) -> str:
        task = self._tasks.get(task_id)
        if task is None:
            return f"Task '{task_id}' not found."
        return (
            f"ID: {task['id']}\n"
            f"Title: {task['title']}\n"
            f"State: {task['state']}\n"
            f"Assignee: {task['assignee']}\n"
            f"Branch: {task['branch']}\n"
            f"Description: {task['description']}"
        )

    def _save(self, args: dict[str, object]) -> str:
        task_id = str(args["id"]) if "id" in args else None
        if task_id and task_id in self._tasks:
            self._tasks[task_id].update({k: str(v) for k, v in args.items() if k != "id"})
            return f"Task {task_id} updated."
        self._counter += 1
        new_id = task_id or f"TASK-{self._counter}"
        self._tasks[new_id] = {
            "id": new_id,
            "title": str(args.get("title", "Untitled")),
            "state": str(args.get("state", "started")),
            "assignee": str(args.get("assignee", "me")),
            "branch": str(args.get("branch", "")),
            "description": str(args.get("description", "")),
        }
        return f"Task {new_id} created."
