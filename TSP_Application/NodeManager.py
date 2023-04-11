"""NodeManager is in charge of maintaining all the nodes and edges to nodes.
    Its primary goal is storing all nodes and edges and passing the data along to
    either the display, or into matrix form for the Travelling Ssalesman Problem
    solvers. This class will exclusively contain 3 types of behaviors: Store and
    access nodes/edges, convert from nodes/edges to their matrix form, and
    communicate to the display about the nodes/edges.
    """
import math
from TSP_Application.Node import Node
from TSP_Application.Edge import Edge
from typing import Callable
import random


class NodeManager:
    """A manager for containing and converting Node and Edge data."""
    def __init__(self):
        self.nodes: dict[str, Node] = dict()
        self.edges: dict[tuple[str, str], Edge] = dict()
        self.solve_commands: dict[str, Callable] = {"Select Algo": None}
        self.best_solution_weight: float = -1
        self.matrix_cache = None

    # add a node to the NodeManager
    def add_node(self, node: Node):
        """Add a given node.

        Args:
            node (Node): A node object.
        """
        self.nodes[node.name] = node
        self.matrix_cache = None

    # add an edge to the NodeManager
    def add_edge(self, edge: Edge):
        """Add a given edge.

        Args:
            edge (Edge): An edge object.
        """
        self.edges[(edge.source.name, edge.destination.name)] = edge
        self.matrix_cache = None

    # generate all possible edges between all nodes if not already existing
    def generate_all_edges(self):
        """Generate edges from every node to every other node."""
        for fromNode in self.nodes.values():
            for toNode in self.nodes.values():
                if fromNode is not toNode and (fromNode.name, toNode.name) not in self.edges:
                    self.edges[
                        (fromNode.name, toNode.name)] = Edge(fromNode, toNode)
        self.matrix_cache = None

    # generate a matrix with the rows being source (along the y axis) and columns being the
    # destination (along the x axis). Each cell contains the weight/destination to the other node.
    def generate_matrix(self) -> 'list[list[float]]':
        """Convert the nodes and edges into an edge matrix format. Due to an
        internal cache this method can be repeatively called with 0 performance
        loss.

        Returns:
            list[list[float]]: A reference to the generated edge matrix (should
            not be modified, assume it is immutable)
        """
        if self.matrix_cache is not None:
            return self.matrix_cache
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
            edge_matrix[y] = row
        
        self.matrix_cache = edge_matrix
        return edge_matrix

    def get_node_from_matrix(self, index: int) -> Node:
        """Convert an index to the node it represents. This is mostly for
        debugging and visual purposes.

        Args:
            index (int): An index representing a node

        Returns:
            Node: The node found at that index.
        """
        sorted_nodes = sorted([node.name for node in self.nodes.values()])
        return sorted_nodes[index]

    def get_edge_from_matrix(self, from_index: int, to_index: int) -> Edge:
        """Convert an index pair into the edge it represents.

        Args:
            from_index (int): index representing the first node
            to_index (int): index representing the second node

        Returns:
            Edge: an Edge object between the two nodes.
        """
        sorted_nodes = sorted([node.name for node in self.nodes.values()])
        key = (sorted_nodes[from_index], sorted_nodes[to_index])
        if key in self.edges:
            return self.edges[key]
        else:
            return None
    
    def delete_all_nodes(self):
        """Unassign all edges and nodes"""
        self.nodes = dict()
        self.edges = dict()

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
            self.add_node(
                Node(coordinate[0], coordinate[1], chr(name) + overflow_char))
            length -= 1
            if length == 0:
                break
        self.generate_all_edges()

    def generate_random_graph(self, seed: int, length: int):
        MIN_X = 25.0
        MIN_Y = 25.0
        MAX_X = 350.0
        MAX_Y = 350.0

        random.seed(seed)
        name = ord('a') - 1
        overflow = 0
        for i in range(length):
            overflow_char = ''
            if name == 122:
                overflow += 1
                name = ord('a')
            else:
                name += 1
            if overflow > 0:
                overflow_char = str(overflow)
            random_x = random.random() * (MAX_X - MIN_X) + MIN_X
            random_y = random.random() * (MAX_Y - MIN_Y) + MIN_Y
            self.add_node(Node(random_x, random_y, chr(name) + overflow_char))

        self.generate_all_edges()


    def highlight_path(self, path: 'list[int]'):
        node_names = [self.get_node_from_matrix(index) for index in path]
        print(node_names)
        for i in range(len(node_names) - 1):
            self.nodes[node_names[i]].highlight = True
            self.edges[(node_names[i], node_names[i+1])].highlight = True
        if node_names[len(node_names) - 1] is not node_names[0]:
            self.nodes[node_names[len(node_names) - 1]].highlight = True
            self.edges[node_names[len(node_names) - 1],
                       node_names[0]].highlight = True

    def unhighligh_all(self):
        for node in self.nodes.values():
            node.highlight = False
        for edge in self.edges.values():
            edge.highlight = False
