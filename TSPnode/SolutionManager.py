"""SolutionManager is responsible for containing all the usable algorithms."""
from typing import Callable


class SolutionManager():
    """SolutionManager is responsible for containing all the usable algorithms."""

    def __init__(self):
        self.solver_callables: dict[str, Callable] = {}

    def add_command(self, command: Callable, name: str) -> None:
        self.solver_callables[name] = command

    def remove_command(self, name: str) -> Callable:
        return self.solver_callables.pop(name)

    def get_all_command_names(self):
        return self.solver_callables.keys()

    def get_command(self, name: str) -> Callable:
        if name not in self.solver_callables:
            raise Exception(f"Name \"{name}\" not assigned to any command.")
        return self.solver_callables[name]
