# Agent Namespace Demo

4 tools instead of 50. A LangGraph ReAct agent built around the **namespace pattern**: one tool per domain, each with a `help` command for runtime self-discovery.

```
git(command="pr", args={"help": True})
# → "pr [--action=create|list|merge] [--branch=NAME] [--title=TEXT] ..."
```

The agent doesn't need every argument baked into its weights — it reads the interface on demand, exactly like a developer reading a man page.

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

## Tools

| Tool | Commands | Mock data |
|------|----------|-----------|
| `wiki` | `search`, `read`, `list` | 3 static pages |
| `tasks` | `list`, `get`, `save` | 3 tasks (mutable) |
| `git` | `pr`, `issue`, `repo` | PRs / issues / repos (mutable) |
| `skills` | `list`, `get`, `save`, `delete` | 1 pre-seeded skill (mutable) |

## Use Cases

Each file in [`docs/scenarios/`](docs/scenarios/) is a static message history trace — system prompt, user message, assistant tool calls, tool results, final response.

| # | Scenario | Demonstrates |
|---|----------|-------------|
| [01](docs/scenarios/01-list-tasks.md) | List assigned tasks | basic namespace call |
| [02](docs/scenarios/02-task-details.md) | Get task details | chaining context |
| [03](docs/scenarios/03-help-discovery.md) | Agent discovers args via `help` | core pattern |
| [04](docs/scenarios/04-create-pr.md) | Create PR from task ID | multi-tool chain |
| [05](docs/scenarios/05-save-skill.md) | Save a reusable skill | skills tool |
| [06](docs/scenarios/06-reuse-skill.md) | Agent reuses a saved skill | skill-guided execution |
| [07](docs/scenarios/07-multi-step-workflow.md) | Full workflow: task → wiki → PR → update | end-to-end |

## Quickstart

```bash
cp .env.example .env          # set LLM_API_KEY
uv sync
uv run python demo.py         # interactive REPL (requires LLM_API_KEY)
uv run python main.py         # static walkthrough, no API key needed
uv run pytest
```

## Project layout

```
agent-namespace-demo/
├── demo.py                        # interactive REPL entry point
├── main.py                        # static walkthrough entry point
├── pyproject.toml
├── src/
│   └── agent_namespace_demo/
│       ├── config.py              # LLM_API_KEY, LLM_MODEL, LLM_BASE_URL
│       ├── graph.py               # LangGraph ReAct agent
│       ├── repl.py                # interactive REPL
│       ├── static_demo.py
│       └── tools/
│           ├── base.py            # NamespaceTool ABC
│           ├── wiki.py
│           ├── tasks.py
│           ├── git.py
│           └── skills.py
├── tests/
│   ├── test_wiki.py
│   ├── test_tasks.py
│   ├── test_git.py
│   └── test_skills.py
└── docs/
    ├── architecture.md
    ├── namespace-pattern.md
    └── scenarios/                 # 7 message history traces
```
