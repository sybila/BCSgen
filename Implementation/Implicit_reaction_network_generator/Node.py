import collections

class Node:
	def __init__(self, header):
		self.header = header
		self.bucket = collections.Counter([])