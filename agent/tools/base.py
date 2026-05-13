from abc import ABC, abstractmethod


class NamespaceTool(ABC):
    """Base class for namespace tools with built-in help discovery."""

    @abstractmethod
    def _get_help(self, command: str) -> str:
        """Return help text for a command."""

    @abstractmethod
    def _execute_command(self, command: str, args: dict) -> str:
        """Execute a command with the given args."""

    def execute(self, command: str, args: dict) -> str:
        if args.get("help"):
            return self._get_help(command)
        return self._execute_command(command, args)
