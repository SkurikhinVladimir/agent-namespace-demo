import logging

from agent_namespace_demo.tools.base import NamespaceTool

logger = logging.getLogger(__name__)

_HELP: dict[str, str] = {
    "list": "list — list all saved skills",
    "get": "get --name=NAME — get a skill by name",
    "save": "save --name=NAME --description=TEXT --steps=[...] — create or update a skill",
    "delete": "delete --name=NAME — delete a skill",
}

_SEED: dict[str, dict[str, object]] = {
    "create_pr_for_task": {
        "name": "create_pr_for_task",
        "description": "Create a pull request from a task ID",
        "steps": [
            "1. Call tasks(command='get', args={'id': TASK_ID}) to get task details.",
            "2. Note the branch name and title from the task.",
            "3. Call git(command='pr', args={'action': 'create', 'branch': BRANCH, 'title': TITLE}).",
            "4. Report the new PR ID to the user.",
        ],
    },
}


class SkillsTool(NamespaceTool):
    def __init__(self) -> None:
        import copy

        self._skills: dict[str, dict[str, object]] = copy.deepcopy(_SEED)

    def _get_help(self, command: str) -> str:
        if command in _HELP:
            return _HELP[command]
        return "Available commands:\n" + "\n".join(f"  {v}" for v in _HELP.values())

    def _execute_command(self, command: str, args: dict[str, object]) -> str:
        logger.debug("skills %s args=%s", command, args)
        if command == "list":
            if not self._skills:
                return "No skills saved yet."
            return "\n".join(f"- {s['name']}: {s['description']}" for s in self._skills.values())
        if command == "get":
            return self._get(str(args.get("name", "")))
        if command == "save":
            return self._save(args)
        if command == "delete":
            return self._delete(str(args.get("name", "")))
        return f"Unknown command '{command}'. Use skills(command='list', args={{'help': true}}) for help."

    def _get(self, name: str) -> str:
        skill = self._skills.get(name)
        if skill is None:
            return f"Skill '{name}' not found. Use skills(command='list') to see available skills."
        steps = "\n".join(str(s) for s in skill["steps"])  # type: ignore[union-attr]
        return f"Skill: {skill['name']}\nDescription: {skill['description']}\nSteps:\n{steps}"

    def _save(self, args: dict[str, object]) -> str:
        name = str(args.get("name", ""))
        if not name:
            return "Error: 'name' is required."
        self._skills[name] = {
            "name": name,
            "description": str(args.get("description", "")),
            "steps": args.get("steps", []),
        }
        return f"Skill '{name}' saved."

    def _delete(self, name: str) -> str:
        if name in self._skills:
            del self._skills[name]
            return f"Skill '{name}' deleted."
        return f"Skill '{name}' not found."
