# Scenario 07 — Multi-Step Workflow

## User Request

> "I'm starting on TASK-1. Find the deploy docs, create a PR, and mark the task as in_review."

## Steps

1. Fetch task details to get branch and title.
2. Search wiki for deployment documentation.
3. Create a PR from the task's branch.
4. Update the task state to `in_review`.

## Tool Calls

```python
# Step 1: get task details
tasks(command="get", args={"id": "TASK-1"})

# Step 2: search wiki for deploy docs
wiki(command="search", args={"query": "deploy"})

# Step 3: read the relevant page
wiki(command="read", args={"page_id": "deploy-guide"})

# Step 4: create PR
git(command="pr", args={"action": "create", "branch": "feature/auth", "title": "Implement auth"})

# Step 5: update task state
tasks(command="save", args={"id": "TASK-1", "state": "in_review"})
```

## Tool Responses

**tasks.get:**
```
ID: TASK-1
Title: Implement auth
State: started
Branch: feature/auth
Description: Add JWT-based authentication to the API.
```

**wiki.search:**
```
- deploy-guide: Deployment Guide
```

**wiki.read:**
```
# Deployment Guide
1. Run `make build` to build the Docker image.
2. Push to registry: `make push`.
...
```

**git.pr create:**
```
Pull request PR-4 created: 'Implement auth' from branch 'feature/auth'.
```

**tasks.save:**
```
Task TASK-1 updated.
```

## Final Agent Response

```
All done for TASK-1:
- Found deploy guide in the wiki.
- PR-4 created from branch feature/auth.
- Task state updated to in_review.
```

## Notes

This scenario shows the full ReAct loop across four different tools. The agent coordinates information from `tasks` to drive actions in `git`, while also fetching context from `wiki` — all in a single conversational turn.
