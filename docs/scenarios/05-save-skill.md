# Scenario 05 — Save a Skill

## User Request

> "Save a skill: after a PR is merged, update the task state to done."

## Steps

1. User describes the skill in natural language.
2. Agent structures it as a skill and saves it via `skills(command="save", ...)`.

## Tool Calls

```python
skills(command="save", args={
    "name": "update_task_after_review",
    "description": "Update task state to done after PR is merged",
    "steps": [
        "1. Call git(command='pr', args={'action': 'merge', 'id': PR_ID}).",
        "2. Call tasks(command='save', args={'id': TASK_ID, 'state': 'done'}).",
        "3. Confirm to the user.",
    ],
})
```

## Tool Response

```
Skill 'update_task_after_review' saved.
```

## Final Agent Response

```
Skill saved: "update_task_after_review" — I'll remember to merge the PR and mark the task done.
```

## Notes

Skills are **instructions for the agent**, not executable objects. The agent reads a skill later with `skills(command="get", ...)` and then follows the steps using normal tools. Skills are only created on explicit user request.
