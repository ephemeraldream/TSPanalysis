from TSP_Application.NodeManager import NodeManager
import numpy as np
from TSP_Application.MatrixToolsTSP import calculate_circuit_cost, compare_best_solution, highlight_and_draw


def maximization(Q: list, listed: int, passed: list):
    maxima = 0
    x = np.arange(len(Q))
    np.random.shuffle(x)
    submaxima = -np.inf
    for i in x:
        if not (passed[i]):
            continue
        if Q[listed][i] > submaxima:
            maxima = i
            submaxima = Q[listed][i]
    return maxima, submaxima



def generate(states, actions):
    Q_matrix = [[0]*states for _ in range(actions)]
    return Q_matrix


def compute_path(Q: list):
    """
    this function computes the path
    distance regarding the learning matrix.
    :param Q:
    :return:
    """
    passed = [True for i in range(len(Q))]
    path = [0 for i in range(len(Q))]
    passed[0] = False
    for i in range(1, len(Q)):
        current = path[i - 1]
        next, not_used = maximization(Q, int(current), passed)
        path[i] = next
        passed[next] = False
    return path


def q_vals(Q_table: list, euc: list):
    path = compute_path(Q_table)
    path = [int(i) for i in path]
    return calculate_circuit_cost(euc, path)


def update(Q, eucs, used, path, eps, gamma, learning_rate, total):
    """
    The process of initializing weights.
    Thhen update weight matrix.
    """
    used[0] = False
    for i in range(1, total):
        possible = np.where(used == True)[0]
        current = path[i - 1]
        if len(possible) == 1:
            after = possible[0]
            food = -eucs[int(current), int(after)]
            max_next = -eucs[int(after), int(path[0])]
        else:
            probs = np.random.random()
            if probs < eps:
                after = np.random.choice(possible)
            else:
                after, none = maximization(Q, int(current), used)
            used[after] = False
            path[i] = after
            food = -eucs[int(current), int(after)]
            none, max_next = maximization(Q, int(after), used)
        Q[int(current)][int(after)] = Q[
            int(current)][int(after)
        ] + learning_rate * (food + gamma * max_next - Q[int(current)][int(after)]) # Bellman equation to update
        # values of marticies.
    return Q


def ReinforcementLearning(node_manager: NodeManager) -> 'list[int]':
    """
    the model itself that will combine everything else in order to learn the weights.
    :param node_manager:
    :return:
    """
    node_manager.generate_matrix()
    eps = 0.95,
    gamma = 0.95,
    learning_rate = 0.2
    total_run: int = 5000

    matrix = node_manager.generate_matrix()
    dist = np.array(matrix)
    Q = [[0]*len(dist) for i in range(len(dist))]
    N = len(Q)
    Q_updated = Q.copy()
    used,path = np.array([True] * N), np.zeros((N,))
    best_distance, temp_distance = np.zeros((total_run,)), np.zeros((total_run,))
    temp_distance = np.zeros((total_run,))
    for var in range(total_run): # Udpate the matrix
        Q_updated = update(
            Q_updated, dist, used, path, eps[0], gamma[0], learning_rate, N
        )
        updated_cost = q_vals(Q, dist)
        updated_temp_cost = q_vals(Q_updated, dist)
        best_distance[var],temp_distance[var] = updated_cost,updated_temp_cost
        if updated_temp_cost < updated_cost:
            Q[:][:] = Q_updated[:][:]
        path[:] = 0
        used[:] = True
    path = compute_path(Q)
    path = [int(i) for i in path]
    return path
    # print(path)
    # final_distance = calculate_circuit_cost(matrix, path)
    # print(final_distance)
    # another_dist = calculate_circuit_cost(matrix, path)
    # print(another_dist)
    # print(compare_best_solution(node_manager.best_solution_weight, calculate_circuit_cost(matrix, path)))
    # highlight_and_draw(node_manager, list(path))























