class State:
	def __init__(self, item):
		self.name = ""
		self.inn = None

		part = item.split("{")
		if len(part) > 1:
			self.name = part[0]
			if len(part) != 1:
				self.inn = part[1][:-1]
		else:
			self.inn = part[0]

	def __repr__(self):
		return str(self)

	def __str__(self):
		if self.name:
			return self.name + "{" + self.inn + "}"
		else:
			return "{" + self.inn + "}"

	def __lt__(self, other):
		return str(self) < str(other)