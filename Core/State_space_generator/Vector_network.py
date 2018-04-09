from .Vector_reaction import *

"""
Class Vector_network
Holds vector representation of reaction-based model
:attribute State: initial State
:attribute Vectors: list of Vector reactions
:attribute Translations: list of unique ordered Agents
"""
class Vector_network:
	def __init__(self, state, vectors, table):
		self.State = state
		self.Vectors = vectors
		self.Translations = table

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return str(self.State) + "\n ------- \n" + "\n".join(list(map(lambda vector: str(vector), self.Vectors))) + \
			   "\n ----- \n" + "\n".join(list(map(lambda item: str(self.Translations.index(item) + 1) + " | " + str(item), self.Translations)))

	def getTranslations(self):
		return self.Translations

	def getState(self):
		return self.State

	def applyVectors(self, state, bound):
		return list(filter(lambda item: item is not None, list(map(lambda vector: vector.applyVector(state, bound), self.Vectors))))

	def getBound(self):
		return max(max(self.State), max(list(map(lambda vector: vector.getBound(), self.Vectors))))
