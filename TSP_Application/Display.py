import tkinter as tk
from typing import Callable
from TSP_Application.Node import Node
from TSP_Application.Edge import Edge


class Display():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TSP Visual")

        self._instantiate_canvas()
        self._instantiate_events()
        self._instantiate_bottom_form()
        self._instantiate_solve_button()
        self._instantiate_weight_label()
        self._instantiate_average_label()
        self._instantiate_algorithm_dropdown()
        self._instantiate_highlight_toggle()
        self._instantiate_node_count_box()
        self._instantiate_seed_val_entry()
        
        self.regen_nodes_request = None

    def mainloop(self):
        self.window.mainloop()

    def _instantiate_canvas(self):
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.viewport_width = 800
        self.viewport_height = 600
        self.zoom = 1
        self.canvas = tk.Canvas(
            self.window, width=self.viewport_width, height=self.viewport_height)
        # scroll region allows for panning to be possible
        self.canvas.configure(scrollregion=(
            0, 0, self.viewport_width, self.viewport_height), yscrollincrement='1', xscrollincrement='1')
        self.canvas.configure(background='white')
        self.canvas.pack()

    def _instantiate_events(self):
        self.canvas.bind("<MouseWheel>", self._scroll_event)
        self.canvas.bind("<B1-Motion>", self._drag_camera_event)
        self.canvas.bind("<Button-1>", self._start_drag_camera_event)
        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)

    def _instantiate_bottom_form(self):
        self._form_frame = tk.Frame(self.window)
        self._form_frame.pack(side=tk.BOTTOM)

    def _instantiate_solve_button(self):
        self.submit_button = tk.Button(
            self._form_frame, text="Solve", command=None)
        self.submit_button.pack(side=tk.LEFT, padx=5, pady=5)

    def _instantiate_weight_label(self):
        self.distance_result = tk.Label(
            self._form_frame, text="", width=14, font=("Roboto Thin", 11), anchor="w")
        self.distance_result.pack(side=tk.LEFT, padx=1, pady=5)
    
    def _instantiate_average_label(self):
        self.average_label = tk.Label(
            self._form_frame, text="Average: ", width=20, font=("Roboto Thin", 7), anchor="w")
        self.average_label.pack(side=tk.LEFT, padx=1, pady=5)

    def _instantiate_algorithm_dropdown(self):
        self.selected_option = tk.StringVar(value="Select Algo")
        self.dropdown_menu = tk.OptionMenu(
            self._form_frame, self.selected_option, "Select Algo")
        self.dropdown_menu.config(width=18)
        self.dropdown_menu.pack(side=tk.LEFT, padx=5, pady=5)

    def _instantiate_highlight_toggle(self):
        self.show_unhighlighted_edges = True
        self.toggle_highlight = tk.Button(
            self._form_frame, text="Toggle unhighlighted edges", command=self.toggle_unhighlighted_edges)
        self.toggle_highlight.pack(side=tk.LEFT, padx=5, pady=5)
    
    def _instantiate_node_count_box(self):
        self._default_node_text = tk.StringVar()
        self._default_node_text.set("node count (default 6)")
        def focus_in(event):
            if self._default_node_text.get() == "node count (default 6)":
                self._default_node_text.set("")
                self._node_val_entry.config(foreground="black")
        def focus_out(event):
            if self._default_node_text.get() == "":
                self._default_node_text.set("node count (default 6)")
                self._node_val_entry.config(foreground="gray")
        def on_enter_pressed(event):
            seed = None
            count = None
            try:
                seed=int(self._seed_val_entry.get())
            except: pass
            try:   
                count=int(self._node_val_entry.get())
            except: pass
            self.regen_nodes_request(seed, count)
        self._node_val_entry = tk.Entry(self._form_frame, textvariable=self._default_node_text)
        self._node_val_entry.config(foreground="gray")
        self._node_val_entry.bind("<FocusIn>", focus_in)
        self._node_val_entry.bind("<FocusOut>", focus_out)
        self._node_val_entry.bind("<Return>", on_enter_pressed)
        self._node_val_entry.pack(side=tk.LEFT, padx=5, pady=5)
        
    def _instantiate_seed_val_entry(self):
        self._default_seed_text = tk.StringVar()
        self._default_seed_text.set("seed (default 0)")
        def focus_in(event):
            if self._default_seed_text.get() == "seed (default 0)":
                self._default_seed_text.set("")
                self._seed_val_entry.config(foreground="black")
        def focus_out(event):
            if self._default_seed_text.get() == "":
                self._default_seed_text.set("seed (default 0)")
                self._seed_val_entry.config(foreground="gray")
        def on_enter_pressed(event):
            seed = None
            count = None
            try:
                seed=int(self._seed_val_entry.get())
            except: pass
            try:   
                count=int(self._node_val_entry.get())
            except: pass
            self.regen_nodes_request(seed, count)
        self._seed_val_entry = tk.Entry(self._form_frame, textvariable=self._default_seed_text)
        self._seed_val_entry.config(foreground="gray")
        self._seed_val_entry.bind("<FocusIn>", focus_in)
        self._seed_val_entry.bind("<FocusOut>", focus_out)
        self._seed_val_entry.bind("<Return>", on_enter_pressed)
        self._seed_val_entry.pack(side=tk.LEFT, padx=5, pady=5)
        

    def _scroll_event(self, event):
        x_pos, _ = self.canvas.xview()
        x_pos *= self.viewport_width
        y_pos, _ = self.canvas.yview()
        y_pos *= self.viewport_height
        new_x_pos = None
        new_y_pos = None
        offset_x = None
        offset_y = None
        if event.delta > 0:
            # shrink
            if self.zoom < 64:
                self.zoom *= 2
                viewport_width = self.viewport_width / self.zoom
                viewport_height = self.viewport_height / self.zoom
                offset_x = viewport_width/2
                offset_y = viewport_height/2
                new_x_pos = x_pos + offset_x
                new_y_pos = y_pos + offset_y
            else:
                return
        else:
            # grow
            viewport_width = self.viewport_width / self.zoom
            viewport_height = self.viewport_height / self.zoom
            if self.zoom > 1:
                self.zoom /= 2
                offset_x = viewport_width/2
                offset_y = viewport_height/2
                new_x_pos = x_pos - offset_x
                new_y_pos = y_pos - offset_y
            else:
                return

        # zoom towards center
        self.canvas.configure(scrollregion=(0,
                                            0,
                                            self.viewport_width * self.zoom,
                                            self.viewport_height * self.zoom))

        self.draw_nodes(self.node_cache, self.edge_cache)
        self.canvas.xview_moveto(new_x_pos/self.viewport_width)
        self.canvas.yview_moveto(new_y_pos/self.viewport_height)

    def _start_drag_camera_event(self, event):
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def _drag_camera_event(self, event):
        # Calculate the difference in mouse position since last event
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y

        # Redraw the canvas with the updated camera position
        self.canvas.xview_scroll(-dx, "units")
        self.canvas.yview_scroll(-dy, "units")

        # Remember the current mouse position for the next event
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y

    def _cam_transform_x(self, x: int):
        return x * self.zoom

    def _cam_transform_y(self, y: int):
        return y * self.zoom
    
    def toggle_unhighlighted_edges(self):
        """Toggle whether or not the unhighlighted edges should be rendered.
            (An event will call this function).
        """
        self.show_unhighlighted_edges = not self.show_unhighlighted_edges
        self.draw_nodes(self.node_cache, self.edge_cache)

    def draw_nodes(self, nodes: 'dict[str, Node]', edges: 'dict[tuple[str, str], Edge]'):
        """Draw given nodes and edges. Nodes will be on top, next will be the
            weight text, next the highlighted edges, and finally the
            unhighlighted edges will be drawn.

        Args:
            nodes (dict[str, Node]): Node to draw
            edges (dict[tuple[str, str], Edge]): Edge to draw
        """
        self.node_cache = nodes # cache for quickly redrawing scene when zooming
        self.edge_cache = edges # cache for quickly redrawing scene when zooming

        xt = self._cam_transform_x
        yt = self._cam_transform_y

        self.canvas.delete('all')
        NODE_SIZE = 26
        edge: Edge
        for edge in edges.values():
            esrcx = edge.source.x
            esrcy = edge.source.y
            edstx = edge.destination.x
            edsty = edge.destination.y
            if not edge.highlight and self.show_unhighlighted_edges:
                self.canvas.create_line(
                    xt(esrcx), yt(esrcy), xt(edstx), yt(edsty), fill="lightgray", width=3)
            # if edge.source.name not in nodes:
            #     raise Exception(
            #         f"Tried to create an edge with a source that does not exist ({edge})")
            # if edge.destination.name not in nodes:
            #     raise Exception(
            #         f"Tried to create an edge with a destination that does not exist ({edge})")
        for edge in edges.values():
            esrcx = edge.source.x
            esrcy = edge.source.y
            edstx = edge.destination.x
            edsty = edge.destination.y
            if edge.highlight:
                self.canvas.create_line(
                    xt(esrcx), yt(esrcy),
                    xt(edstx), yt(edsty), fill="black", width=5)
                self.canvas.create_line(
                    xt(esrcx), yt(esrcy),
                    xt(edstx), yt(edsty), fill="red", width=3)
        for edge in edges.values():
            esrcx = edge.source.x
            esrcy = edge.source.y
            edstx = edge.destination.x
            edsty = edge.destination.y
            WEIGHT_NODE_SIZE = 25
            if edge.highlight:
                midpoint_x = (esrcx + edstx)/2
                midpoint_y = (esrcy + edsty)/2
                # create text with weight
                self.canvas.create_oval(xt(midpoint_x) - WEIGHT_NODE_SIZE/2, yt(midpoint_y) - WEIGHT_NODE_SIZE/2,
                                        xt(midpoint_x) + WEIGHT_NODE_SIZE/2, yt(midpoint_y) + WEIGHT_NODE_SIZE/2, fill="white", outline="white")
                self.canvas.create_text(
                    xt(midpoint_x), yt(midpoint_y), text=f"{edge.weight:.1f}", font=("Roboto Thin", 7))
        node: Node
        for node in nodes.values():
            color = None
            if node.highlight:
                color = "red"
            else:
                color = "black"
            self.canvas.create_oval(xt(node.x) - NODE_SIZE/2, yt(node.y) - NODE_SIZE/2,
                                    xt(node.x) + NODE_SIZE/2, yt(node.y) + NODE_SIZE/2, fill="white", outline=color, width=4)
            self.canvas.create_text(
                xt(node.x), yt(node.y), text=node.name)
        self.distance_result

    def assign_solve_options(self, commands_str: 'list[str]'):
        """Set all dropdown options from a given string array.

        Args:
            commands_str (list[str]): A list containing strings which represent
            the names of each algorithm. (Each one should be unique)
        """
        menu = self.dropdown_menu["menu"]
        menu.delete(0, "end")
        for command_str in commands_str:
            menu.add_command(label=command_str, command=tk._setit(
                self.selected_option, command_str))

    def update_average_label(self, new_average: float):
        self.average_label.configure(text=f"Average: {new_average:.2f}")
    
    def remove_average_label(self):
        self.average_label.configure(text="Average:")