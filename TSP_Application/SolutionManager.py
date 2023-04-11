"""SolutionManager is responsible for containing all the usable algorithms."""
from typing import Callable
import TSP_Application.TSP_Solvers.BruteForceTSP
import TSP_Application.TSP_Solvers.NearestNeighborTSP
import TSP_Application.TSP_Solvers.NearestNeighbor2optTSP
import TSP_Application.TSP_Solvers.SimulatedAnnealing
import TSP_Application.TSP_Solvers.Genetic
import TSP_Application.TSP_Solvers.RL


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

    def add_all_commands(self):
        """Manually add various commands to SolutionManager."""
        # TODO, maybe this should be moved to main?
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
            TSP_Application.TSP_Solvers.Genetic.genetic_algorithm,
            "Genetics")
        self.add_command(
            TSP_Application.TSP_Solvers.RL.ReinforcementLearning,
            "Reinforcement Learning")
