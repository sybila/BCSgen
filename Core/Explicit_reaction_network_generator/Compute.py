from Reaction import *

def sortInitialState(initialState):
	return map(str, map(Reactant, initialState))

class Compute:
	def __init__(self):
		self.reactants = set()
		self.reactions = list()
		self.agents = dict()
		self.usedStates = list()
		self.tmpResult = list()
		self.middle = 0

	def computeReactions(self, reactions):
		self.parse(reactions)
		return self.CreateReactions()

	def parse(self, reactionList):
		for reactionLine in reactionList:
			reaction = Reaction(reactionLine)
			self.reactions.append(reaction)

			self.reactants.update(set(reaction.reactants))

			for item in reaction.reactants:
				for agent in item.agents:
					self.agentToDictionary(agent)

	def agentToDictionary(self, agent):
		if agent.states:
			if agent.name not in self.agents:
				dictionaryOfStates = dict()
				for state in agent.states:
					dictionaryOfStates[state.name] = set([state.inn])
				self.agents[agent.name] = dictionaryOfStates
			else:
				dictionaryOfStates = self.agents[agent.name]
				for state in agent.states:
					if state.name in dictionaryOfStates:  
						setOfInnerStates = dictionaryOfStates[state.name]
					else:
						setOfInnerStates = set()
					
					setOfInnerStates.add(state.inn)
					dictionaryOfStates[state.name] = setOfInnerStates
					self.agents[agent.name] = dictionaryOfStates

	def AddKeyToList(self, agent, key, inn):
		outputList = []
		if key != self.agents[agent.name].keys()[-1]:
			if not inn:
				outputList.append(key + ",")
			else:
				outputList.append(key + "{" + inn + "},")
		else:
			if not inn:
				outputList.append(key)
			else:
				outputList.append(key + "{" + inn + "}")

		return outputList

	def AddItemToList(self, item):
		self.usedStates.append(-1)
		return [item]

	def CreateReactions(self):
		OutputReactions = []

		for reaction in self.reactions:
			self.usedStates = []
			alphabet = []
			a = 1
			i = 0
			tmplist2 = []
			if i == reaction.left:
				tmplist2.append(" => ")
				self.middle = len(alphabet) + 1
				alphabet.append(tmplist2)
				self.usedStates.append(-1)
			for reactant in reaction.reactants:
				i += 1
				for agent in reactant.agents:
					alphabet.append(self.AddItemToList(agent.name))
					if agent.name in self.agents:
						for key in self.agents[agent.name].keys():
							tmplist = []
							contains = False
							normalState = True
							inn = ""
							if agent.states:
								for agentState in agent.states:
									if agentState.name == key:
										contains = True
										inn = agentState.inn
									if agentState.name == "":
										normalState = False

								if contains:
									if normalState and key == self.agents[agent.name].keys()[0]:
										alphabet.append(self.AddItemToList("("))

									tmplist += self.AddKeyToList(agent, key, inn)
									alphabet.append(tmplist)
									self.usedStates.append(-1)

									if key == self.agents[agent.name].keys()[-1] and normalState:
										alphabet.append(self.AddItemToList(")"))
									continue

							if normalState and key != "" and key == self.agents[agent.name].keys()[0]:
								alphabet.append(self.AddItemToList("("))

							for state in self.agents[agent.name][key]:
								tmplist += self.AddKeyToList(agent, key, state)
							alphabet.append(tmplist)
							self.usedStates.append(a)
							a += 1
							if key == self.agents[agent.name].keys()[-1] and normalState and key != "":
								alphabet.append(self.AddItemToList(")"))

					if reactant.agents[-1] != agent:
						alphabet.append(self.AddItemToList("."))
					else:
						alphabet.append(self.AddItemToList("::" + reactant.compartment))

				tmplist2 = []
				if i == reaction.left:
					tmplist2.append(" => ")
					self.middle = len(alphabet) + 1
				elif i == len(reaction.reactants):
					tmplist2.append("")
				else:
					tmplist2.append(" + ")
				alphabet.append(tmplist2)
				self.usedStates.append(-1)

			self.tmpResult = []
			self.Combinations(len(alphabet), "", alphabet)
			OutputReactions += self.tmpResult

		return OutputReactions

	def Combinations(self, rest, result, alphabet):
		#print alphabet
		if rest > 0:
			for letter in alphabet[len(alphabet) - rest]:
				steps = rest - 1
				if self.usedStates[len(alphabet) - rest] > 0 and len(alphabet) - rest < self.middle:
					newAlphabet = []
					j = 0
					for i in range(len(alphabet)):
						if i > self.middle and self.usedStates[i] > 0:
							j += 1
							if j == self.usedStates[len(alphabet) - rest]:
								newAlphabet.append([letter])
							else:
								newAlphabet.append(alphabet[i])
						else:
							newAlphabet.append(alphabet[i])
					self.Combinations(steps, result + letter, newAlphabet)
				else:
					self.Combinations(steps, result + letter, alphabet)
		else:
			self.tmpResult.append(result)
