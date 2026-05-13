# 06 — Reuse a Skill

Agent recognises a "close out" intent, scans available skills, retrieves the relevant one, and follows its steps.

```json
[
  {
    "role": "system",
    "content": "You are a helpful developer assistant. You have four namespace tools: wiki, tasks, git, skills. When unsure about a tool's arguments, call it with args={\"help\": true} first. Be concise."
  },
  {
    "role": "user",
    "content": "TASK-2 PR got approved. Wrap it up."
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
          "arguments": "{\"command\": \"list\", \"args\": {}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "- create_pr_for_task: Create a pull request from a task ID\n- update_task_after_review: Merge PR and mark the task as done",
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
          "name": "skills_tool",
          "arguments": "{\"command\": \"get\", \"args\": {\"name\": \"update_task_after_review\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "Skill: update_task_after_review\nDescription: Merge PR and mark the task as done\nSteps:\n1. Call git(command='pr', args={'action': 'merge', 'id': PR_ID}).\n2. Call tasks(command='save', args={'id': TASK_ID, 'state': 'done'}).\n3. Confirm to the user.",
    "tool_call_id": "call_02"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_03",
        "type": "function",
        "function": {
          "name": "git_tool",
          "arguments": "{\"command\": \"pr\", \"args\": {\"action\": \"merge\", \"id\": \"PR-2\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "Pull request PR-2 merged.",
    "tool_call_id": "call_03"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_04",
        "type": "function",
        "function": {
          "name": "tasks_tool",
          "arguments": "{\"command\": \"save\", \"args\": {\"id\": \"TASK-2\", \"state\": \"done\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "Task TASK-2 updated.",
    "tool_call_id": "call_04"
  },
  {
    "role": "assistant",
    "content": "Done — PR-2 merged and TASK-2 marked as done."
  }
]
```
