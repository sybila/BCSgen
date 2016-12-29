class Conflict:
	def __init__(self, fromTo, column):
		self.fromTo = fromTo
		self.column = column

	def __eq__(self, other):
		return self.fromTo == other.fromTo

	def __hash__(self):
		return hash(self.fromTo)

	def getFrom(self):
		return self.fromTo[0]

	def getTo(self):
		return self.fromTo[1]


def isNeg(i):
	if i > 0:
		return True
	return False

def checkVector(vector, column):
	concurrent = set()
	dependent = set()
	lenvec = len(vector)
	for i in range(lenvec):
		for j in range(i, lenvec):
			if vector[i] and vector[j]:
				if isNeg(vector[i]) and isNeg(vector[j]):
					concurrent.add(Conflict((i,j), column))
				if (isNeg(vector[i]) and not isNeg(vector[j])) or (not isNeg(vector[i]) and isNeg(vector[j])):
					dependent.add(Conflict((i,j), column))
	return concurrent, dependent

def toStr(i):
	if i < 0:
		return " " + str(i)
	return "  " + str(i)
