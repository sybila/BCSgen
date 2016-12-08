import collections
from Reaction import *

class Edge:
	def __init__(self, From, To, bucket):
		self.From = From 			# list of Nodes
		self.To = To 				# list of Nodes
		self.bucket = set(bucket) 	# set of Reactions