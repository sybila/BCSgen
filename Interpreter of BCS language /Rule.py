import collections
import copy

direction = " => "

def substitute(substitutions, set_of_rules):
    #tba
    return

#first choose equal ones, then compatible ones !!!
def flatten(rule):
    #tba
    return

class Rule:
    def __init__(self, left_hand_side, right_hand_side, reversible):
        self.left_hand_side = collections.Counter(left_hand_side)
        self.right_hand_side = collections.Counter(right_hand_side)
        self.reversible = reversible

    def __eq__(self, other):
        if not (self.reversible and other.reversible):
            return False
        else:
            if self.reversible:
                return (self.left_hand_side == other.left_hand_side and self.right_hand_side == other.right_hand_side) \
                       or (self.right_hand_side == other.left_hand_side and self.left_hand_side == other.right_hand_side)
            else:
                return (self.left_hand_side == other.left_hand_side and self.right_hand_side == other.right_hand_side)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        global direction
        if self.reversible:
            direction = " <=> "
        return " + ".join(map(lambda k: k.__str__(), sorted(list(self.left_hand_side.elements())))) + direction \
               +  " + ".join(map(lambda k: k.__str__(), sorted(list(self.right_hand_side.elements()))))

    def __hash__(self):
        return hash((str(self.left_hand_side), str(self.right_hand_side), str(self.reversible)))

    def __lt__(self, other):
        return self.__repr__() < other.__repr__()

    def getLeftHandSide(self):
        return self.left_hand_side

    def getRightHandSide(self):
        return self.right_hand_side

    def getReversible(self):
        return  self.reversible

