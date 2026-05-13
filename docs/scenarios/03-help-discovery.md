# 03 — Help Discovery

Agent doesn't know the exact PR arguments, so it calls `help` first — then acts. This is the core pattern: the agent self-documents at runtime instead of relying on baked-in knowledge.

```json
[
  {
    "role": "system",
    "content": "You are a helpful developer assistant. You have four namespace tools: wiki, tasks, git, skills. When unsure about a tool's arguments, call it with args={\"help\": true} first. Be concise."
  },
  {
    "role": "user",
    "content": "Create a PR for the auth work."
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_01",
        "type": "function",
        "function": {
          "name": "git_tool",
          "arguments": "{\"command\": \"pr\", \"args\": {\"help\": true}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "pr [--action=create|list|merge] [--branch=NAME] [--title=TEXT] [--id=ID] [--state=open|merged]",
    "tool_call_id": "call_01"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_02",
        "type": "function",
        "function": {
          "name": "git_tool",
          "arguments": "{\"command\": \"pr\", \"args\": {\"action\": \"create\", \"branch\": \"feature/auth\", \"title\": \"Implement auth\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "Pull request PR-4 created: 'Implement auth' from branch 'feature/auth'.",
    "tool_call_id": "call_02"
  },
  {
    "role": "assistant",
    "content": "Done — PR-4 created: \"Implement auth\" from branch `feature/auth`."
  }
]
```
