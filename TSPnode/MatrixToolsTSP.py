def calculate_cost(matrix, path):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += matrix[path[i]][path[i+1]]
    print(total_cost)