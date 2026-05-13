#!/usr/bin/env python
"""Interactive demo — chat with the namespace agent using a real LLM."""

import os

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()

if not os.environ.get("LLM_API_KEY"):
    raise SystemExit("LLM_API_KEY is not set. Copy .env.example to .env and fill in your key.")

from agent.graph import build_agent  # noqa: E402  (after load_dotenv)

BANNER = """
╔══════════════════════════════════════════════════════╗
║        Tool Namespace Pattern — Interactive Demo     ║
║  Type your request. All tool calls are shown live.   ║
║  Press Ctrl-C or type 'exit' to quit.                ║
╚══════════════════════════════════════════════════════╝
"""


def print_tool_call(name: str, args: dict) -> None:
    args_str = ", ".join(f"{k}={v!r}" for k, v in args.items())
    print(f"\033[33m[Tool call] {name}({args_str})\033[0m")


def print_tool_result(result: str) -> None:
    for line in result.strip().splitlines():
        print(f"\033[36m  {line}\033[0m")


def run() -> None:
    print(BANNER)
    agent = build_agent()
    history: list = []

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
        all_messages = result["messages"]

        for msg in all_messages[len(history):]:
            msg_type = type(msg).__name__
            if msg_type == "AIMessage":
                if msg.tool_calls:
                    for tc in msg.tool_calls:
                        print_tool_call(tc["name"], tc["args"])
                elif msg.content:
                    print(f"\nAgent: {msg.content}")
            elif msg_type == "ToolMessage":
                print_tool_result(msg.content)

        history = all_messages


if __name__ == "__main__":
    run()
