from NodeManager import NodeManager
import NearestNeighborTSP
import BruteForceTSP
import MatrixToolsTSP

node_manager = NodeManager()


def main():
    node_manager.init_display()
    node_manager.assign_solve_command(
        NearestNeighborTSP.solve, "Nearest Neighbor")
    node_manager.assign_solve_command(BruteForceTSP.solve, "Brute force")

    node_manager.generate_graph(MatrixToolsTSP.graph7)

    node_manager.draw()
    node_manager.display_mainloop()

    print("Closed succesfully")


if __name__ == "__main__":
    main()
