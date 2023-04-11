import random

import numpy as np
import TSP_Application.Node
from TSP_Application.NodeManager import NodeManager




class Colony:
    def __init__(self, total, ans, distance_matrix):
        self.total = total
        self.ans = ans
        self.distance_matrix = distance_matrix
        self.pheromones = [[1]*len(distance_matrix) for i in range(len(distance_matrix))]


    def train(self, ants):
        """
        we update a particular
        :param env:
        :param ants:
        :return:
        """
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones)):
                for ant in ants:
                    self.pheromones[i][j] += ant.own_pheromone[i][j]


    def train_all(self):
        cost,path = np.inf, []
        for anss in range(self.ans):
            objs = [Ant(self) for i in range(self.total)]
            for ant in objs:
                for i in range(len(self.pheromones)-1):
                    ant.next_motion()
                ant.total += self.distance_matrix[ant.stop[-1]][ant.stop[0]]
                if ant.total < cost:
                    cost, path = ant.total, ant.stop
                ant.move_ant()
            self.train(objs)
        return path, cost



class Ant:
    def __init__(self, colony: Colony):
        self.total = 0
        self.colony = colony
        self.own_pheromone = []
        self.non_stop = [i for i in range(len(colony.distance_matrix))]
        self.stop = []
        self.non_stop.remove(0)
        self.stop.append(0)
        self.next = 0


    def next_motion(self):
        """
        Here we are throwing an ant to the graph. One by one and then update the matrix.
        :return: None
        """
        u,total = random.random(),0
        for var in self.non_stop:
            total += self.colony.pheromones[self.next][var] * self.colony.pheromones[self.next][var]
        p_mat = [0 for i in range(len(self.colony.pheromones))]
        for var in range(len(p_mat)):
            try:
                self.non_stop.index(var)
                p_mat[var] = self.colony.pheromones[self.next][var] * self.colony.pheromones[self.next][var] / total
            except ValueError:
                pass
        chosen = 0
        for var, p in enumerate(p_mat):
            u -= p
            if u <= 0:
                chosen = var
                break
        self.stop.append(chosen)  # I use stop and non_stop like a double queue(!) to check the passed edges.
        self.non_stop.remove(chosen)
        self.total += self.colony.distance_matrix[self.next][chosen]
        self.next = chosen


    def move_ant(self):
        """
        whenever the ant went all the road,
        we need to store its pheromones to the right
        places to update it after.
        :return:
        """
        self.own_pheromone = [[0]*len(self.colony.distance_matrix) for i in range(len(self.colony.distance_matrix))]
        for z in range(1, len(self.stop)):
            j,i = self.stop[z], self.stop[z-1]
            self.own_pheromone[i][j] = 1 / self.total





def solve(node_manager: NodeManager) -> 'list[int]':
    """
    API for connecting class
    :param node_manager:
    :return:
    """
    matrix = node_manager.generate_matrix()
    colony = Colony(5000, 10, distance_matrix=matrix)
    path, y = colony.train_all()
    return path



# graph7 = ((340.35029115373504, 291.9911036284341),
#           (330.546912512813, 50.76377300133961),
#           (102.02621099177865, 314.0781008584721),
#           (192.30295951856758, 316.8848105036639),
#           (155.10029229106644, 205.99512383080938),
#           (236.62287527731527, 191.59689495925704),
#           (80.57511663571202, 131.04706564193646))

# node_manager = NodeManager()
# for i in range(7):
#     vertex = graph7[i]
#     node_manager.add_node(Node.Node(vertex[0], vertex[1], str(i)))



# node_manager.generate_all_edges()
# matrix = node_manager.generate_matrix()
# map = Environment(matrix)
# colony = Colony(1000, 10)
# x, y = colony.train_all(map)
# print(x, y)
# x = 2














