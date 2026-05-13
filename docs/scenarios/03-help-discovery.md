# 03 — Help Discovery

**User:** "Create a PR for the auth work."

The agent knows the `git` tool exists but is unsure of the exact PR arguments. It calls `help` first.

## Tool calls

```python
# Step 1 — discover the interface
git(command="pr", args={"help": True})
# → "pr [--action=create|list|merge] [--branch=NAME] [--title=TEXT] [--id=ID] [--state=open|merged]"

# Step 2 — act with correct arguments
git(command="pr", args={"action": "create", "branch": "feature/auth", "title": "Implement auth"})
# → "Pull request PR-4 created: 'Implement auth' from branch 'feature/auth'."
```

## Agent response

> Done — PR-4 created: "Implement auth" from branch `feature/auth`.

## Why this matters

This is the core benefit of the namespace pattern: the agent can **self-document** through a `help` call instead of needing every argument baked into the LLM's weights.
