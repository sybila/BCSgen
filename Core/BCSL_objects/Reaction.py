class Rule:
	def __init__(self, seq, I):
		self.seq = seq
		self.I = I

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "seq = [" + ",".join(map(str, self.seq)) + "]" + "\n" +\
			   "I = " + str(self.I) + "\n"
			   
	def __lt__(self, other):
		return str(self) < str(other)