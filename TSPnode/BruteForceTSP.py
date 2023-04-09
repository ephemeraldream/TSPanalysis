import itertools
from NodeManager import NodeManager
from MatrixToolsTSP import calculate_cost


def solve_brute_force(node_manager: NodeManager):
    if len(node_manager.nodes) > 9:
        raise Exception(
            "ABORTING! Cannot feasably solve over 9 nodes using this approach in a timely manner!")
    matrix = node_manager.generate_matrix()

    num_nodes = len(matrix)
    nodes = list(range(num_nodes))
    best_path = None
    best_cost = float('inf')

    # Iterate through all possible permutations of nodes
    for perm in itertools.permutations(nodes):
        # Calculate the cost of the current path
        cost = 0
        for i in range(num_nodes):
            cost += matrix[perm[i-1]][perm[i]]

        # Update the best path and cost if this path is better
        if cost < best_cost:
            best_path = list(perm)
            best_cost = cost

    print(best_path)
    print(calculate_cost(matrix, best_path))
    node_manager.highlight_path(best_path)
    node_manager.draw()
    node_manager.unhighligh_all()

    print("Solved!")

    return best_path
