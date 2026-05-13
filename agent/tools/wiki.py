from .base import NamespaceTool

WIKI_HELP = {
    "search": "search --query=TEXT — search pages by keyword",
    "read": "read --page_id=ID — read a wiki page by its ID",
    "list": "list — list all available wiki pages",
}

MOCK_PAGES = {
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
            "Welcome! Follow these steps:\n"
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
        if command in WIKI_HELP:
            return WIKI_HELP[command]
        lines = ["Available commands:"] + [f"  {v}" for v in WIKI_HELP.values()]
        return "\n".join(lines)

    def _execute_command(self, command: str, args: dict) -> str:
        if command == "search":
            query = args.get("query", "").lower()
            results = [
                f"- {p['id']}: {p['title']}"
                for p in MOCK_PAGES.values()
                if query in p["title"].lower() or query in p["content"].lower()
            ]
            return "\n".join(results) if results else "No pages found."

        if command == "read":
            page_id = args.get("page_id", "")
            page = MOCK_PAGES.get(page_id)
            if not page:
                return f"Page '{page_id}' not found. Use wiki(command='list') to see available pages."
            return page["content"]

        if command == "list":
            lines = [f"- {p['id']}: {p['title']}" for p in MOCK_PAGES.values()]
            return "\n".join(lines)

        return f"Unknown command '{command}'. Use wiki(command='list', args={{'help': true}}) for help."


wiki_tool = WikiTool()
