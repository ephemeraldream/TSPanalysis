import tkinter as tk
from typing import Callable
from Node import Node
from Edge import Edge


class Scene():
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=300, height=300)

        self.solve_command = None

        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)

        # Add a canvas to the window
        self.canvas.pack()

        # Draw three circles on the canvas
        #canvas.create_oval(50, 50, 150, 150, fill="red")
        #canvas.create_oval(100, 100, 200, 200, fill="green")
        #canvas.create_oval(150, 150, 250, 250, fill="blue")

        solve_button = tk.Button(
            self.window, text="Solve", command=self.run_solve_command)
        solve_button.pack()

        start_node_text = tk.Text(self.window)
        start_node_text.pack()

        # Add a "Quit" button to the window
        quit_button = tk.Button(self.window, text="Quit",
                                command=self.window.quit)
        quit_button.pack()

    def mainloop(self):
        self.window.mainloop()

    def draw_nodes(self, nodes: 'dict[str, Node]', edges: 'dict[tuple[str, str], Edge]'):
        self.canvas.delete('all')
        NODE_SIZE = 20
        edge: Edge
        for edge in edges.values():
            if edge.source.name not in nodes:
                raise Exception(
                    f"Tried to create an edge with a source that does not exist ({edge})")
            if edge.destination.name not in nodes:
                raise Exception(
                    f"Tried to create an edge with a destination that does not exist ({edge})")
            self.canvas.create_line(
                edge.source.x, edge.source.y, edge.destination.x, edge.destination.y)
        node: Node
        for node in nodes.values():
            self.canvas.create_oval(node.x - NODE_SIZE/2, node.y - NODE_SIZE/2,
                                    node.x + NODE_SIZE/2, node.y + NODE_SIZE/2, fill="white")

    def run_solve_command(self):
        if callable(self.solve_command):
            self.solve_command()
        else:
            raise Exception(
                "No callable \"solve_command\" present. Run assign_solve_command(command: Callable) to fix the issue.")

    def assign_solve_command(self, command: Callable):
        self.solve_command = command
