# Tool Namespace Pattern

## The Problem

A typical agent might need 30–50 narrow tools: `list_tasks`, `get_task`, `update_task_state`, `create_pr`, `list_prs`, `merge_pr`, `search_wiki`, `read_wiki_page`, …

This creates problems:
- The LLM must choose from a huge tool list on every step.
- Adding a new sub-command means adding a new tool (schema update, documentation update).
- Related actions are spread across disconnected tools — harder to reason about as a group.

## The Solution

Group related actions under a **namespace tool** with a `command` parameter:

```python
tasks(command="list",   args={"assignee": "me"})
tasks(command="get",    args={"id": "TASK-1"})
tasks(command="save",   args={"id": "TASK-1", "state": "done"})
```

Instead of 50 tools, the agent has 4.

## Help Discovery

The agent doesn't need to know all commands upfront. It can call `args={"help": true}` on any command to get usage:

```python
tasks(command="save", args={"help": True})
# → "save [--id=ID] [--title=TEXT] [--state=STATE]"
```

This lets the agent **discover** available arguments rather than hallucinating them.

## Trade-offs

| Aspect | Narrow tools | Namespace tools |
|--------|-------------|-----------------|
| Tool count | Many | Few |
| Discoverability | Tool name is explicit | Requires help call |
| Schema complexity | Simple per-tool | Richer args dict |
| Extensibility | Add new tool | Add new command to existing tool |
| LLM context usage | Large tool list | Small tool list |

## When to Use

Use namespace tools when:
- You have many related operations (CRUD on a resource).
- Operations share similar argument shapes.
- You want the agent to be able to discover sub-commands dynamically.

Keep narrow tools for:
- Truly unrelated capabilities.
- Tools with very different argument structures.
- Tools the agent must always know about (core capabilities).
