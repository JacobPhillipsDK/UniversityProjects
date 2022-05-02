class Node:
    """
        A node class for A* Pathfinding
        g is cost from start to current Node
        h is heuristic based estimated cost for current Node to end Node
        f is total cost of present node i.e. :  f = g + h
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0 # cost from start to current Node
        self.h = 0 # heuristic based estimated cost for current Node to end Node
        self.f = 0 # total cost of present node i.e. :  f = g + h
        self.cost = 0

    def __eq__(self, other): # Overriding the default __eq__ method
        return self.position == other.position

    def set_cost(self, cost):
        self.cost = cost
