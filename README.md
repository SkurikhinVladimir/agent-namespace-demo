# agent-namespace-demo

Демонстрация паттерна **Tool Namespace** — подхода, при котором агент имеет несколько широких namespace-инструментов вместо десятков узких. Каждый инструмент поддерживает встроенный `help`-механизм, позволяющий агенту самостоятельно узнавать доступные команды и аргументы.

## Быстрый старт

```bash
# 1. Установить зависимости (через uv)
uv sync

# 2. Настроить API-ключ
cp .env.example .env
# Отредактировать .env — вставить LLM_API_KEY

# 3. Запустить интерактивное демо
uv run python demo.py

# 4. Запустить статический демо (без LLM)
uv run python main.py
```

## Инструменты

| Инструмент | Команды | Описание |
|------------|---------|----------|
| `wiki`     | `search`, `read`, `list` | Корпоративная база знаний |
| `tasks`    | `list`, `get`, `save` | Таск-трекер |
| `git`      | `pr`, `issue`, `repo` | Управление репозиторием |
| `skills`   | `list`, `get`, `save`, `delete` | База инструкций для агента |

## Help-механизм

Любой инструмент возвращает справку при `args={"help": true}`:

```python
git(command="pr", args={"help": True})
# → "pr [--action=create|list|merge] [--branch=NAME] [--title=TEXT] ..."
```

## Документация

- [`docs/architecture.md`](docs/architecture.md) — архитектура и диаграммы
- [`docs/namespace-pattern.md`](docs/namespace-pattern.md) — описание паттерна
- [`docs/scenarios/`](docs/scenarios/) — примеры использования

## Структура

```
agent-namespace-demo/
├── agent/
│   ├── graph.py          # LangGraph ReAct граф
│   └── tools/
│       ├── base.py       # NamespaceTool — базовый класс
│       ├── wiki.py       # WikiTool + моки
│       ├── tasks.py      # TasksTool + моки
│       ├── git.py        # GitTool + моки
│       └── skills.py     # SkillsTool + in-memory хранилище
├── docs/
│   ├── architecture.md
│   ├── namespace-pattern.md
│   └── scenarios/
├── demo.py               # Интерактивный демо с реальным LLM
├── main.py               # Статический демо без LLM
└── pyproject.toml
```
