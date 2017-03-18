class State:
	def __init__(self, item):
		self.name = None # ""
		self.inn = None

		part = item.split("{")
		if len(part) > 1:
			self.name = part[0]
			if len(part) != 1:
				self.inn = part[1][:-1]
		else:
			self.inn = part[0]