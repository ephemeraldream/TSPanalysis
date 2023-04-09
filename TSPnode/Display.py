import tkinter as tk
from typing import Callable
from Node import Node
from Edge import Edge


class Scene():
    def __init__(self):
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.SOLVE_OPTIONS = ["Heuristic/Naive", "Option 2", "Option 3"]
        self.solve_command = None

        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)

        # Add a canvas to the window
        self.canvas.pack()
        
        # Create the form at the bottom
        form_frame = tk.Frame(self.window)
        form_frame.pack(side=tk.BOTTOM)

        # Create the two text boxes
        text_box1 = tk.Entry(form_frame, width=10)
        text_box1.pack(side=tk.LEFT, padx=5, pady=5)
        text_box2 = tk.Entry(form_frame, width=10)
        text_box2.pack(side=tk.LEFT, padx=5, pady=5)

        # Create the submit button
        submit_button = tk.Button(form_frame, text="Solve", command=self.run_solve_command)
        submit_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create the dropdown button
        selected_option = tk.StringVar(value=self.SOLVE_OPTIONS[0])
        dropdown_menu = tk.OptionMenu(form_frame, selected_option, *self.SOLVE_OPTIONS)
        dropdown_menu.pack(side=tk.LEFT, padx=5, pady=5)

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
            color = None
            if edge.highlight:
                color = "red"
            else:
                color = "black"
            self.canvas.create_line(
                edge.source.x, edge.source.y, edge.destination.x, edge.destination.y, fill=color)
        node: Node
        for node in nodes.values():
            color = None
            if node.highlight:
                color = "red"
            else:
                color = "black"
            self.canvas.create_oval(node.x - NODE_SIZE/2, node.y - NODE_SIZE/2,
                                    node.x + NODE_SIZE/2, node.y + NODE_SIZE/2, fill="white", outline=color)
            self.canvas.create_text(node.x, node.y, text=node.name)

    def run_solve_command(self):
        if callable(self.solve_command):
            self.solve_command()
        else:
            raise Exception(
                "No callable \"solve_command\" present. Run assign_solve_command(command: Callable) to fix the issue.")

    def assign_solve_command(self, command: Callable):
        self.solve_command = command
