# 01 — List Tasks

User asks for their assigned tasks. One tool call, straight answer.

```json
[
  {
    "role": "system",
    "content": "You are a helpful developer assistant. You have four namespace tools: wiki, tasks, git, skills. When unsure about a tool's arguments, call it with args={\"help\": true} first. Be concise."
  },
  {
    "role": "user",
    "content": "What tasks are assigned to me?"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_01",
        "type": "function",
        "function": {
          "name": "tasks_tool",
          "arguments": "{\"command\": \"list\", \"args\": {\"assignee\": \"me\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "- TASK-1: Implement auth (started)\n- TASK-2: Fix bug in API (in_review)",
    "tool_call_id": "call_01"
  },
  {
    "role": "assistant",
    "content": "You have 2 tasks:\n- TASK-1: Implement auth (started)\n- TASK-2: Fix bug in API (in_review)"
  }
]
```
