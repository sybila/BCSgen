from Reactant import *

class Reaction:
	def __init__(self, line):
		self.name = line
		self.left = len(filter(None, line.split("=>")[0].split("+")))
		line = line.replace("=>", "+")
		self.reactants = map(Reactant, filter(None, line.split("+")))

	def __repr__(self):
		return str(self)

	def __str__(self):
		return " + ".join(map(str, self.reactants[:self.left])) + " => " + " + ".join(map(str, self.reactants[self.left:]))