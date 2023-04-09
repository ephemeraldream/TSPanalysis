import math
import Display
from Node import Node
from Edge import Edge
from typing import Callable


class NodeManager:
    def __init__(self):
        self.nodes: dict[str, Node] = dict()
        self.edges: dict[tuple[str, str], Edge] = dict()
        self.scene: Display.Scene
        self.solve_commands: dict[str, Callable] = {"Select Algo": None}
        self.best_solution_weight: float = -1

    # add a node to the NodeManager
    def add_node(self, node: Node):
        self.nodes[node.name] = node

    # add an edge to the NodeManager
    def add_edge(self, edge: Edge):
        self.edges[(edge.source.name, edge.destination.name)] = edge

    # generate all possible edges between all nodes if not already existing
    def generate_all_edges(self):
        for fromNode in self.nodes.values():
            for toNode in self.nodes.values():
                if fromNode is not toNode and (fromNode.name, toNode.name) not in self.edges:
                    self.edges[
                        (fromNode.name, toNode.name)] = Edge(fromNode, toNode)

    # generate a matrix with the rows being source (along the y axis) and columns being the
    # destination (along the x axis). Each cell contains the weight/destination to the other node.
    def generate_matrix(self) -> 'list[list[float]]':
        sorted_nodes = sorted([node.name for node in self.nodes.values()])
        edge_matrix = [None]*len(sorted_nodes)
        for y in range(len(sorted_nodes)):
            row = [math.inf]*len(sorted_nodes)
            for x in range(len(sorted_nodes)):
                fromNode = sorted_nodes[y]
                toNode = sorted_nodes[x]
                if fromNode == toNode:
                    row[x] = 0
                if (fromNode, toNode) in self.edges:
                    row[x] = self.edges.get((fromNode, toNode)).weight
                pass
            edge_matrix[y] = row
        return edge_matrix

    # convert the index into the node it represents
    def get_node_from_matrix(self, index: int) -> Node:
        sorted_nodes = sorted([node.name for node in self.nodes.values()])
        return sorted_nodes[index]

    # convert an index pair into the edge it represents
    def get_edge_from_matrix(self, from_index: int, to_index: int) -> Edge:
        sorted_nodes = sorted([node.name for node in self.nodes.values()])
        key = (sorted_nodes[from_index], sorted_nodes[to_index])
        if key in self.edges:
            return self.edges[key]
        else:
            return None

    # initialize the display by preparing the window (mainloop is needed for the window to show up)
    def init_display(self):
        self.scene = Display.Scene()
        self.scene.run_solve_command = self.run_solve_command
        self.scene.solve_commands = self.solve_commands

    # begin the tkinter display mainloop (note: execution is permanently kept by the display at this point.
    # Use event hooks to receive execute commands)
    def display_mainloop(self):
        self.scene.mainloop()

    # draw/redraw all the node elements
    def draw(self):
        self.scene.draw_nodes(self.nodes, self.edges)

    # pass in your custom function to be executed when a user clicks the "solve" button
    def assign_solve_command(self, name: str, command: Callable):
        self.scene.assign_solve_command(name, command)
    
    def run_solve_command(self):
        solve_command = self.solve_commands[self.scene.selected_option.get()]
        if callable(solve_command):
            solve_command(self)
        else:
            raise Exception(
                "No callable \"solve_command\" present. Run assign_solve_command(command: Callable) to fix the issue.")
    
    def assign_solve_command(self, command: Callable, name: str):
        self.solve_commands[name] = command
        #self.selected_option.set(name)
        self.scene.assign_solve_command(command, name)
    
    def generate_graph(self, coordinates: 'list[tuple]', length=-1):
        name = ord('a')
        overflow = 0
        for coordinate in coordinates:
            overflow_char = ''
            if name == 123:
                overflow += 1
                overflow_char = str(overflow)
            else:
                name += 1
            self.add_node(Node(coordinate[0], coordinate[1], chr(name) + overflow_char))
            length -= 1
            if length == 0:
                break
        self.generate_all_edges()
    
    def highlight_path(self, path: 'list[int]'):
        node_names = [self.get_node_from_matrix(index) for index in path]
        print(node_names)
        for i in range(len(node_names) - 1):
            self.nodes[node_names[i]].highlight = True
            self.edges[(node_names[i],node_names[i+1])].highlight = True
        if node_names[len(node_names) - 1] is not node_names[0]:
            self.nodes[node_names[len(node_names) - 1]].highlight = True
            self.edges[node_names[len(node_names) - 1], node_names[0]].highlight = True
        
    def unhighligh_all(self):
        for node in self.nodes.values():
            node.highlight = False
        for edge in self.edges.values():
            edge.highlight = False
            
