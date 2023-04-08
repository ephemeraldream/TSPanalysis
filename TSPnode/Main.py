from NodeManager import NodeManager
from Node import Node
from Edge import Edge
import numpy as np

node_manager = NodeManager()

def pretty_print(matrix: 'list[list[float]]'):
    np_matrix = np.array(matrix)
    print(np.array2string(np_matrix, formatter={'float_kind': '{0:.1f}'.format}))



def main():
    node_manager.init_display()

    nodeA = Node(100, 100, "a")
    nodeB = Node(150, 100, "b")
    nodeC = Node(100, 150, "c")

    edgeAB = Edge(nodeA, nodeB, 100) # manually added weight

    node_manager.add_node(nodeA)
    node_manager.add_node(nodeB)
    node_manager.add_node(nodeC)
    node_manager.add_edge(edgeAB)

    node_manager.generate_all_edges()
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
