"""Application is in charge of handling the SolutuionManager, NodeManager,
    and the Display, acting as a communication bridge between the three. 
    It is also responsible for all the event handling of the application.
    """
from Display import Display
from NodeManager import NodeManager
from SolutionManager import SolutionManager
import NearestNeighborTSP
import BruteForceTSP
import MatrixToolsTSP
import SimulatedAnnealing
import MatrixToolsTSP


class TSPApplication:
    """Application is in charge of handling the SolutuionManager, NodeManager,
        and the Display, acting as a communication bridge between the three. 
        It is also responsible for all the event handling of the application.
    """

    def __init__(self):
        self.display = Display()
        self.node_manager = NodeManager()
        self.solution_manager = SolutionManager()

        self.add_all_commands()
        self.display.assign_solve_options(
            self.solution_manager.get_all_command_names())
        self.display.submit_button.configure(command=self.solve_button_event)

        self.node_manager.generate_random_graph(0, 6)

        self.draw_nodes()

    def enter_mainloop(self):
        """Begin mainloop, this will hand over execution to tkinter.
            This means that from now on, receiving execution must be done
            through user events.
        """
        self.display.mainloop()

    def draw_nodes(self):
        """Draw nodes and edges to the canvas of display using available
            NodeManager data.
        """
        self.display.draw_nodes(self.node_manager.nodes,
                                self.node_manager.edges)

    def add_all_commands(self):
        """Manually add various commands to SolutionManager."""
        # TODO, maybe this should be moved to main?
        self.solution_manager.add_command(
            NearestNeighborTSP.solve, "Nearest Neighbor")
        self.solution_manager.add_command(
            BruteForceTSP.solve, "Brute force")
        self.solution_manager.add_command(
            SimulatedAnnealing.simulated_annealing, "Simulated Annealing")

    def solve_button_event(self):
        """Event function that will get called on a "press solve button"
            event. Afterwards execute the solution function selected by the
            user. Finally, highlight the solution on the canvas.
        """
        solve_func = self.solution_manager.get_command(
            self.display.selected_option.get())
        path = solve_func(self.node_manager)
        self.highlight_solution(path)

    def highlight_solution(self, path: 'list[int]'):
        """Highlight a given solution to the canvas.

        Args:
            path (list): A path of indices with each index representing a node
            (which is handled and translated by node manager). The path
            generally shouldn't have the start and end be the same node because
            it is assumed that the end node will connect back to the start node
            (because it represents a circuit).
        """
        cost = MatrixToolsTSP.calculate_circuit_cost(
            self.node_manager.generate_matrix(), path)
        MatrixToolsTSP.display_solution(
            self.node_manager, self.display, path, cost)

    pass
