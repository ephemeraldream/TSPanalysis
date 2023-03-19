import math


class TspNode:

    def __init__(self, x,y,name):
        self.x = x
        self.y = y
        self.name = name

    def __eq__(self, other):
        if self.x == other.x and self.y and self.name == self.name:
            return False
        else:
            return True

    @staticmethod
    def length(node1, node2):
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)



class TSP:

    def __init__(self):
        self.sequence = []

    def addNode(self, newNode):
        if self not in self.sequence:
            self.sequence.append(newNode)
            return True
        else:
            return False

    def totalLength(self):
        total = 0
        for i in range(len(self.sequence)-1):
            total += TspNode.length(self.sequence[i], self.sequence[i+1])
        return total


    def restart(self):
        self.sequence = []













