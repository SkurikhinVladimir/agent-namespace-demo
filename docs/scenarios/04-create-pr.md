# 04 — Create PR from Task

Agent fetches task details to get the branch name, then opens the PR. Context from one tool feeds the next.

```json
[
  {
    "role": "system",
    "content": "You are a helpful developer assistant. You have four namespace tools: wiki, tasks, git, skills. When unsure about a tool's arguments, call it with args={\"help\": true} first. Be concise."
  },
  {
    "role": "user",
    "content": "Create a PR for TASK-1."
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
    "content": "PR-4 created: \"Implement auth\" from `feature/auth`."
  }
]
```
