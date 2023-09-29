"""Application is in charge of handling the SolutuionManager, NodeManager,
    and the Display, acting as a communication bridge between the three. 
    It is also responsible for all the event handling of the application.
    """
from TSP_Application.MatrixToolsTSP import display_solution
from TSP_Application.Display import Display
from TSP_Application.NodeManager import NodeManager
from TSP_Application.SolutionManager import SolutionManager
from TSP_Application.MatrixToolsTSP import calculate_circuit_cost
import threading


class TSPApplication:
    """Application is in charge of handling the SolutuionManager, NodeManager,
        and the Display, acting as a communication bridge between the three. 
        It is also responsible for all the event handling of the application.
    """

    def __init__(self):
        # prepare needed instances
        self.display = Display()
        self.node_manager = NodeManager()
        self.solution_manager = SolutionManager()

        # prepare extra data
        self.seed = 0
        self.node_count = 6
        self.last_command = None
        self.solve_count = 0
        self.average = 0
        self.currently_solving = False

        # prepare event handling of solver functions
        self.solution_manager.add_all_commands()
        self.display.assign_solve_options(
            self.solution_manager.get_all_command_names())
        self.display.submit_button.configure(command=self.solve_button_event)
        self.display.regen_nodes_request = self.handle_regen_nodes_request

        # generate and draw nodes
        self.generate_nodes(self.seed, self.node_count)
        self.draw_nodes()

    def enter_mainloop(self) -> None:
        """Begin mainloop, this will hand over execution to tkinter.
            This means that from now on, receiving execution must be done
            through user events.
        """
        self.display.mainloop()

    def generate_nodes(self, seed: int, count: int) -> None:
        """Generate fresh new nodes onto the graph.

        Args:
            seed (int): An int which will be fed into the randomizer to provide
            consistant nodes for debugging.
            count (int): A count of how many nodes to generate (does not affect
            placement of previous nodes).
        """
        self.node_manager.delete_all_nodes()
        if self.node_count > 16:
            self.display.show_unhighlighted_edges = False
        else:
            self.display.show_unhighlighted_edges = True
        self.node_manager.generate_random_graph(seed, count)

    def draw_nodes(self) -> None:
        """Draw nodes and edges to the canvas of display using available
            NodeManager data.
        """
        self.display.draw_nodes(self.node_manager.nodes,
                                self.node_manager.edges)

    def solve_button_event(self) -> None:
        """Event function that will get called on a "press solve button"
            event. Afterwards execute the solution function selected by the
            user. Finally, highlight the solution on the canvas.
        """
        if (self.currently_solving == True and self.display.selected_option.get() != None):
            return
        self.currently_solving = True
        solvingThread = threading.Thread(
            target=self.solve_thread, args=(), kwargs={})
        solvingThread.start()

    def solve_thread(self) -> None:
        """Event function that will get called on a "press solve button"
            event. Afterwards execute the solution function selected by the
            user. Finally, highlight the solution on the canvas. (this method
            is the other half of solve_button_event() but is threaded)
        """
        solve_func = self.solution_manager.get_command(
            self.display.selected_option.get())
        if solve_func != self.last_command:
            self.average = 0
            self.solve_count = 0
            self.display.remove_average_label()
        path = solve_func(self.node_manager)
        cost = calculate_circuit_cost(
            self.node_manager.generate_matrix(), path)
        self.solve_count += 1
        self.average = (self.average * (self.solve_count - 1) +
                        cost)/self.solve_count
        self.last_command = solve_func
        self.display.update_average_label(self.average)
        self.highlight_solution(path)
        self.currently_solving = False

    def highlight_solution(self, path: 'list[int]') -> None:
        """Highlight a given solution to the canvas.

        Args:
            path (list): A path of indices with each index representing a node
            (which is handled and translated by node manager). The path
            generally shouldn't have the start and end be the same node because
            it is assumed that the end node will connect back to the start node
            (because it represents a circuit).
        """
        cost = calculate_circuit_cost(
            self.node_manager.generate_matrix(), path)
        display_solution(
            self.node_manager, self.display, path, cost)

    def handle_regen_nodes_request(self, seed: int = None, count: int = None):
        """User event for regenerating nodes incase the user changes the seed
        or count parameters.

        Args:
            seed (int, optional): Seed replaced if a new one is provided,
            else use the old one. Defaults to None.
            count (int, optional): Count replaced if a new one is provided,
            else use the old one. Defaults to None.
        """
        if isinstance(seed, int):
            self.seed = seed
        if isinstance(count, int):
            self.node_count = count

        # should reset averages
        self.average = 0
        self.solve_count = 0

        self.generate_nodes(self.seed, self.node_count)
        self.draw_nodes()
    pass
