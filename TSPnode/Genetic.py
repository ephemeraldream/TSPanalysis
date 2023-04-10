import math
from NodeManager import NodeManager
from Node import Node
from Edge import Edge
import numpy as np
import itertools
from MatrixToolsTSP import calculate_circuit_cost, compare_best_solution, highlight_and_draw
import random
from NearestNeighborTSP import solve
from BruteForceTSP import solve
import pandas as pd

def genetic_algorithm(node_manager: NodeManager):
    iterations = 1000
    pop = 100
    elite_amount = 20
    matrix = node_manager.generate_matrix()
    nodes = list(range(len(matrix)))
    population = []
    for i in range(pop):
        temp_nodes = nodes.copy()
        temp_nodes = np.random.permutation(temp_nodes)
        population.append((temp_nodes, 1/calculate_circuit_cost(matrix, temp_nodes)))
    population = sorted(population, key=lambda x: x[1], reverse=True)
    elite_population = []
    selectionResults = []
    df = pd.DataFrame(np.array(population), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()

    

















    print(nodes)
    cost = calculate_circuit_cost(matrix, nodes)
    print(cost)
    print(compare_best_solution(node_manager.best_solution_weight, cost))

    # Highlight and draw the best path in the NodeManager object.
    highlight_and_draw(node_manager, nodes)

    print("Solved!")


def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []

    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])

    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    return child





























def swap_random(array):
    idx = range(len(array))
    i1, i2 = random.sample(idx, 2)
    array[i1], array[i2] = array[i2], array[i1]