import logging

from agent_namespace_demo.config import Settings
from agent_namespace_demo.graph import build_agent
from agent_namespace_demo.repl import run
from agent_namespace_demo.tools.git import GitTool
from agent_namespace_demo.tools.skills import SkillsTool
from agent_namespace_demo.tools.tasks import TasksTool
from agent_namespace_demo.tools.wiki import WikiTool

logging.basicConfig(level=logging.WARNING, format="%(name)s %(levelname)s %(message)s")


def main() -> None:
    settings = Settings()
    agent = build_agent(
        settings=settings,
        wiki=WikiTool(),
        tasks=TasksTool(),
        git=GitTool(),
        skills=SkillsTool(),
    )
    run(agent)


if __name__ == "__main__":
    main()
