import random

import numpy as np
import Node
from NodeManager import NodeManager


class Environment:
    def __init__(self, distance_matrix):
        self.distance_matrix = distance_matrix
        self.pheromones = [[1]*len(distance_matrix) for i in range(len(distance_matrix))]


class Colony:
    def __init__(self, total, ans):
        self.total = total
        self.ans = ans


    def train(self, env: Environment, ants):
        for i in range(len(env.pheromones)):
            for j in range(len(env.pheromones)):
                for ant in ants:
                    env.pheromones[i][j] += ant.own_pheromone[i][j]


    def train_all(self, env: Environment):
        cost = np.inf
        path = []
        for anss in range(self.ans):
            objs = [Ant(self, env=env) for i in range(self.total)]
            for ant in objs:
                for i in range(len(env.pheromones)-1):
                    ant.next_motion()
                ant.total += env.distance_matrix[ant.stop[-1]][ant.stop[0]]
                if ant.total < cost:
                    cost = ant.total
                    path = ant.stop
                ant.upgrade_ant()
            self.train(env, objs)
        return path, cost



class Ant:
    def __init__(self, colony: Colony, env:Environment):
        self.total = 0
        self.env = env
        self.own_pheromone = []


        self.non_stop = [i for i in range(len(env.distance_matrix))]
        self.stop = []
        self.non_stop.remove(0)
        self.stop.append(0)
        self.next = 0

    def next_motion(self):
        total = 0
        for var in self.non_stop:
            total += self.env.pheromones[self.next][var] * self.env.pheromones[self.next][var]
        p_mat = [0 for i in range(len(self.env.pheromones))]
        for var in range(len(p_mat)):
            try:
                self.non_stop.index(var)
                p_mat[var] = self.env.pheromones[self.next][var] * self.env.pheromones[self.next][var] / total
            except ValueError:
                pass
        chosen = 0
        ran = random.random()
        for var, p in enumerate(p_mat):
            ran -= p
            if ran <= 0:
                chosen = var
                break
        self.stop.append(chosen)
        self.non_stop.remove(chosen)
        self.total += self.env.distance_matrix[self.next][chosen]
        self.next = chosen


    def upgrade_ant(self):
        self.own_pheromone = [[0]*len(self.env.distance_matrix) for i in range(len(self.env.distance_matrix))]
        for z in range(1, len(self.stop)):
            j = self.stop[z]
            i = self.stop[z-1]
            self.own_pheromone[i][j] = 1 / self.total #self.env.distance_matrix[i][j]



















graph7 = ((340.35029115373504, 291.9911036284341),
          (330.546912512813, 50.76377300133961),
          (102.02621099177865, 314.0781008584721),
          (192.30295951856758, 316.8848105036639),
          (155.10029229106644, 205.99512383080938),
          (236.62287527731527, 191.59689495925704),
          (80.57511663571202, 131.04706564193646))

node_manager = NodeManager()
for i in range(7):
    vertex = graph7[i]
    node_manager.add_node(Node.Node(vertex[0], vertex[1], str(i)))



node_manager.generate_all_edges()
matrix = node_manager.generate_matrix()
map = Environment(matrix)
colony = Colony(1000, 10)
x, y = colony.train_all(map)
print(x, y)
x = 2














