# Architecture

## Component diagram

```
demo.py / main.py  (composition root)
    │
    ├── Settings          (pydantic-settings, reads .env)
    ├── WikiTool          (mock pages)
    ├── TasksTool         (mutable mock tasks)
    ├── GitTool           (mutable mock PRs / issues / repos)
    ├── SkillsTool        (mutable in-memory skills store)
    │
    └── build_agent(settings, wiki, tasks, git, skills)
            │
            ├── ChatOpenAI        (langchain-openai)
            └── create_react_agent (langgraph)
                    │
                    └── [wiki_tool, tasks_tool, git_tool, skills_tool]
                            (closures — capture injected instances)
```

## ReAct loop

```
User message
    │
    ▼
Agent reasons → calls tool(command, args)
    │
    ├─ args.help == true? → return usage string
    │
    └─ dispatch to command handler
            │
            └─ return result string
                    │
                    ▼
            Agent observes, reasons again
                    │
                    └─ no more tools needed → final response
```

## Key design decisions

**Dependency injection at composition root.**
Tools are instantiated in `demo.py` / `main.py` and passed into `build_agent`. The tools themselves have no knowledge of the LLM or LangGraph. This makes them independently testable.

**Closures as LangChain tools.**
`build_agent` defines `@tool`-decorated functions as closures that capture injected tool instances. This avoids module-level singletons (global mutable state).

**`NamespaceTool` ABC.**
All tools share a single `execute(command, args)` entry point. The `help` check lives in the base class — concrete tools only implement `_get_help` and `_execute_command`.

**All config via Pydantic Settings.**
`Settings` validates environment variables at startup. Missing `LLM_API_KEY` fails immediately with a clear error, not at the first LLM call.

**Mock data is module-level constants.**
`_SEED` dicts are constants (never mutated). Instance state is initialised with `deepcopy(_SEED)` so each `TasksTool()` / `GitTool()` / `SkillsTool()` starts from the same known state and is isolated from other instances.
