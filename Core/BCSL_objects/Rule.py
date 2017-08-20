class Rule(object):
	def __init__(self, chi, omega, I, indexMap, Indices):
		self.chi = chi
		self.omega = omega
		self.I = I 					# last index on lhs
		self.indexMap = [-1] + indexMap
		self.Indices = Indices

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "chi = [" + ", ".join(map(str, self.chi)) + "]" + "\n" +\
			   "omega = [" + ", ".join(map(str, self.omega)) + "]" + "\n" +\
			   "I = " + str(self.I) + "\n" +\
			   "map = (" + ", ".join(map(str, self.indexMap)) + ")\n" +\
			   "Indices = [" + "; ".join(map(str, self.Indices)) + "]"

	def __lt__(self, other):
		return str(self) < str(other)