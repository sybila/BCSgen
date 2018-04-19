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
		return "chi = [" + ", ".join(list(map(str, self.chi))) + "]" + "\n" +\
			   "omega = [" + ", ".join(list(map(str, self.omega))) + "]" + "\n" +\
			   "I = " + str(self.I) + "\n" +\
			   "map = (" + ", ".join(list(map(str, self.indexMap))) + ")\n" +\
			   "Indices = [" + "; ".join(list(map(str, self.Indices))) + "]"

	def __lt__(self, other):
		return str(self) < str(other)