from .base import NamespaceTool

TASKS_HELP = {
    "list": "list [--assignee=me|user_id] [--state=started|in_review|done]",
    "get": "get --id=ID — get a task by ID (e.g. TASK-1)",
    "save": "save [--id=ID] [--title=TEXT] [--state=STATE] — create or update a task",
}

MOCK_TASKS: dict[str, dict] = {
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
        self._tasks = dict(MOCK_TASKS)

    def _get_help(self, command: str) -> str:
        if command in TASKS_HELP:
            return TASKS_HELP[command]
        lines = ["Available commands:"] + [f"  {v}" for v in TASKS_HELP.values()]
        return "\n".join(lines)

    def _execute_command(self, command: str, args: dict) -> str:
        if command == "list":
            assignee = args.get("assignee")
            state = args.get("state")
            results = list(self._tasks.values())
            if assignee:
                results = [t for t in results if t["assignee"] == assignee]
            if state:
                results = [t for t in results if t["state"] == state]
            if not results:
                return "No tasks found."
            return "\n".join(f"- {t['id']}: {t['title']} ({t['state']})" for t in results)

        if command == "get":
            task_id = args.get("id", "")
            task = self._tasks.get(task_id)
            if not task:
                return f"Task '{task_id}' not found."
            return (
                f"ID: {task['id']}\n"
                f"Title: {task['title']}\n"
                f"State: {task['state']}\n"
                f"Assignee: {task['assignee']}\n"
                f"Branch: {task['branch']}\n"
                f"Description: {task['description']}"
            )

        if command == "save":
            task_id = args.get("id")
            if task_id and task_id in self._tasks:
                self._tasks[task_id].update({k: v for k, v in args.items() if k != "id"})
                return f"Task {task_id} updated."
            new_id = task_id or f"TASK-{len(self._tasks) + 1}"
            self._tasks[new_id] = {
                "id": new_id,
                "title": args.get("title", "Untitled"),
                "state": args.get("state", "started"),
                "assignee": args.get("assignee", "me"),
                "branch": args.get("branch", ""),
                "description": args.get("description", ""),
            }
            return f"Task {new_id} created."

        return f"Unknown command '{command}'. Use tasks(command='list', args={{'help': true}}) for help."


tasks_tool = TasksTool()
