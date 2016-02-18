class Edge:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __eq__(self, other):
        return self.left == other.left and self.right == other.right

    def __str__(self):
        return self.__repr__() + '\n'

    def __repr__(self):
        return self.left.__str__() + ' -> ' + self.right.__str__()

    def __hash__(self):
        return hash(self.__repr__())

    """
    Checks if a edge is not self-loop
    Caused by the fact changeStructureStates sometimes return original agent.. should be checked and fixed
    :return: False if it is not a self-loop
    """
    def isNotSelfLoop(self):
        return not self.left == self.right