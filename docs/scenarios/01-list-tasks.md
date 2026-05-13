# 01 — List Tasks

**User:** "What tasks are assigned to me?"

## Tool calls

```python
tasks(command="list", args={"assignee": "me"})
```

**Result:**
```
- TASK-1: Implement auth (started)
- TASK-2: Fix bug in API (in_review)
```

## Agent response

> You have 2 tasks: TASK-1 "Implement auth" (started) and TASK-2 "Fix bug in API" (in_review).

## Notes

The agent infers `assignee="me"` from context. If it were unsure of the field name, it would call `tasks(command="list", args={"help": true})` first.
