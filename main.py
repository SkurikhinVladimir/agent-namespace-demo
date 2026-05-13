import logging

from agent_namespace_demo.static_demo import run
from agent_namespace_demo.tools.git import GitTool
from agent_namespace_demo.tools.skills import SkillsTool
from agent_namespace_demo.tools.tasks import TasksTool
from agent_namespace_demo.tools.wiki import WikiTool

logging.basicConfig(level=logging.WARNING, format="%(name)s %(levelname)s %(message)s")


def main() -> None:
    run(
        wiki=WikiTool(),
        tasks=TasksTool(),
        git=GitTool(),
        skills=SkillsTool(),
    )


if __name__ == "__main__":
    main()
