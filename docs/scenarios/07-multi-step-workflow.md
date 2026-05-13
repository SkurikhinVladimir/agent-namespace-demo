# 07 — Multi-Step Workflow

**User:** "Starting on TASK-1. Find the deploy docs, open a PR, and move the task to in_review."

## Tool calls

```python
tasks(command="get", args={"id": "TASK-1"})
# → branch: feature/auth, title: Implement auth

wiki(command="search", args={"query": "deploy"})
# → - deploy-guide: Deployment Guide

wiki(command="read", args={"page_id": "deploy-guide"})
# → # Deployment Guide …

git(command="pr", args={"action": "create", "branch": "feature/auth", "title": "Implement auth"})
# → "Pull request PR-4 created."

tasks(command="save", args={"id": "TASK-1", "state": "in_review"})
# → "Task TASK-1 updated."
```

## Agent response

> All set for TASK-1:
> - Deploy guide found in the wiki.
> - PR-4 opened from `feature/auth`.
> - Task moved to in_review.

## Notes

Five tool calls across three different namespace tools, all driven by a single user message. The agent coordinates data from `tasks` → `wiki` → `git` → `tasks` in one ReAct pass.
