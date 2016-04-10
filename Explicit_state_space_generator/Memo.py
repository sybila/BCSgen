import sys
import os
sys.path.append(os.path.abspath('../Interpreter of BCS language '))
from Rule import *
from Edge import *

"""
Connects two memos to one memo
:param memos: input list of memos
:return: one memo containing all records
"""
def connect_memos(memos):
    m = Memo()
    for memo in memos:
        m = connect_two_memos(m, memo)
    return m

"""
Connects two memos
:param first: first memo
:param second: second memo
:return: connected memo
"""
def connect_two_memos(first, second):
    first.getRecords().update(second.getRecords())
    first.getAgents().update(second.getAgents())
    return first

class Memo:
    def __init__(self, records = [], agents = []):
        self.records = dict(records)
        self.agents = dict(agents)

    def getRecords(self):
        return self.records

    def getAgents(self):
        return self.agents

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Records: " + self.records.__str__() + "\n" + "Agents: " + self.agents.__str__() + "\n"

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
