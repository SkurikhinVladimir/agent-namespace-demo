# Scenario 01 — List Tasks

## User Request

> "What tasks are assigned to me?"

## Steps

1. Agent decides to call `tasks` with `command="list"` and `assignee="me"`.
2. Tool returns a filtered list of tasks.
3. Agent formats and presents the result.

## Tool Calls

```python
tasks(command="list", args={"assignee": "me"})
```

## Tool Response

```
- TASK-1: Implement auth (started)
- TASK-2: Fix bug in API (in_review)
```

## Final Agent Response

```
You have 2 tasks assigned to you:
1. TASK-1: Implement auth (started)
2. TASK-2: Fix bug in API (in_review)
```

## Notes

The agent filtered by `assignee="me"` without needing to know the exact field names upfront — it inferred them from context. If it was unsure, it could call `tasks(command="list", args={"help": true})` first.
