import numpy as np
from copy import deepcopy

class Vector_reaction:
	def __init__(self, From, To):
		self.From = From
		self.To = To

	def __eq__(self, other):
		return self.From == other.From and self.To == other.To

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return str(self.From) + " -> " + str(self.To)

	def __hash__(self):
		return hash(str(self.From) + str(self.To))

	def applyVector(self, state):
		if (state >= self.From).all():
			return new_state - self.From + self.To
		return None