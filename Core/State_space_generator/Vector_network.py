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
		return str(self.State) + "\n ------- \n" + "\n".join([str(vector) for vector in self.Vectors]) + \
			   "\n ----- \n" + "\n".join([str(self.Translations.index(item) + 1) + \
			   		" | " + str(item) for item in self.Translations])

	def getTranslations(self):
		return self.Translations

	def getState(self):
		return self.State

	def applyVectors(self, state, bound):
		return [item for item in [vector.applyVector(state, bound) for vector in self.Vectors] if item is not None]

	def getBound(self):
		return max(max(self.State), max([vector.getBound() for vector in self.Vectors]))
