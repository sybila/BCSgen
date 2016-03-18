import sys
import os
sys.path.append(os.path.abspath('../Interpreter of BCS language '))
from Rule import *
from Edge import *

class Memo:
    def __init__(self):
        self.records = dict([])
        self.agents = dict([])

    """
    Adds new record to the dictionary of records
    :param solution_rule_hash: hash calculated from a solution and a rule
    :param solutions: given list of solutions
    """
    def addRecord(self, solution_rule_hash, solutions):
        new_solutions = map(lambda solution: self.translateToHashes(solution), solutions)
        self.records[solution_rule_hash] = new_solutions

    """
    Checks if a hash is already in the dictionary of records
    :param solution_rule_hash: hash calculated from a solution and a rule
    :return: True if the has is in the list
    """
    def isInRecords(self, solution_rule_hash):
        return solution_rule_hash in self.records

    """
    Returns solutions from dictionary of records
    :param solution_rule_hash: hash calculated from a solution and a rule
    :return: list of solutions produced by rule applied to input solution (encoded in the hash)
    """
    def getRecord(self, solution_rule_hash):
        return map(lambda hashes: self.translateFromHashes(hashes), self.records[solution_rule_hash])

    """
    Translates every agent from solution to hash and adds it to dictionary of agents
    :param solution: given list of agents
    :return: list of hashes
    """
    def translateToHashes(self, solution):
        hashes = []
        for agent in solution:
            my_hash = hash(agent)
            self.agents[my_hash] = agent
            hashes.append(my_hash)
        return hashes

    """
    Translates every hash to agent
    :param hashes: list of hashes
    :return: list of agents
    """
    def translateFromHashes(self, hashes):
        return map(lambda the_hash: self.agents[the_hash], hashes)
