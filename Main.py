from TSP_Application.TSPApplication import TSPApplication

def main():
    # application contains all instance data for the TSP solvers
    tsp_app = TSPApplication()
    
    # once we enter the main loop we hand over execution over to tkinter
    tsp_app.enter_mainloop()

    # ^^^ this means that the print statement here will only occur after
    # tkinter finishes execution (aka it closes)
    print("Closed succesfully")


if __name__ == "__main__":
    main()
