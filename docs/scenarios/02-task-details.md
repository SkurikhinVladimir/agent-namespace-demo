# Scenario 02 — Task Details

## User Request

> "Tell me more about TASK-1."

## Steps

1. Agent calls `tasks` with `command="get"` and `id="TASK-1"`.
2. Tool returns full task details including branch name and description.
3. Agent presents the details.

## Tool Calls

```python
tasks(command="get", args={"id": "TASK-1"})
```

## Tool Response

```
ID: TASK-1
Title: Implement auth
State: started
Assignee: me
Branch: feature/auth
Description: Add JWT-based authentication to the API.
```

## Final Agent Response

```
TASK-1: Implement auth
- State: started
- Branch: feature/auth
- Description: Add JWT-based authentication to the API.
```
