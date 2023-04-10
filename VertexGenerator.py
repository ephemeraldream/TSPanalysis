import itertools
import random
import math
import csv

def main():
    points_and_solutions = generate_points_and_paths(1000, 6, 0)
    print(len(str(points_and_solutions)))
    filename = "points_solutions.csv"
    print("Expanding data into comma separeted list...")
    rows = []
    for single_points_and_solution in points_and_solutions:
        points, solution, cost = single_points_and_solution
        expanded_points = []
        for point in points:
            expanded_points.append(point[0])
            expanded_points.append(point[1])
        row = []
        row.extend(expanded_points)
        row.extend(solution)
        row.append(cost)
        rows.append(row)
    print("Writing to \"points_solutions.csv\"...")
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(rows)
    # print(points_and_solutions)
    print("Done!")

def generate_points_and_paths(total_solutions: int, node_count: int, seed: int) -> 'list[list[tuple[float, float],list[int], float]]':
    random.seed(seed)
    points_and_solutions = [None] * total_solutions
    for i in range(total_solutions):
        points = _generate_points(node_count)
        solution, cost = brute_force_solve(points)
        points_and_solutions[i] = (points, solution, cost)
    return points_and_solutions

def _generate_points(node_count: int) -> 'list[tuple[float, float]]':
    MIN_X = 25.0
    MIN_Y = 25.0
    MAX_X = 350.0
    MAX_Y = 350.0
    points = [None]*node_count
    for i in range(node_count):
        random_x = random.random() * (MAX_X - MIN_X) + MIN_X
        random_y = random.random() * (MAX_Y - MIN_Y) + MIN_Y
        points[i] = (random_x, random_y)
    return points
    
    
def generate_matrix(points: 'list[tuple[float, float]]') -> 'list[list[float]]':
    edge_matrix = [None]*len(points)
    for y in range(len(points)):
        row = [math.inf]*len(points)
        for x in range(len(points)):
            row[x] = euclidean_distance(points[x], points[y])
        edge_matrix[y] = row
    return edge_matrix
                
def euclidean_distance(point1: 'tuple[float, float]', point2: 'tuple[float, float]') -> float:
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def brute_force_solve(points: 'list[tuple[float, float]]') -> 'tuple[list[int],float]':
    # Generate a matrix representing the distances 
    # between nodes in the NodeManager object.
    matrix = generate_matrix(points)

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

    cost = calculate_circuit_cost(matrix, best_path)
    # print(points)
    # print(best_path)
    # print(cost)
    return (best_path, cost)

def calculate_circuit_cost(matrix, path) -> float:
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += matrix[path[i]][path[i+1]]
    if path[len(path) - 1] != path[0]:
        total_cost += matrix[path[len(path) - 1]][path[0]]
    return total_cost

if __name__ == "__main__":
    main()