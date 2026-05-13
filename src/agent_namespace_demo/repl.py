import logging
from typing import Any

from langchain_core.messages import HumanMessage

logger = logging.getLogger(__name__)

_BANNER = """
╔══════════════════════════════════════════════════════╗
║        Tool Namespace Pattern — Interactive Demo     ║
║  Type your request. All tool calls are shown live.   ║
║  Press Ctrl-C or type 'exit' to quit.                ║
╚══════════════════════════════════════════════════════╝
"""


def run(agent: Any) -> None:
    print(_BANNER)
    history: list[Any] = []

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

        if user_input.lower() in ("exit", "quit", "q"):
            print("Bye!")
            break

        if not user_input:
            continue

        history.append(HumanMessage(content=user_input))
        result = agent.invoke({"messages": history})
        all_messages: list[Any] = result["messages"]

        for msg in all_messages[len(history):]:
            msg_type = type(msg).__name__
            if msg_type == "AIMessage":
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                        args_str = ", ".join(f"{k}={v!r}" for k, v in tc["args"].items())
                        print(f"\033[33m[Tool] {tc['name']}({args_str})\033[0m")
                elif msg.content:
                    print(f"\nAgent: {msg.content}")
            elif msg_type == "ToolMessage":
                for line in msg.content.strip().splitlines():
                    print(f"\033[36m  {line}\033[0m")

        history = all_messages
