import math
from TSP_Application.NodeManager import NodeManager
from TSP_Application.Node import Node
from TSP_Application.Edge import Edge
import numpy as np
from TSP_Application.MatrixToolsTSP import calculate_circuit_cost
import random
from TSP_Application.TSP_Solvers.NearestNeighborTSP import solve
from TSP_Application.TSP_Solvers.BruteForceTSP import solve


def simulated_annealing(node_manager: NodeManager) -> list:
    temperature: float = 1000
    iters: int = 1000
    gamma: float = 0.95
    matrix = node_manager.generate_matrix()

    num_nodes = len(matrix)
    nodes = list(range(num_nodes))
    best_distance = calculate_circuit_cost(matrix, nodes)
    for i in range(iters):
        new_nodes = nodes.copy()
        swap_random(new_nodes)
        temp_distance = calculate_circuit_cost(
            matrix, new_nodes)
        if best_distance > temp_distance:
            nodes = new_nodes.copy()
            best_distance = temp_distance

        else:
            if trigger(temp_distance, best_distance, temperature):
                nodes = new_nodes.copy()
                best_distance = temp_distance
        temperature = freezing(temperature, gamma)

    # Calculate and print the cost of the best path.

    return nodes


def trigger(new: float, old: float, temperature: float):
    p = min(1, np.exp(-(new - old) / temperature))
    if p > random.uniform(0, 1):
        return True
    else:
        return False


def freezing(temperature: float, gamma: float):
    return gamma * temperature


def swap_random(array):
    idx = range(len(array))
    i1, i2 = random.sample(idx, 2)
    array[i1], array[i2] = array[i2], array[i1]


graph7 = ((340.35029115373504, 291.9911036284341),
          (330.546912512813, 50.76377300133961),
          (102.02621099177865, 314.0781008584721),
          (192.30295951856758, 316.8848105036639),
          (155.10029229106644, 205.99512383080938),
          (236.62287527731527, 191.59689495925704),
          (80.57511663571202, 131.04706564193646))
