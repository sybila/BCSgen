import numpy as np

"""
Class Vector_reaction
Vector representation of Reaction
:attribute From: vector (numpy array)
:attribute To: vector (numpy array)
"""
class Vector_reaction:
	def __init__(self, From, To):
		self.From = From
		self.To = To
		self.difference = self.To - self.From

	def __eq__(self, other):
		return (self.From == other.From).all() and (self.To == other.To).all()

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return "".join(map(lambda item: str(item), self.From)) + " -> " + "".join(map(lambda item: str(item), self.To))

	def __hash__(self):
		return hash(str(self.From) + str(self.To))

	def applyVector(self, state, bound):
		vec = np.array(state) - self.From
		if (vec >= 0).all():
			vec += self.To
		 	if max(vec) <= bound:
				return tuple(vec)

	def getDict(self):
		return {'from' : "|".join(map(str, self.From)), 'to' : "|".join(map(str, self.To))}

	def getBound(self):
		return max((max(self.From), max(self.To)))