import numpy as np
from copy import deepcopy

class Vector_reaction:
	def __init__(self, From, To):
		self.From = From
		self.To = To

	def __eq__(self, other):
		return (self.From == other.From).all() and (self.To == other.To).all()

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "".join(map(lambda item: str(item), self.From)) + " -> " + "".join(map(lambda item: str(item), self.To))

	def __hash__(self):
		return hash(str(self.From) + str(self.To))

	def applyVector(self, state, bound):
		if (state >= self.From).all():
			vec = tuple(np.array(state) - self.From + self.To)
			if max(vec) <= bound:
				return vec