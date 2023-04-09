
import random
import math
from NodeManager import NodeManager
from MatrixToolsTSP import calculate_cost
import MatrixToolsTSP
# currently following the pdf below
# http://160592857366.free.fr/joe/ebooks/ShareData/Heuristics%20for%20the%20Traveling%20Salesman%20Problem%20By%20Christian%20Nillson.pdf


def solve(node_manager: NodeManager) -> None:
    matrix = node_manager.generate_matrix()
    visited_cities = [False]*len(matrix)
    path = []

    # select a random city
    start_city = random.randrange(0, len(matrix))
    path.append(start_city)
    visited_cities[start_city] = True

    curr_city = start_city
    while False in visited_cities:
        # find nearest unvisited city and go there
        nearest_unvisited_city = None
        nearest_unvisited_weight = math.inf
        for i in range(len(matrix)):
            if curr_city != i and not visited_cities[i] and matrix[curr_city][i] < nearest_unvisited_weight:
                nearest_unvisited_city = i
        path.append(nearest_unvisited_city)
        visited_cities[nearest_unvisited_city] = True

        # are there any unvisited cities left? If yes, repeat step 2

    # return to first city
    # node: omitted but is currently still handled by node_manager (having a duplicate end and start)
    # path.append(start_city)

    print(path)
    print(calculate_cost(matrix, path))
    MatrixToolsTSP.highlight_and_draw(node_manager, path)
    print("Solved!")
