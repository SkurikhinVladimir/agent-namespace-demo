# 04 — Create PR from Task

**User:** "Create a PR for TASK-1."

The agent fetches task details to get the branch name, then creates the PR.

## Tool calls

```python
tasks(command="get", args={"id": "TASK-1"})
# → branch: feature/auth, title: Implement auth

git(command="pr", args={"action": "create", "branch": "feature/auth", "title": "Implement auth"})
# → "Pull request PR-4 created: 'Implement auth' from branch 'feature/auth'."
```

## Agent response

> PR-4 created: "Implement auth" from `feature/auth`.

## Notes

Classic two-step chain: gather context first (`tasks.get`), then act (`git.pr create`). The branch name and title come directly from the task, no user input required.
