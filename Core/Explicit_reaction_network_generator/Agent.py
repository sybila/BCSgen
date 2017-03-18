from State import *

class Agent:
	def __init__(self, item):
		if "{" in item and not "(" in item:
			item = item.replace("{", "(").replace("}", ")")

		part = item.split("(")
		self.name = part[0]

		self.states = []
		if len(part) > 1:
			tmp = part[1].split(",")
			for i in range(len(tmp)):
				self.states.append(State(tmp[i].replace(")", "")))
		#else:
		#	self.states = None # asi netreba

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "/ Agent - " + self.name + ": " + ", ".join(map(str, self.states)) + " /"