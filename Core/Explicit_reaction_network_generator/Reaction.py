from Reactant import *

class Reaction:
	def __init__(self, line):
		self.name = line
		self.reactants = []

		self.left = len(line.split(" => ")[0].split(" + "))

		sides = line.replace(" => ", " + ")
		react = sides.split(" + ")

		for item in react:
			self.reactants.append(Reactant(item))

	def __repr__(self):
		return str(self)

	def __str__(self):
		return "Reaction - " + self.name + ": | " + ", ".join(map(str, self.reactants)) + " |"