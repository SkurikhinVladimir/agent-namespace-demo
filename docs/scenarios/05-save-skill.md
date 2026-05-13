# 05 — Save a Skill

**User:** "Save a skill: after a PR is merged, mark the task as done."

## Tool calls

```python
skills(command="save", args={
    "name": "update_task_after_review",
    "description": "Merge PR and mark the task as done",
    "steps": [
        "1. Call git(command='pr', args={'action': 'merge', 'id': PR_ID}).",
        "2. Call tasks(command='save', args={'id': TASK_ID, 'state': 'done'}).",
        "3. Confirm to the user.",
    ],
})
# → "Skill 'update_task_after_review' saved."
```

## Agent response

> Saved skill "update_task_after_review". I'll remember: merge the PR, then mark the task done.

## Notes

A skill is an **instruction for the agent**, not executable code. The agent reads it later with `skills.get` and then follows the steps using normal tools. Skills are only created on explicit user request.
