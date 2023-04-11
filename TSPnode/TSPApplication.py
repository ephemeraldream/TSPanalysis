"""Application is in charge of handling the SolutuionManager, NodeManager,
    and the Display, acting as a communication bridge between the three. 
    It is also responsible for all the event handling of the application.
    """
from Display import Display
from NodeManager import NodeManager
from SolutionManager import SolutionManager
import BruteForceTSP
import NearestNeighborTSP
import NearestNeighbor2optTSP
import MatrixToolsTSP
import SimulatedAnnealing
import MatrixToolsTSP
import Genetic
import RL

class TSPApplication:
    """Application is in charge of handling the SolutuionManager, NodeManager,
        and the Display, acting as a communication bridge between the three. 
        It is also responsible for all the event handling of the application.
    """
    

    def __init__(self):
        self.display = Display()
        self.node_manager = NodeManager()
        self.solution_manager = SolutionManager()
        
        self.seed = 0
        self.node_count = 6
        self.last_command = None
        self.solve_count = 0
        self.average = 0

        self.add_all_commands()
        self.display.assign_solve_options(
            self.solution_manager.get_all_command_names())
        self.display.submit_button.configure(command=self.solve_button_event)
        self.display.regen_nodes_request = self.handle_regen_nodes_request

        self.generate_nodes(self.seed, self.node_count)

        self.draw_nodes()

    def enter_mainloop(self):
        """Begin mainloop, this will hand over execution to tkinter.
            This means that from now on, receiving execution must be done
            through user events.
        """
        self.display.mainloop()
    
    def generate_nodes(self, seed: int, count: int):
        self.node_manager.delete_all_nodes()
        if self.node_count > 16:
            self.display.show_unhighlighted_edges = False
        else:
            self.display.show_unhighlighted_edges = True
        self.node_manager.generate_random_graph(seed, count)

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
            BruteForceTSP.solve, "Brute force")
        self.solution_manager.add_command(
            NearestNeighborTSP.solve, "Nearest Neighbor")
        self.solution_manager.add_command(
            NearestNeighbor2optTSP.solve, "Nearest Neighbor (2-opt)"
        )
        
        self.solution_manager.add_command(
            SimulatedAnnealing.simulated_annealing, "Simulated Annealing")
        self.solution_manager.add_command(Genetic.genetic_algorithm, "Genetics")
        self.solution_manager.add_command(RL.ReinforcementLearning, "Reinforcement Learning")

    def solve_button_event(self):
        """Event function that will get called on a "press solve button"
            event. Afterwards execute the solution function selected by the
            user. Finally, highlight the solution on the canvas.
        """
        solve_func = self.solution_manager.get_command(
            self.display.selected_option.get())
        if solve_func != self.last_command:
            self.average = 0
            self.solve_count = 0
            self.display.remove_average_label()
        path = solve_func(self.node_manager)
        cost = MatrixToolsTSP.calculate_circuit_cost(self.node_manager.generate_matrix(), path)
        self.solve_count += 1
        self.average = (self.average * (self.solve_count - 1) + cost)/self.solve_count
        self.last_command = solve_func
        self.display.update_average_label(self.average)
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

    def handle_regen_nodes_request(self, seed: int = None, count: int = None):
        if isinstance(seed, int):
            self.seed = seed
        if isinstance(count, int):
            self.node_count = count
            
        self.generate_nodes(self.seed, self.node_count)
        self.draw_nodes()
    pass
