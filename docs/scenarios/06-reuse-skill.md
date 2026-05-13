# 06 — Reuse a Skill

**User:** "TASK-2 PR got approved. Wrap it up."

The agent recognises a "close out" intent, checks available skills, finds the relevant one, and follows its steps.

## Tool calls

```python
skills(command="list", args={})
# → - create_pr_for_task: ...
#   - update_task_after_review: Merge PR and mark the task as done

skills(command="get", args={"name": "update_task_after_review"})
# → Steps:
#   1. Call git(command='pr', args={'action': 'merge', 'id': PR_ID}).
#   2. Call tasks(command='save', args={'id': TASK_ID, 'state': 'done'}).
#   3. Confirm to the user.

git(command="pr", args={"action": "merge", "id": "PR-2"})
# → "Pull request PR-2 merged."

tasks(command="save", args={"id": "TASK-2", "state": "done"})
# → "Task TASK-2 updated."
```

## Agent response

> Done — PR-2 merged and TASK-2 marked as done.
