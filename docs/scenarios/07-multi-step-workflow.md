# 07 — Multi-Step Workflow

Single user message triggers five tool calls across three namespaces: tasks → wiki → wiki → git → tasks.

```json
[
  {
    "role": "system",
    "content": "You are a helpful developer assistant. You have four namespace tools: wiki, tasks, git, skills. When unsure about a tool's arguments, call it with args={\"help\": true} first. Be concise."
  },
  {
    "role": "user",
    "content": "Starting on TASK-1. Find the deploy docs, open a PR, and move the task to in_review."
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
          "name": "wiki_tool",
          "arguments": "{\"command\": \"search\", \"args\": {\"query\": \"deploy\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "- deploy-guide: Deployment Guide",
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
          "name": "wiki_tool",
          "arguments": "{\"command\": \"read\", \"args\": {\"page_id\": \"deploy-guide\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "# Deployment Guide\n\n1. Run `make build`.\n2. Push to registry: `make push`.\n3. Apply k8s manifests: `kubectl apply -f deploy/`.\n4. Verify rollout: `kubectl rollout status deployment/app`.",
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
          "name": "git_tool",
          "arguments": "{\"command\": \"pr\", \"args\": {\"action\": \"create\", \"branch\": \"feature/auth\", \"title\": \"Implement auth\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "Pull request PR-4 created: 'Implement auth' from branch 'feature/auth'.",
    "tool_call_id": "call_04"
  },
  {
    "role": "assistant",
    "content": null,
    "tool_calls": [
      {
        "id": "call_05",
        "type": "function",
        "function": {
          "name": "tasks_tool",
          "arguments": "{\"command\": \"save\", \"args\": {\"id\": \"TASK-1\", \"state\": \"in_review\"}}"
        }
      }
    ]
  },
  {
    "role": "tool",
    "content": "Task TASK-1 updated.",
    "tool_call_id": "call_05"
  },
  {
    "role": "assistant",
    "content": "All set for TASK-1:\n- Deploy guide found in the wiki.\n- PR-4 opened from `feature/auth`.\n- Task moved to in_review."
  }
]
```
