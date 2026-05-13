import logging

from agent_namespace_demo.tools.base import NamespaceTool

logger = logging.getLogger(__name__)

_HELP: dict[str, str] = {
    "pr": "pr [--action=create|list|merge] [--branch=NAME] [--title=TEXT] [--id=ID] [--state=open|merged]",
    "issue": "issue [--action=list|create] [--title=TEXT] [--body=TEXT] [--state=open|closed]",
    "repo": "repo [--action=list|create|delete] [--name=NAME] [--description=TEXT]",
}

_PRS: list[dict[str, str]] = [
    {"id": "PR-1", "title": "Add auth middleware", "branch": "feature/auth", "state": "open"},
    {"id": "PR-2", "title": "Fix null pointer", "branch": "fix/api-bug", "state": "open"},
    {"id": "PR-3", "title": "Update CI pipeline", "branch": "ci/update", "state": "merged"},
]

_ISSUES: list[dict[str, str]] = [
    {"id": "ISS-1", "title": "Auth token expires too fast", "state": "open"},
    {"id": "ISS-2", "title": "API returns 500 on empty body", "state": "open"},
    {"id": "ISS-3", "title": "Docs site broken on mobile", "state": "closed"},
]

_REPOS: list[dict[str, str]] = [
    {"name": "backend", "description": "Main API service"},
    {"name": "frontend", "description": "React web app"},
    {"name": "infra", "description": "Terraform + k8s manifests"},
]


class GitTool(NamespaceTool):
    def __init__(self) -> None:
        import copy

        self._prs = copy.deepcopy(_PRS)
        self._issues = copy.deepcopy(_ISSUES)
        self._repos = copy.deepcopy(_REPOS)

    def _get_help(self, command: str) -> str:
        if command in _HELP:
            return _HELP[command]
        return "Available commands:\n" + "\n".join(f"  {v}" for v in _HELP.values())

    def _execute_command(self, command: str, args: dict[str, object]) -> str:
        logger.debug("git %s args=%s", command, args)
        if command == "pr":
            return self._handle_pr(args)
        if command == "issue":
            return self._handle_issue(args)
        if command == "repo":
            return self._handle_repo(args)
        return f"Unknown command '{command}'. Use git(command='pr', args={{'help': true}}) for help."

    def _handle_pr(self, args: dict[str, object]) -> str:
        action = str(args.get("action", "list"))
        if action == "list":
            state = str(args["state"]) if "state" in args else None
            prs = self._prs if not state else [p for p in self._prs if p["state"] == state]
            if not prs:
                return "No pull requests found."
            return "\n".join(f"- {p['id']}: {p['title']} [{p['state']}] ({p['branch']})" for p in prs)
        if action == "create":
            branch = str(args.get("branch", "unknown"))
            title = str(args.get("title", "Untitled PR"))
            new_id = f"PR-{len(self._prs) + 1}"
            self._prs.append({"id": new_id, "title": title, "branch": branch, "state": "open"})
            return f"Pull request {new_id} created: '{title}' from branch '{branch}'."
        if action == "merge":
            pr_id = str(args.get("id", ""))
            for pr in self._prs:
                if pr["id"] == pr_id:
                    pr["state"] = "merged"
                    return f"Pull request {pr_id} merged."
            return f"PR '{pr_id}' not found."
        return f"Unknown action '{action}'."

    def _handle_issue(self, args: dict[str, object]) -> str:
        action = str(args.get("action", "list"))
        if action == "list":
            state = str(args["state"]) if "state" in args else None
            issues = self._issues if not state else [i for i in self._issues if i["state"] == state]
            if not issues:
                return "No issues found."
            return "\n".join(f"- {i['id']}: {i['title']} [{i['state']}]" for i in issues)
        if action == "create":
            new_id = f"ISS-{len(self._issues) + 1}"
            self._issues.append({
                "id": new_id,
                "title": str(args.get("title", "Untitled")),
                "body": str(args.get("body", "")),
                "state": "open",
            })
            return f"Issue {new_id} created: '{args.get('title', 'Untitled')}'."
        return f"Unknown action '{action}'."

    def _handle_repo(self, args: dict[str, object]) -> str:
        action = str(args.get("action", "list"))
        if action == "list":
            return "\n".join(f"- {r['name']}: {r['description']}" for r in self._repos)
        if action == "create":
            name = str(args.get("name", "unnamed"))
            self._repos.append({"name": name, "description": str(args.get("description", ""))})
            return f"Repository '{name}' created."
        if action == "delete":
            name = str(args.get("name", ""))
            before = len(self._repos)
            self._repos = [r for r in self._repos if r["name"] != name]
            return f"Repository '{name}' deleted." if len(self._repos) < before else f"Repo '{name}' not found."
        return f"Unknown action '{action}'."
