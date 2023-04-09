from NodeManager import NodeManager
from Node import Node
from Edge import Edge
import numpy as np
from random import random

node_manager = NodeManager()

def pretty_print(matrix: 'list[list[float]]'):
    np_matrix = np.array(matrix)
    print(np.array2string(np_matrix, formatter={'float_kind': '{0:.1f}'.format}))

def printRandomVertecies(x, y, width, height, count):
    for _ in range(count):
        print(f"{random()*width+x}, {random()*height+y}")
    
    

def createGraph3():
    nodeA = Node(100, 100, "a")
    nodeB = Node(150, 100, "b")
    nodeC = Node(100, 150, "c")

    node_manager.add_node(nodeA)
    node_manager.add_node(nodeB)
    node_manager.add_node(nodeC)
    
    node_manager.generate_all_edges()

def createGraph5():
    nodes = [
        Node(230.49504523961062, 105.43057168619771, "a"),
        Node(338.0115162465884, 157.20422605699437, "c"),
        Node(178.61405457099016, 248.0545501331334, "d"),
        Node(323.3895424676583, 207.4384329111723, "e"),
        Node(99.88198923623604, 182.1961799738695, "f")
    ]
    for node in nodes:
        node_manager.add_node(node)
    node_manager.generate_all_edges()

def createGraph7():
    nodes = [
        Node(340.35029115373504, 291.9911036284341, "a"),
        Node(330.546912512813, 50.76377300133961, "c"),
        Node(102.02621099177865, 314.0781008584721, "d"),
        Node(192.30295951856758, 316.8848105036639, "e"),
        Node(155.10029229106644, 205.99512383080938, "f"),
        Node(236.62287527731527, 191.59689495925704, "g"),
        Node(80.57511663571202, 131.04706564193646, "h")
    ]
    for node in nodes:
        node_manager.add_node(node)
    node_manager.generate_all_edges()

def createGraph10():
    nodes = [
        Node(168.87564991613763, 224.00475922677046, "a"),
        Node(225.55478793876802, 69.95926719875305, "c"),
        Node(290.7925722451604, 195.52894255256285, "d"),
        Node(57.29739774371288, 255.6624830176453, "e"),
        Node(270.14700507253997, 344.24929501176723, "f"),
        Node(80.4312032802269, 151.7902987241904, "g"),
        Node(334.2859624137761, 287.90233760039587, "h"),
        Node(246.1610173095308, 81.59918420334145, "i"),
        Node(98.89499875712568, 322.1012226197179, "j"),
        Node(256.38504957287716, 149.4712506936051, "k")
    ]
    for node in nodes:
        node_manager.add_node(node)
    node_manager.generate_all_edges()

def main():
    node_manager.init_display()
    
    createGraph5()
    
    node_manager.generate_matrix()
    node_manager.assign_solve_command(solve)

    node_manager.draw()
    node_manager.display_mainloop()

    print("Closed succesfully")

def solve():
    matrix = node_manager.generate_matrix()
    
    pretty_print(matrix)
    
    print("totally solved...")

if __name__ == "__main__":
    main()
