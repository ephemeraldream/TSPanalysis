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
import random
import math
from NodeManager import NodeManager
from MatrixToolsTSP import calculate_cost, calculate_circuit_cost
import MatrixToolsTSP
# currently following the pdf below
# http://160592857366.free.fr/joe/ebooks/ShareData/Heuristics%20for%20the%20Traveling%20Salesman%20Problem%20By%20Christian%20Nillson.pdf


# This function takes a NodeManager object as an argument and returns None.
def solve(node_manager: NodeManager) -> list:
    """Solve the travelling salesman problem using a nearest-neighbor approach
    (assuming all nodes have edges to all other nodes). Update the result to
    the GUI.

    The Nearest Neighbor approach is very lazy in which it repeatively chooses
    the shortest node at every step. The steps are: pick random node,
    repeatively pick the shortest unvisited node, complete the circuit. This
    can sometimes give poor results but generally does better than simply
    randomly picking a permutation as a path. It uses a space complexity of
    O(n^2) as that is the size of the matrix.
    
    This approach is O(n). As it only has to keep picking the shortest path n
    times. The current implementation however isn't quite O(n) because it
    searches the entire node for the shortest next node at every step of the
    path (making it O(n^2)). This, however, can be mitigated by using a
    non-comparison sorting algorithm and appropriate data structures (making
    it O(n) again). It's not currently implemented as it adds complexity
    taking away from the main focus of the nearest neighbor algorithm.
    
    tl;dr
        Time complexity: O(n) (currently though O(n^2))
        Space complexity: O(n^2)

    Args:
        node_manager (NodeManager): Needs a NodeManager to be passed as the
        function will need to pull matrix data and then update the graph with
        the solution.
    """
    # Generate a matrix representing the distances between nodes in the NodeManager object.
    matrix = node_manager.generate_matrix()

    # Create a list of boolean values representing whether each city has been visited or not.
    visited_cities = [False]*len(matrix)

    # Create an empty list for storing the path.
    path = []

    # Select a random city to start the path.
    start_city = random.randrange(0, len(matrix))
    path.append(start_city)
    visited_cities[start_city] = True

    # Initialize a variable for storing the current city.
    curr_city = start_city

    # Repeat the following steps until all cities have been visited.
    while False in visited_cities:

        # Find the nearest unvisited city to the current city.
        nearest_unvisited_city = None
        nearest_unvisited_weight = math.inf
        for i in range(len(matrix)):
            if curr_city != i and not visited_cities[i] and matrix[curr_city][i] < nearest_unvisited_weight:
                nearest_unvisited_city = i
        path.append(nearest_unvisited_city)
        visited_cities[nearest_unvisited_city] = True

        # If there are any unvisited cities left, repeat the previous step.

    return path
