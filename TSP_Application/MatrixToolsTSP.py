import random
import numpy as np
from TSP_Application.NodeManager import NodeManager
from TSP_Application.Display import Display

def calculate_cost(matrix, path) -> float:
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += matrix[path[i]][path[i+1]]
    return total_cost

def calculate_circuit_cost(matrix, path) -> float:
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += matrix[path[i]][path[i+1]]
    if path[len(path) - 1] != path[0]:
        total_cost += matrix[path[len(path) - 1]][path[0]]
    return total_cost

def compare_best_solution(best_weight: float, current_weight: float) -> str:
    if best_weight is None:
        return "No best possible solution data available."
    percent_more_than = (current_weight/best_weight - 1.0)*100
    return f"This algorithm found a distance {percent_more_than:.4f}% longer than the best possible solution."

def print_random_vertecies(x, y, width, height, count):
    for _ in range(count):
        print(f"{random.random()*width+x}, {random.random()*height+y}")

def pretty_print(matrix: 'list[list[float]]'):
    np_matrix = np.array(matrix)
    print(np.array2string(np_matrix, formatter={
          'float_kind': '{0:.1f}'.format}))

def display_solution(node_manager: NodeManager, display: Display, path: 'list[int]', cost: float):
    # Print the best path and its cost.
    print(path)
    print(cost)
    
    # Print a comparison between the best known solution and the current solution
    # TODO currently disabled, may want to implement Held-Karp first!!!
    # print(compare_best_solution(node_manager.best_solution_weight, cost))
    
    # TEMP TODO calculating and setting distance on the spot
    # this is not the right place to be doing this however
    display.distance_result.config(text=f"Distance: {cost:.2f}")

    # Highlight and draw the best path in the NodeManager object.
    highlight_and_draw(node_manager, display, path)

def highlight_and_draw(node_manager: NodeManager, display: Display, path: 'list[int]'):
    node_manager.unhighligh_all()
    node_manager.highlight_path(path)
    display.draw_nodes(node_manager.nodes, node_manager.edges)
    
graph3 = ((100, 100),
          (150, 100),
          (100, 150))

graph3_best_distance = 170.71067811865476
graph3_best_path = ['b', 'c', 'd']

graph5 = ((230.49504523961062, 105.43057168619771),
          (338.0115162465884, 157.20422605699437),
          (178.61405457099016, 248.0545501331334),
          (323.3895424676583, 207.4384329111723),
          (99.88198923623604, 182.1961799738695))

graph5_best_distance = 576.1635719194229
graph5_best_path = ['b', 'f', 'd', 'e', 'c']

graph7 = ((340.35029115373504, 291.9911036284341),
          (330.546912512813, 50.76377300133961),
          (102.02621099177865, 314.0781008584721),
          (192.30295951856758, 316.8848105036639),
          (155.10029229106644, 205.99512383080938),
          (236.62287527731527, 191.59689495925704),
          (80.57511663571202, 131.04706564193646))

graph7_best_distance = 1023.9144239772485
graph7_best_path = ['d', 'e', 'b', 'c', 'g', 'f', 'h']

graph10 = ((168.87564991613763, 224.00475922677046),
           (225.55478793876802, 69.95926719875305),
           (290.7925722451604, 195.52894255256285),
           (57.29739774371288, 255.6624830176453),
           (270.14700507253997, 344.24929501176723),
           (80.4312032802269, 151.7902987241904),
           (334.2859624137761, 287.90233760039587),
           (246.1610173095308, 81.59918420334145),
           (98.89499875712568, 322.1012226197179),
           (256.38504957287716, 149.4712506936051))

graph10_best_distance = 966.3873413305154
graph10_best_path = ['c', 'g', 'e', 'j', 'b', 'f', 'h', 'd', 'k', 'i']

graph20 = ((174.4130316683828, 69.55558809662536),
           (29.868265154015937, 28.346875777925874),
           (178.79564979865066, 312.0379139676986),
           (328.4151854900073, 163.3721443627838),
           (358.1405353962685, 128.95922425718948),
           (67.12567194635979, 62.111764772615686),
           (191.15021630009457, 236.83069707019496),
           (208.25299236469016, 140.88326001297673),
           (52.9235287573503, 164.93359059469086),
           (389.4501822131618, 51.55948048221493),
           (353.83849605846666, 398.3092969478408),
           (394.13894803623856, 309.17129591058347),
           (284.56353691893764, 162.04260995464915),
           (286.60619101735426, 194.66470239511418),
           (78.49614836114479, 67.91040882661727),
           (352.4015027655291, 248.07480569101918),
           (113.9784380920963, 224.45683794390237),
           (181.87566208948775, 394.52568073410214),
           (109.52410586219484, 385.38509459600556),
           (300.85998645444397, 128.82662723159416))

# no data on shortest possible path :(
