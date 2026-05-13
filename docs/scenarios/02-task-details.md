# 02 — Task Details

User asks for full details on a specific task.

```json
[
  {
    "role": "system",
    "content": "You are a helpful developer assistant. You have four namespace tools: wiki, tasks, git, skills. When unsure about a tool's arguments, call it with args={\"help\": true} first. Be concise."
  },
  {
    "role": "user",
    "content": "Tell me more about TASK-1."
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
          "arguments": "{\"command\": \"get\", \"args\": {\"id\": \"TASK-1\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "ID: TASK-1\nTitle: Implement auth\nState: started\nAssignee: me\nBranch: feature/auth\nDescription: Add JWT-based authentication to the API.",
    "tool_call_id": "call_01"
  },
  {
    "role": "assistant",
    "content": "TASK-1 \"Implement auth\" is in progress on branch `feature/auth`. Description: Add JWT-based authentication to the API."
  }
]
```
