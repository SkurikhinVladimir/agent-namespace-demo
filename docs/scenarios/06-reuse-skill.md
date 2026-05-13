# Scenario 06 — Reuse a Skill

## User Request

> "TASK-2 PR is approved. Wrap it up."

## Steps

1. Agent recognises a "close out a task" intent and checks available skills.
2. Agent finds the `update_task_after_review` skill and reads it.
3. Agent follows the skill steps: merges the PR and updates the task state.

## Tool Calls

```python
# Check available skills
skills(command="list", args={})

# Read the relevant skill
skills(command="get", args={"name": "update_task_after_review"})

# Follow step 1: merge the PR
git(command="pr", args={"action": "merge", "id": "PR-2"})

# Follow step 2: mark task as done
tasks(command="save", args={"id": "TASK-2", "state": "done"})
```

## Tool Responses

**skills.list:**
```
- create_pr_for_task: Create a pull request from a task ID
- update_task_after_review: Update task state to done after PR is merged
```

**skills.get:**
```
Skill: update_task_after_review
Description: Update task state to done after PR is merged
Steps:
1. Call git(command='pr', args={'action': 'merge', 'id': PR_ID}).
2. Call tasks(command='save', args={'id': TASK_ID, 'state': 'done'}).
3. Confirm to the user.
```

**git.pr merge:**
```
Pull request PR-2 merged.
```

**tasks.save:**
```
Task TASK-2 updated.
```

## Final Agent Response

```
Done! PR-2 merged and TASK-2 marked as done.
```
