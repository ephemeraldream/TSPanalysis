"""Solve the travelling salesman problem using a nearest-neighbor approach
    (assuming all nodes have edges to all other nodes). Update the result to
    the GUI.

    The Nearest Neighbor approach is very lazy in which it repeatively chooses
    the shortest node at every step. The steps are: pick random node,
    repeatively pick the shortest unvisited node, complete the circuit. This
    can sometimes give poor results but generally does better than simply
    randomly picking a permutation as a path. It uses a space complexity of
    O(n) to store a path and unvisited nodes.
    
    This approach is O(n). As it only has to keep picking the shortest path n
    times. The current implementation however isn't quite O(n) because it
    searches the entire node for the shortest next node at every step of the
    path (making it O(n^2)). This, however, can be mitigated by using a
    non-comparison sorting algorithm and appropriate data structures (making
    it O(n) again). It's not currently implemented as it adds complexity
    taking away from the main focus of the nearest neighbor algorithm.

    tl;dr
        Time complexity: O(n) (currently though O(n^2))
        Space complexity: O(n)
"""
import itertools
import random
import math
from TSP_Application.NodeManager import NodeManager
from TSP_Application.MatrixToolsTSP import calculate_cost, calculate_circuit_cost
import TSP_Application.TSP_Solvers.NearestNeighborTSP
import TSP_Application.MatrixToolsTSP
# currently following the pdf below
# http://160592857366.free.fr/joe/ebooks/ShareData/Heuristics%20for%20the%20Traveling%20Salesman%20Problem%20By%20Christian%20Nillson.pdf


def solve(node_manager: NodeManager) -> list:
    
    # reuse nearest neighbor... costs O(n)
    matrix = node_manager.generate_matrix()
    path = TSP_Application.TSP_Solvers.NearestNeighborTSP.solve(node_manager)
    cost = TSP_Application.MatrixToolsTSP.calculate_circuit_cost(matrix, path)
    
    # now try 2-opt algorithm to re-choose paths to see if there is a better
    # solution. This costs O(n^k) where k is 2. So the time complexity is O(n^2)
    
    # len(path) choose 2 (nCr)
    for swap_index_pair in itertools.combinations(range(len(path)),2):
        swap(path, swap_index_pair[0], swap_index_pair[1])
        new_cost = TSP_Application.MatrixToolsTSP.calculate_circuit_cost(matrix, path)
        if new_cost >= cost:
            swap(path, swap_index_pair[0], swap_index_pair[1])
        

    return path

def swap(arr: list, i1: int, i2: int):
    arr[i1], arr[i2] = arr[i2],arr[i1]