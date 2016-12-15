import collections

class State:
    def __init__(self, agents, ID = ''):
        self.agents = collections.Counter(agents)
        self.ID = ID

    def __eq__(self, other):
        return self.agents == other.agents

    def __hash__(self):
        return hash(tuple(self.agents.elements()))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'vertex ID: ' + str(self.ID) + '\n' + '\n'.join(map(lambda (a, b): b.__str__() + " " + a.__str__(), self.agents.items())) + '\n\n'

    def getAgents(self):
        return self.agents

    """
    Checks if number of all agents in the state is lower than given bound
    :param bound: integer number
    :return: True if condition is satisfied
    """
    def isInBound(self, bound):
    	if self.agents:
       		return self.agents.most_common(1)[0][1] <= bound
        return True