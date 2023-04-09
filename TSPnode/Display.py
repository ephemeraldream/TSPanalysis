import tkinter as tk
from typing import Callable
from Node import Node
from Edge import Edge


class Scene():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TSP Visual")
        self.camera_x = 0
        self.camera_y = 0
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.camera_width = 800
        self.camera_height = 600
        self.zoom = 1
        self.canvas = tk.Canvas(
            self.window, width=self.camera_width, height=self.camera_height)
        self.canvas.configure(scrollregion=(0, 0, self.camera_width, self.camera_height), yscrollincrement='1', xscrollincrement='1')
        self.canvas.configure(background='white')

        self.canvas.bind("<MouseWheel>", self.scroll)
        self.canvas.bind("<B1-Motion>", self.drag_camera)
        self.canvas.bind("<ButtonPress>", self.start_drag_camera)
        
        

        self.run_solve_command = None
        self.solve_commands = None

        self.window.protocol("WM_DELETE_WINDOW", self.window.quit)

        # Add a canvas to the window
        self.canvas.pack()
        
        # Create the form at the bottom
        form_frame = tk.Frame(self.window)
        form_frame.pack(side=tk.BOTTOM)
        
        # Create the submit button
        self.submit_button = tk.Button(form_frame, text="Solve", command=None)
        self.submit_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.distance_result = tk.Label(form_frame, text="Hello, world!", width=40)
        self.distance_result.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create the dropdown button
        self.selected_option = tk.StringVar(value="Select Algo")
        self.dropdown_menu = tk.OptionMenu(
            form_frame, self.selected_option, "Select Algo")
        self.dropdown_menu.config(width=30)
        self.dropdown_menu.pack(side=tk.LEFT, padx=5, pady=5)

        self.show_unhighlighted_edges = True
        self.toggle_highlight = tk.Button(form_frame, text="Toggle unhighlighted edges", command=self.toggle_unhighlighted_edges)
        self.toggle_highlight.pack(side=tk.LEFT, padx=5, pady=5)

        

        
        
        self.nodes = None
        self.edges = None

    def mainloop(self):
        self.window.mainloop()
    
    def toggle_unhighlighted_edges(self):
        self.show_unhighlighted_edges = not self.show_unhighlighted_edges
        self.draw_nodes(self.nodes, self.edges)

    def scroll(self, event):
        
        x_pos, _ = self.canvas.xview()
        x_pos *= self.camera_width
        y_pos, _ = self.canvas.yview()
        y_pos *= self.camera_height
        new_x_pos = None
        new_y_pos = None
        offset_x = None
        offset_y = None
        if event.delta > 0:
            # shrink
            if self.zoom < 64:
                self.zoom *= 2
                viewport_width = self.camera_width / self.zoom
                viewport_height = self.camera_height / self.zoom
                offset_x = viewport_width/2
                offset_y = viewport_height/2
                new_x_pos = x_pos + offset_x
                new_y_pos = y_pos + offset_y
            else:
                return
        else:
            # grow
            viewport_width = self.camera_width / self.zoom
            viewport_height = self.camera_height / self.zoom
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
                                            self.camera_width * self.zoom,
                                            self.camera_height * self.zoom))
        
        self.draw_nodes(self.nodes, self.edges)
        self.canvas.xview_moveto(new_x_pos/self.camera_width)
        self.canvas.yview_moveto(new_y_pos/self.camera_height)
        
    def start_drag_camera(self, event):
        if event.state == 0x0008 and event.num == 1:  # Left mouse button
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y
    
    def drag_camera(self, event):
        # Calculate the difference in mouse position since last event
        dx = event.x - self.last_mouse_x
        dy = event.y - self.last_mouse_y
        
        # Update the camera position based on the mouse movement
        #self.camera_x -= dx
        #self.camera_y -= dy
        
        # Redraw the canvas with the updated camera position
        self.canvas.xview_scroll(-dx, "units")
        self.canvas.yview_scroll(-dy, "units")
        
        x_pos, _ = self.canvas.xview()
        y_pos, _ = self.canvas.yview()
        
        # Remember the current mouse position for the next event
        self.last_mouse_x = event.x
        self.last_mouse_y = event.y


    def cam_transform_x(self, x: int):
        return (x) * self.zoom
    def cam_transform_y(self, y: int):
        return (y) * self.zoom
    def draw_nodes(self, nodes: 'dict[str, Node]', edges: 'dict[tuple[str, str], Edge]'):
        self.nodes = nodes
        self.edges = edges

        xt = self.cam_transform_x
        yt = self.cam_transform_y
        
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
        
        

    def assign_solve_command(self, command: Callable, name: str):
        self.submit_button.configure(command=self.run_solve_command)
        self.dropdown_menu["menu"].add_command(
            label=name, command=tk._setit(self.selected_option, name))
