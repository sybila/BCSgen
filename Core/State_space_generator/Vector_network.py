from Vector_reaction import *

class Vector_network:
	def __init__(self, state, vectors, table):
		self.State = state
		self.Vectors = self.toVectorReactions(vectors)
		self.Translations = table

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return str(self.State) + "\n ------- \n" + "\n".join(map(lambda vector: str(vector), self.Vectors)) + \
			   "\n ----- \n" + "\n".join(map(lambda item: str(self.Translations.index(item) + 1) + " | " + str(item), self.Translations))

	def getState(self):
		return self.State

	def toVectorReactions(self, vectors):
		return map(lambda vector: Vector_reaction(*vector), vectors)

	def applyVectors(self, state, bound):
		return filter(lambda item: item is not None, map(lambda vector: vector.applyVector(state, bound), self.Vectors))