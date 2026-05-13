from abc import ABC, abstractmethod


class NamespaceTool(ABC):
    """Groups related commands under one interface with built-in help discovery."""

    def execute(self, command: str, args: dict[str, object]) -> str:
        if args.get("help"):
            return self._get_help(command)
        return self._execute_command(command, args)

    @abstractmethod
    def _get_help(self, command: str) -> str: ...

    @abstractmethod
    def _execute_command(self, command: str, args: dict[str, object]) -> str: ...
