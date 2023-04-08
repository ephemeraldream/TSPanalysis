import math
from Node import Node


class Edge:
    def __init__(self, source: Node, destination: Node, weight: float = -1):
        self.source: Node = source
        self.destination: Node = destination
        self.weight: float = weight
        if self.weight < 0:
            self.generate_weight()

    def generate_weight(self):
        self.weight = math.sqrt(
            (self.source.x - self.destination.x) ** 2 + (self.source.y - self.destination.y) ** 2)
