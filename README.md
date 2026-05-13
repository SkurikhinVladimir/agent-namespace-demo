# agent-namespace-demo

A demonstration of the **Tool Namespace Pattern** — a LangGraph agent that uses four broad namespace tools instead of dozens of narrow ones. Each tool exposes a `command` parameter and a built-in `help` mechanism so the agent can discover available sub-commands at runtime.

## How it works

```
User message
     │
     ▼
┌─────────────────────────────────────────────────┐
│  LangGraph ReAct Agent                          │
│                                                 │
│  wiki(command, args)   tasks(command, args)     │
│  git(command, args)    skills(command, args)    │
│                                                 │
│  Any command accepts args={"help": true}        │
│  → returns usage string for self-discovery      │
└─────────────────────────────────────────────────┘
```

Instead of 50 narrow tools, the agent has 4. When it is unsure about arguments, it calls `help` first and then acts — exactly like a developer reading a man page.

## Scenarios

The [`docs/scenarios/`](docs/scenarios/) directory walks through concrete agent dialogues:

| # | Scenario | Demonstrates |
|---|----------|-------------|
| [01](docs/scenarios/01-list-tasks.md) | List assigned tasks | basic namespace call |
| [02](docs/scenarios/02-task-details.md) | Get task details | chaining context |
| [03](docs/scenarios/03-help-discovery.md) | Agent discovers args via `help` | core pattern |
| [04](docs/scenarios/04-create-pr.md) | Create PR from task ID | multi-tool chain |
| [05](docs/scenarios/05-save-skill.md) | Save a reusable skill | skills tool |
| [06](docs/scenarios/06-reuse-skill.md) | Agent reuses a saved skill | skill-guided execution |
| [07](docs/scenarios/07-multi-step-workflow.md) | Full workflow: task → wiki → PR → update | end-to-end |

## Tools

| Tool | Commands | Mock data |
|------|----------|-----------|
| `wiki` | `search`, `read`, `list` | 3 static pages |
| `tasks` | `list`, `get`, `save` | 3 tasks (mutable) |
| `git` | `pr`, `issue`, `repo` | PRs / issues / repos (mutable) |
| `skills` | `list`, `get`, `save`, `delete` | 1 pre-seeded skill (mutable) |

Every command supports `args={"help": true}`:
```python
git(command="pr", args={"help": True})
# → "pr [--action=create|list|merge] [--branch=NAME] [--title=TEXT] ..."
```

## Quickstart

```bash
cp .env.example .env          # set LLM_API_KEY
uv sync
uv run python demo.py         # interactive REPL (requires LLM_API_KEY)
uv run python main.py         # static walkthrough, no API key needed
uv run pytest                 # run tests
```

## Project layout

```
src/agent_namespace_demo/
├── config.py          # Pydantic Settings (LLM_API_KEY, LLM_MODEL, …)
├── graph.py           # builds LangGraph ReAct agent — dependencies injected
├── repl.py            # interactive REPL logic
├── static_demo.py     # static scenario runner
└── tools/
    ├── base.py        # NamespaceTool ABC
    ├── wiki.py
    ├── tasks.py
    ├── git.py
    └── skills.py
tests/                 # pytest, one file per tool
docs/
├── architecture.md    # component diagram + ReAct loop
├── namespace-pattern.md
└── scenarios/         # 7 annotated dialogue examples
demo.py                # entry point — wires deps, starts REPL
main.py                # entry point — wires deps, runs static demo
```

## Further reading

- [Architecture](docs/architecture.md) — component diagram, ReAct loop, design decisions
- [Namespace Pattern](docs/namespace-pattern.md) — motivation, trade-offs, when to use
