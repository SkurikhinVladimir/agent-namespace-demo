import os

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .tools.git import git_tool
from .tools.skills import skills_tool
from .tools.tasks import tasks_tool
from .tools.wiki import wiki_tool


@tool
def wiki(command: str, args: dict) -> str:
    """Corporate knowledge base.

    Commands: search, read, list.
    Pass args={'help': true} to any command to get usage info.
    """
    return wiki_tool.execute(command, args)


@tool
def tasks(command: str, args: dict) -> str:
    """Task tracker.

    Commands: list, get, save.
    Pass args={'help': true} to any command to get usage info.
    """
    return tasks_tool.execute(command, args)


@tool
def git(command: str, args: dict) -> str:
    """Git repository management.

    Commands: pr, issue, repo.
    Pass args={'help': true} to any command to get usage info.
    """
    return git_tool.execute(command, args)


@tool
def skills(command: str, args: dict) -> str:
    """Skills knowledge base — instructions for how to perform tasks.

    Commands: list, get, save, delete.
    Pass args={'help': true} to any command to get usage info.
    """
    return skills_tool.execute(command, args)


def build_agent():
    llm = ChatOpenAI(
        model=os.environ.get("LLM_MODEL", "gpt-4o-mini"),
        base_url=os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1"),
        api_key=os.environ.get("LLM_API_KEY", ""),
    )
    return create_react_agent(
        model=llm,
        tools=[wiki, tasks, git, skills],
        prompt=(
            "You are a helpful developer assistant. "
            "You have access to four namespace tools: wiki, tasks, git, skills. "
            "When unsure about a tool's arguments, call it with args={'help': true} first. "
            "Always be concise and show the user what tool calls you are making."
        ),
    )
