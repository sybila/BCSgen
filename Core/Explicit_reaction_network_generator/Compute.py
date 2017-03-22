from Reaction import *

class Compute:
	def __init__(self):
		self.reactants = set()
		self.reactions = list()
		self.agents = dict()
		self.usedStates = list()
		self.tmpResult = list()
		self.middle = 0

	def computeReactions(self, reactions):
		# maybe remove white spaces
		self.parse(reactions)
		return self.CreateReactions()

	def parse(self, reactionList):
		for reactionLine in reactionList:
			reaction = Reaction(reactionLine)
			self.reactions.append(reaction)

			for item in reaction.reactants:
				if item not in self.reactants:
					self.reactants.add(item)

			for item in self.reactants:
				for agent in item.agents:
					self.agentToDictionary(agent)

	def agentToDictionary(self, agent):
		if agent.states:
			if agent.name not in self.agents:
				dictionaryOfStates = dict()
				for i in range(len(agent.states)):
					setOfInnerStates = set()
					setOfInnerStates.add(agent.states[i].inn)
					dictionaryOfStates[agent.states[i].name] = setOfInnerStates
				self.agents[agent.name] = dictionaryOfStates
			else:
				dictionaryOfStates = self.agents[agent.name]
				for i in range(len(agent.states)):
					setOfInnerStates = set()
					if agent.states[i].name in dictionaryOfStates:  
						setOfInnerStates = dictionaryOfStates[agent.states[i].name]
					
					setOfInnerStates.add(agent.states[i].inn)
					dictionaryOfStates[agent.states[i].name] = setOfInnerStates
					self.agents[agent.name] = dictionaryOfStates

	def AddKeyToList(self, agent, key, inn, inputList):
		outputList = inputList
		if not inn:
			if key != self.agents[agent.name].keys()[-1]:
				outputList.append(key + ",")
			else:
				outputList.append(key)
		else:
			if key != self.agents[agent.name].keys()[-1]:
				outputList.append(key + "{" + inn + "},")
			else:
				outputList.append(key + "{" + inn + "}")

		return outputList

	def AddItemToList(self, item, inputList):
		inputList.append([item])
		self.usedStates.append(-1)
		return inputList

	def CreateReactions(self):
		OutputReactions = []

		for reaction in self.reactions:
			self.usedStates = []
			alphabet = []
			a = 1
			i = 0
			for reactant in reaction.reactants:
				i += 1
				for agent in reactant.agents:
					alphabet = self.AddItemToList(agent.name, alphabet)
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
										alphabet = self.AddItemToList("(", alphabet)

									tmplist = self.AddKeyToList(agent, key, inn, tmplist)
									alphabet.append(tmplist)
									self.usedStates.append(-1)

									if key == self.agents[agent.name].keys()[-1] and normalState:
										alphabet = self.AddItemToList(")", alphabet)
									continue

							if normalState and key != "" and key == self.agents[agent.name].keys()[0]:
								alphabet = self.AddItemToList("(", alphabet)

							for state in self.agents[agent.name][key]:
								tmplist = self.AddKeyToList(agent, key, state, tmplist)
							alphabet.append(tmplist)
							self.usedStates.append(a)
							a += 1
							if key == self.agents[agent.name].keys()[-1] and normalState and key != "":
								alphabet = self.AddItemToList(")", alphabet)

					if reactant.agents[-1] != agent:
						alphabet = self.AddItemToList(".", alphabet)
					else:
						alphabet = self.AddItemToList("::" + reactant.compartment, alphabet)

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
			for result in self.tmpResult:
				OutputReactions.append(result)

		return OutputReactions

	def Combinations(self, rest, res, alphabet):
		#print alphabet
		#print len(alphabet), rest
		if rest > 0:
			for letter in alphabet[len(alphabet) - rest]: # is this correct ? always just one element
				steps = rest - 1
				if self.usedStates[len(alphabet) - rest] > 0 and len(alphabet) - rest < self.middle:
					newAlphabet = []
					j = 0
					for i in range(len(alphabet)):
						if i > self.middle and self.usedStates[i] > 0 and len(alphabet) - rest < self.middle:
							j += 1
							if j == self.usedStates[len(alphabet) - rest]:
								tmpList = []
								tmpList.append(letter)
								newAlphabet.append(tmpList)
							else:
								newAlphabet.append(alphabet[i])
						else:
							newAlphabet.append(alphabet[i])
					self.Combinations(steps, res + letter, newAlphabet)
				else:
					self.Combinations(steps, res + letter, alphabet)

			return ""
		else:
			self.tmpResult.append(res)
			return res
