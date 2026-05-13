import logging

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from agent_namespace_demo.config import Settings
from agent_namespace_demo.tools.git import GitTool
from agent_namespace_demo.tools.skills import SkillsTool
from agent_namespace_demo.tools.tasks import TasksTool
from agent_namespace_demo.tools.wiki import WikiTool

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = (
    "You are a helpful developer assistant. "
    "You have four namespace tools: wiki, tasks, git, skills. "
    "When unsure about a tool's arguments, call it with args={'help': true} first. "
    "Be concise."
)


def build_agent(
    settings: Settings,
    wiki: WikiTool,
    tasks: TasksTool,
    git: GitTool,
    skills: SkillsTool,
) -> object:
    @tool
    def wiki_tool(command: str, args: dict) -> str:  # type: ignore[type-arg]
        """Corporate knowledge base. Commands: search, read, list. Pass args={'help': true} for usage."""
        return wiki.execute(command, args)

    @tool
    def tasks_tool(command: str, args: dict) -> str:  # type: ignore[type-arg]
        """Task tracker. Commands: list, get, save. Pass args={'help': true} for usage."""
        return tasks.execute(command, args)

    @tool
    def git_tool(command: str, args: dict) -> str:  # type: ignore[type-arg]
        """Git repository tools. Commands: pr, issue, repo. Pass args={'help': true} for usage."""
        return git.execute(command, args)

    @tool
    def skills_tool(command: str, args: dict) -> str:  # type: ignore[type-arg]
        """Skills knowledge base. Commands: list, get, save, delete. Pass args={'help': true} for usage."""
        return skills.execute(command, args)

    llm = ChatOpenAI(
        model=settings.llm_model,
        base_url=settings.llm_base_url,
        api_key=settings.llm_api_key.get_secret_value(),
    )

    logger.info("Building agent with model=%s base_url=%s", settings.llm_model, settings.llm_base_url)

    return create_react_agent(
        model=llm,
        tools=[wiki_tool, tasks_tool, git_tool, skills_tool],
        prompt=_SYSTEM_PROMPT,
    )
