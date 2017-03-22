from State import *

class Agent:
	def __init__(self, item):
		if "{" in item and not "(" in item:
			item = item.replace("{", "(").replace("}", ")")

		part = item.split("(")
		self.name = part[0]
		self.states = []

		if len(part) > 1:
			self.states = map(lambda tmp: State(tmp.replace(")", "")), part[1].split(","))

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "/ Agent - " + self.name + ": " + ", ".join(map(str, self.states)) + " /"