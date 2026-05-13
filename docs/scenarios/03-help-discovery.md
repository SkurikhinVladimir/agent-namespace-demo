# Scenario 03 — Help Discovery

## User Request

> "Create a PR for the auth work."

## Steps

1. Agent knows the `git` tool exists but is unsure about exact PR arguments.
2. Agent calls `git` with `command="pr"` and `args={"help": true}` to discover the interface.
3. Tool returns usage string.
4. Agent now knows the required arguments and calls `git` again to create the PR.

## Tool Calls

```python
# Step 1: discover arguments
git(command="pr", args={"help": True})

# Step 2: create PR with correct args
git(command="pr", args={"action": "create", "branch": "feature/auth", "title": "Implement auth"})
```

## Tool Responses

**Step 1:**
```
pr [--action=create|list|merge] [--branch=NAME] [--title=TEXT] [--state=open|merged]
```

**Step 2:**
```
Pull request PR-4 created: 'Implement auth' from branch 'feature/auth'.
```

## Final Agent Response

```
Done! PR-4 created: "Implement auth" from branch feature/auth.
```

## Notes

This is the key benefit of the namespace pattern: the agent can **self-document** through help calls instead of requiring the LLM to memorise every argument schema.
