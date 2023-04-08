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

    def add_node(self, node: Node):
        self.nodes[node.name] = node

    def add_edge(self, edge: Edge):
        self.edges[(edge.source.name, edge.destination.name)] = edge

    def generate_all_edges(self):
        for fromNode in self.nodes.values():
            for toNode in self.nodes.values():
                if fromNode is not toNode and (fromNode.name, toNode.name) not in self.edges:
                    self.edges[
                        (fromNode.name, toNode.name)] = Edge(fromNode, toNode)

    def generate_matrix(self):
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

    #matrix: 'list[list[float]]'

    def get_node_from_matrix(self, index: int) -> Node:
        sorted_nodes = sorted([node.name for node in self.nodes.values()])
        return sorted_nodes[index]

    def get_edge_from_matrix(self, from_index: int, to_index: int) -> Edge:
        sorted_nodes = sorted([node.name for node in self.nodes.values()])
        key = (sorted_nodes[from_index], sorted_nodes[to_index])
        if key in self.edges:
            return self.edges[key]
        else:
            return None

    def init_display(self):
        self.scene = Display.Scene()

    def display_mainloop(self):
        self.scene.mainloop()

    def draw(self):
        self.scene.draw_nodes(self.nodes, self.edges)

    def assign_solve_command(self, command: Callable):
        self.scene.assign_solve_command(command)
