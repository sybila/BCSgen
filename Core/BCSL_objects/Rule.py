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
		return "chi = [" + ", ".join([str(x) for x in self.chi]) + "]" + "\n" +\
			   "omega = [" + ", ".join([str(x) for x in self.omega]) + "]" + "\n" +\
			   "I = " + str(self.I) + "\n" +\
			   "map = (" + ", ".join([str(x) for x in self.indexMap]) + ")\n" +\
			   "Indices = [" + "; ".join([str(x) for x in self.Indices]) + "]"

	def __lt__(self, other):
		return str(self) < str(other)
