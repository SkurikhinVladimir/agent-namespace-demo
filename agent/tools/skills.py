from .base import NamespaceTool

SKILLS_HELP = {
    "list": "list — list all saved skills",
    "get": "get --name=NAME — get a skill by name",
    "save": "save --name=NAME --description=TEXT --steps=[...] — create or update a skill",
    "delete": "delete --name=NAME — delete a skill",
}

INITIAL_SKILLS: dict[str, dict] = {
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
        self._skills: dict[str, dict] = dict(INITIAL_SKILLS)

    def _get_help(self, command: str) -> str:
        if command in SKILLS_HELP:
            return SKILLS_HELP[command]
        lines = ["Available commands:"] + [f"  {v}" for v in SKILLS_HELP.values()]
        return "\n".join(lines)

    def _execute_command(self, command: str, args: dict) -> str:
        if command == "list":
            if not self._skills:
                return "No skills saved yet."
            return "\n".join(
                f"- {s['name']}: {s['description']}" for s in self._skills.values()
            )

        if command == "get":
            name = args.get("name", "")
            skill = self._skills.get(name)
            if not skill:
                return f"Skill '{name}' not found. Use skills(command='list') to see available skills."
            steps = "\n".join(skill["steps"])
            return f"Skill: {skill['name']}\nDescription: {skill['description']}\nSteps:\n{steps}"

        if command == "save":
            name = args.get("name")
            if not name:
                return "Error: 'name' is required."
            self._skills[name] = {
                "name": name,
                "description": args.get("description", ""),
                "steps": args.get("steps", []),
            }
            return f"Skill '{name}' saved."

        if command == "delete":
            name = args.get("name", "")
            if name in self._skills:
                del self._skills[name]
                return f"Skill '{name}' deleted."
            return f"Skill '{name}' not found."

        return f"Unknown command '{command}'. Use skills(command='list', args={{'help': true}}) for help."


skills_tool = SkillsTool()
