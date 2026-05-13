# Tool Namespace Pattern

## The problem

A typical agent might need 30–50 narrow tools: `list_tasks`, `get_task`, `update_task_state`, `create_pr`, `list_prs`, `merge_pr`, `search_wiki`, `read_wiki_page`, …

Problems:
- The LLM sees a huge tool list in its context on every step.
- Adding a sub-command means registering a new tool — schema changes, doc updates.
- Related operations are spread across disconnected tools.

## The solution

Group related operations under a **namespace tool** with a `command` parameter:

```python
tasks(command="list",  args={"assignee": "me"})
tasks(command="get",   args={"id": "TASK-1"})
tasks(command="save",  args={"id": "TASK-1", "state": "done"})
```

Instead of 50 tools, the agent has 4.

## Help discovery

The agent does not need to memorise argument schemas. Calling `args={"help": true}` returns a short usage string for that command:

```python
tasks(command="save", args={"help": True})
# → "save [--id=ID] [--title=TEXT] [--state=STATE]"
```

The agent can discover the interface at runtime — the same way a developer reads `--help`.

## Trade-offs

| | Narrow tools | Namespace tools |
|---|---|---|
| Tool count in context | Many | Few |
| Argument discoverability | Implicit in schema | Explicit via `help` call |
| Adding a sub-command | New tool registration | New `if command == …` branch |
| LLM context pressure | High | Low |
| Per-command type safety | Strong (typed schema) | Weaker (generic `args: dict`) |

## When to use

**Use namespace tools when:**
- Multiple operations share the same resource (tasks CRUD, PR management).
- Operations have similar argument shapes.
- You want the agent to self-discover sub-commands.

**Keep narrow tools when:**
- Operations are truly unrelated.
- Argument structures are very different.
- Strong per-command type validation is more important than a small tool list.
