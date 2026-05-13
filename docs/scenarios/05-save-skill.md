# 05 — Save a Skill

User teaches the agent a reusable procedure. A skill is instruction text, not code — the agent reads it later and follows the steps using normal tools.

```json
[
  {
    "role": "system",
    "content": "You are a helpful developer assistant. You have four namespace tools: wiki, tasks, git, skills. When unsure about a tool's arguments, call it with args={\"help\": true} first. Be concise."
  },
  {
    "role": "user",
    "content": "Save a skill: after a PR is merged, mark the task as done."
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_01",
        "type": "function",
        "function": {
          "name": "skills_tool",
          "arguments": "{\"command\": \"save\", \"args\": {\"name\": \"update_task_after_review\", \"description\": \"Merge PR and mark the task as done\", \"steps\": [\"1. Call git(command='pr', args={'action': 'merge', 'id': PR_ID}).\", \"2. Call tasks(command='save', args={'id': TASK_ID, 'state': 'done'}).\", \"3. Confirm to the user.\"]}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "Skill 'update_task_after_review' saved.",
    "tool_call_id": "call_01"
  },
  {
    "role": "assistant",
    "content": "Saved skill \"update_task_after_review\". I'll remember: merge the PR, then mark the task done."
  }
]
```
