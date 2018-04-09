class AtomicAgent(object):
	def __init__(self, name, state):
		self.name = name
		self.state = state

	def __repr__(self):
		return str(self)

	def __str__(self):
		return self.name + "{" + self.state + "}"

	def __lt__(self, other):
		return self.name < other.name

	def __eq__(self, other):
		return self.name == other.name and self.state == other.state

	def __hash__(self):
		return hash(str(self))

	def setState(self, newState):
		self.state = newState
