"""SolutionManager is responsible for containing all the usable algorithms."""
from typing import Callable
import TSP_Application.TSP_Solvers.BruteForceTSP
import TSP_Application.TSP_Solvers.NearestNeighborTSP
import TSP_Application.TSP_Solvers.NearestNeighbor2optTSP
import TSP_Application.TSP_Solvers.SimulatedAnnealing
import TSP_Application.TSP_Solvers.RL
import TSP_Application.TSP_Solvers.AntColony


class SolutionManager():
    """SolutionManager is responsible for containing all the usable algorithms."""

    def __init__(self):
        self.solver_callables: dict[str, Callable] = {}

    def add_command(self, command: Callable, name: str) -> None:
        """Add a command to the SolutionManager.

        Args:
            command (Callable): A Python Callable function to store into command.
            name (str): A name/alias that will refer to an added command.
        """
        self.solver_callables[name] = command

    def remove_command(self, name: str) -> Callable:
        """Remove a command.

        Args:
            name (str): Look for a function with this name and remove it.

        Returns:
            Callable: The removed command.
        """
        return self.solver_callables.pop(name)

    def get_all_command_names(self) -> 'list[str]':
        return self.solver_callables.keys()

    def get_command(self, name: str) -> Callable:
        if name not in self.solver_callables:
            raise Exception(f"Name \"{name}\" not assigned to any command.")
        return self.solver_callables[name]

    def add_all_commands(self) -> None:
        """Manually add various commands."""
        self.add_command(
            TSP_Application.TSP_Solvers.BruteForceTSP.solve,
            "Brute force")
        self.add_command(
            TSP_Application.TSP_Solvers.NearestNeighborTSP.solve,
            "Nearest Neighbor")
        self.add_command(
            TSP_Application.TSP_Solvers.NearestNeighbor2optTSP.solve,
            "Nearest Neighbor (2-opt)")
        self.add_command(
            TSP_Application.TSP_Solvers.SimulatedAnnealing.simulated_annealing,
            "Simulated Annealing")
        self.add_command(
            TSP_Application.TSP_Solvers.RL.ReinforcementLearning,
            "Reinforcement Learning")
        self.add_command(
            TSP_Application.TSP_Solvers.AntColony.solve,
            "Ant Colony")
