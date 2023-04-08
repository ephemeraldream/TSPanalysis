

def main():
    dijkstras: Dijkstras = Dijkstras()

    # not strictly necessary
    # dijkstras.addNode(100, 100, 'a')
    # dijkstras.addNode(50, 150, 'b')
    # dijkstras.addNode(150, 150, 'c')
    # dijkstras.addNode(100, 200, 'd')

    dijkstras.addEdge('a', 'b', 2)
    dijkstras.addEdge('a', 'c', 1)
    dijkstras.addEdge('b', 'd', 1)
    dijkstras.addEdge('c', 'd', 4)

    dijkstras.solve('a')

    # should print "a -> b -> d (cost = 1)"
    dijkstras.printShortestPath('a', 'd')
    dijkstras.printShortestPath('a', 'c')  # should print "a -> c (cost = 1)"

    print("Done")


class Dijkstras():
    def __init__(self):
        # important, as it stores initial data about all edges
        self.nodes: dict[str, MinHeap[Edge]] = dict()

        # not as important, it will get written to by solve()
        self.paths: dict[str, str] = dict()
        self.totalCost: dict[str, float] = dict()

    # not necessary
    def addNode(self, x: float, y: float, name: str) -> None:
        pass

    # add an edge from one node to another, implicitly adds the node
    def addEdge(self, fromNode: str, toNode: str, weight: float = -1) -> None:
        if fromNode not in self.nodes:
            self.nodes[fromNode] = MinHeap()
        self.nodes[fromNode].add(Edge(toNode, weight))

    # solve the
    def solve(self, startNode: str) -> None:
        exploredNodes = set()
        totalCost: dict[str, float] = dict()
        totalCost[startNode] = 0
        paths: dict[str, str] = dict()
        nextUnexploredNodes = MinHeap()
        unexploredNodes = MinHeap()
        unexploredNodes.add(startNode)

        while unexploredNodes:
            for node in unexploredNodes:
                exploredNodes.add(node)

                if node in self.nodes:
                    edge: Edge
                    for edge in self.nodes[node]:
                        newCost = totalCost[node] + edge.weight
                        if edge.toNode not in totalCost or newCost < totalCost[edge.toNode]:
                            paths[edge.toNode] = node
                            totalCost[edge.toNode] = totalCost[node] + \
                                edge.weight
                        if edge.toNode not in exploredNodes:
                            nextUnexploredNodes.add(edge.toNode)
            unexploredNodes = nextUnexploredNodes
            nextUnexploredNodes = MinHeap()

        print(f"all node costs from {startNode}: {totalCost}")
        print(f"path (toNode, fromNode): {paths}")

        self.paths = paths
        self.totalCost = totalCost

        return

    def printShortestPath(self, fromNode: str, toNode: str) -> None:
        currentNode = toNode
        output = ""
        while currentNode is not fromNode:
            output = f" -> {currentNode}" + output
            currentNode = self.paths[currentNode]
        output = fromNode + output + f" (cost = {self.totalCost[toNode]})"
        print(output)


class Edge:
    def __init__(self, toNode: str, weight: float = -1):
        self.toNode: str = toNode
        self.weight: float = weight

    def __hash__(self) -> int:
        return self.toNode.__hash__()

    def __eq__(self, other: 'Edge') -> bool:
        return self.toNode.__eq__(other.toNode)

    def __lt__(self, other: 'Edge') -> bool:
        return self.toNode < other.toNode


class MinHeap:
    def __init__(self):
        self.edges: list[Edge] = list()

    def add(self, edge: Edge):
        self.edges.append(edge)

    def pop(self) -> Edge:
        self.edges.sort()
        return self.edges.pop(0)

    def __iter__(self) -> Edge:
        sorted_edges = sorted(self.edges)
        while sorted_edges:
            yield sorted_edges.pop()

    def __bool__(self) -> bool:
        return bool(self.edges)


if __name__ == "__main__":
    main()
