"""Solve the travelling salesman problem using a brute-force approach
    (assuming all nodes have edges to all other nodes). Update the result to
    the GUI.

    Because this is a brute-force algorithm it will calculate the distance of
    every possible permutation of paths. Thus, this algorithm will run O(n!)
    operations, where n is the number of nodes. Space complexity will be
    O(n^2) as that is the size of the matrix.
    
    tl;dr
        Time complexity: O(n!)
        Space complexity: O(n^2)

Raises:
        Exception: When attempting to solve a matrix bigger than 9
        (it would take too long).
"""
import itertools
from NodeManager import NodeManager
from MatrixToolsTSP import calculate_cost, calculate_circuit_cost
import MatrixToolsTSP


def solve(node_manager: NodeManager) -> list:
    """Solve the travelling salesman problem using a brute-force approach
    (assuming all nodes have edges to all other nodes). Update the result to
    the GUI.

    Because this is a brute-force algorithm it will calculate the distance of
    every possible permutation of paths. Thus, this algorithm will run O(n!)
    operations, where n is the number of nodes. Space complexity will be
    O(n) as we will be generating a path of n length.
    
    tl;dr
        Time complexity: O(n!)
        Space complexity: O(n)

    Args:
        node_manager (NodeManager): Needs a NodeManager to be passed as the
        function will need to pull matrix data and then update the graph with
        the solution.

    Raises:
        Exception: When attempting to solve a matrix bigger than 9
        (it would take too long).
    """
    # Check if the number of nodes in the NodeManager object is greater than 9.
    # If it is, raise an exception and print a message.
    if len(node_manager.nodes) > 9:
        raise Exception(
            "ABORTING! Cannot feasably solve over 9 nodes \
                using this approach in a timely manner!")

    # Generate a matrix representing the distances 
    # between nodes in the NodeManager object.
    matrix = node_manager.generate_matrix()

    # Get the number of nodes in the matrix.
    num_nodes = len(matrix)

    # Create a list of node indices.
    nodes = list(range(num_nodes))

    # Initialize variables for storing the best path and its cost.
    best_path = None
    best_cost = float('inf')

    # Iterate through all possible permutations of the nodes.
    for perm in itertools.permutations(nodes):
        # Initialize a variable for storing the cost of the current path.
        cost = 0

        # Calculate the cost of the current path.
        cost = calculate_circuit_cost(matrix, perm)

        # Update the best path and its cost if this path is better.
        if cost < best_cost:
            best_path = list(perm)
            best_cost = cost

    return best_path
