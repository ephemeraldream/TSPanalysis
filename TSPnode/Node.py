class Node:
    def __init__(self, x: float, y: float, name: str):
        self.x: float = x
        self.y: float = y
        self.name: str = name
        self.highlight: bool = False
