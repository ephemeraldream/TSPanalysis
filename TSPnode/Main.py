from NodeManager import NodeManager
import NearestNeighborTSP
import BruteForceTSP
import MatrixToolsTSP
import SimulatedAnnealing

node_manager = NodeManager()


def main():
    node_manager.init_display()
    
    node_manager.assign_solve_command(
        NearestNeighborTSP.solve, "Nearest Neighbor")
    node_manager.assign_solve_command(BruteForceTSP.solve, "Brute force")
    node_manager.assign_solve_command(SimulatedAnnealing.simulated_annealing, "Simulated Annealing")

    node_manager.generate_random_graph(0, 200)
    #node_manager.generate_graph(MatrixToolsTSP.graph20)
    #node_manager.best_solution_weight = MatrixToolsTSP.graph7_best_distance

    node_manager.draw()
    node_manager.display_mainloop()

    print("Closed succesfully")


if __name__ == "__main__":
    main()
