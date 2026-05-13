# Scenario 04 — Create PR from Task

## User Request

> "Create a PR for TASK-1."

## Steps

1. Agent fetches task details to get the branch name and title.
2. Agent uses that information to create a PR via the `git` tool.

## Tool Calls

```python
# Get task info
tasks(command="get", args={"id": "TASK-1"})

# Create PR using task's branch and title
git(command="pr", args={"action": "create", "branch": "feature/auth", "title": "Implement auth"})
```

## Tool Responses

**tasks.get:**
```
ID: TASK-1
Title: Implement auth
State: started
Assignee: me
Branch: feature/auth
Description: Add JWT-based authentication to the API.
```

**git.pr create:**
```
Pull request PR-4 created: 'Implement auth' from branch 'feature/auth'.
```

## Final Agent Response

```
PR-4 created: "Implement auth" from branch feature/auth.
```

## Notes

The agent chains two tool calls: first gathers context (task details), then acts (creates PR). This is a common pattern when the action requires data from a previous step.
