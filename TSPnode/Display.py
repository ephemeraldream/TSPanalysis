import tkinter as tk
from typing import Callable
from Node import Node
from Edge import Edge


class Scene():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TSP Visual")
        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.canvas.configure(background='white')

        self.run_solve_command = None
        self.solve_commands = None

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
        self.submit_button = tk.Button(form_frame, text="Solve", command=None)
        self.submit_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create the dropdown button
        self.selected_option = tk.StringVar(value="Select Algo")
        self.dropdown_menu = tk.OptionMenu(
            form_frame, self.selected_option, "Select Algo")
        self.dropdown_menu.pack(side=tk.LEFT, padx=5, pady=5)

    def mainloop(self):
        self.window.mainloop()

    def draw_nodes(self, nodes: 'dict[str, Node]', edges: 'dict[tuple[str, str], Edge]'):
        self.canvas.delete('all')
        NODE_SIZE = 26
        edge: Edge
        for edge in edges.values():
            self.canvas.create_line(
                edge.source.x, edge.source.y, edge.destination.x, edge.destination.y, fill="lightgray", width=3)
            # if edge.source.name not in nodes:
            #     raise Exception(
            #         f"Tried to create an edge with a source that does not exist ({edge})")
            # if edge.destination.name not in nodes:
            #     raise Exception(
            #         f"Tried to create an edge with a destination that does not exist ({edge})")
        for edge in edges.values():
            if edge.highlight:
                self.canvas.create_line(
                    edge.source.x, edge.source.y, edge.destination.x, edge.destination.y, fill="black", width=5)
                self.canvas.create_line(
                    edge.source.x, edge.source.y, edge.destination.x, edge.destination.y, fill="red", width=3)
        for edge in edges.values():
            WEIGHT_NODE_SIZE = 15
            if edge.highlight:
                midpoint_x = (edge.source.x + edge.destination.x)/2
                midpoint_y = (edge.source.y + edge.destination.y)/2
                # create text with weight
                self.canvas.create_oval(midpoint_x - NODE_SIZE/2, midpoint_y - NODE_SIZE/2,
                                        midpoint_x + NODE_SIZE/2, midpoint_y + NODE_SIZE/2, fill="white", outline="white")
                self.canvas.create_text(midpoint_x, midpoint_y, text=f"{edge.weight:.1f}", font=("Roboto Thin", 7))
        node: Node
        for node in nodes.values():
            color = None
            if node.highlight:
                color = "red"
            else:
                color = "black"
            self.canvas.create_oval(node.x - NODE_SIZE/2, node.y - NODE_SIZE/2,
                                    node.x + NODE_SIZE/2, node.y + NODE_SIZE/2, fill="white", outline=color, width=4)
            self.canvas.create_text(node.x, node.y, text=node.name)

    def assign_solve_command(self, command: Callable, name: str):
        self.submit_button.configure(command=self.run_solve_command)
        self.dropdown_menu["menu"].add_command(
            label=name, command=tk._setit(self.selected_option, name))
