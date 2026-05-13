import logging

from agent_namespace_demo.tools.base import NamespaceTool

logger = logging.getLogger(__name__)

_HELP: dict[str, str] = {
    "search": "search --query=TEXT — search pages by keyword",
    "read": "read --page_id=ID — read a wiki page by its ID",
    "list": "list — list all available wiki pages",
}

_PAGES: dict[str, dict[str, str]] = {
    "deploy-guide": {
        "id": "deploy-guide",
        "title": "Deployment Guide",
        "content": (
            "# Deployment Guide\n\n"
            "1. Run `make build` to build the Docker image.\n"
            "2. Push to registry: `make push`.\n"
            "3. Apply k8s manifests: `kubectl apply -f deploy/`.\n"
            "4. Verify rollout: `kubectl rollout status deployment/app`."
        ),
    },
    "onboarding": {
        "id": "onboarding",
        "title": "Developer Onboarding",
        "content": (
            "# Developer Onboarding\n\n"
            "1. Clone the repo and run `make setup`.\n"
            "2. Copy `.env.example` to `.env` and fill in secrets.\n"
            "3. Run `make dev` to start the local stack."
        ),
    },
    "api-conventions": {
        "id": "api-conventions",
        "title": "API Conventions",
        "content": (
            "# API Conventions\n\n"
            "- REST endpoints follow `/v1/<resource>` pattern.\n"
            "- Use snake_case for JSON fields.\n"
            "- All timestamps are ISO-8601 UTC."
        ),
    },
}


class WikiTool(NamespaceTool):
    def _get_help(self, command: str) -> str:
        if command in _HELP:
            return _HELP[command]
        return "Available commands:\n" + "\n".join(f"  {v}" for v in _HELP.values())

    def _execute_command(self, command: str, args: dict[str, object]) -> str:
        logger.debug("wiki %s args=%s", command, args)
        if command == "search":
            return self._search(str(args.get("query", "")))
        if command == "read":
            return self._read(str(args.get("page_id", "")))
        if command == "list":
            return "\n".join(f"- {p['id']}: {p['title']}" for p in _PAGES.values())
        return f"Unknown command '{command}'. Use wiki(command='list', args={{'help': true}}) for help."

    def _search(self, query: str) -> str:
        q = query.lower()
        hits = [
            f"- {p['id']}: {p['title']}"
            for p in _PAGES.values()
            if q in p["title"].lower() or q in p["content"].lower()
        ]
        return "\n".join(hits) if hits else "No pages found."

    def _read(self, page_id: str) -> str:
        page = _PAGES.get(page_id)
        if page is None:
            return f"Page '{page_id}' not found. Use wiki(command='list') to see available pages."
        return page["content"]
