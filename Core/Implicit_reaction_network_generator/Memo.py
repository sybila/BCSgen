from State import *

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
    :param candidate_rule_hash: hash calculated from a candidate and a rule
    :param candidates: given list of candidates
    """
    def addRecord(self, candidate_rule_hash, candidates):
        new_candidates = map(lambda candidate: self.translateToHashes(candidate), candidates)
        self.records[candidate_rule_hash] = new_candidates

    """
    Checks if a hash is already in the dictionary of records
    :param candidate_rule_hash: hash calculated from a candidate and a rule
    :return: True if the has is in the list
    """
    def isInRecords(self, candidate_rule_hash):
        return candidate_rule_hash in self.records

    """
    Returns candidates from dictionary of records
    :param candidate_rule_hash: hash calculated from a candidate and a rule
    :return: list of candidates produced by rule applied to input candidate (encoded in the hash)
    """
    def getRecord(self, candidate_rule_hash):
        return map(lambda hashes: self.translateFromHashes(hashes), self.records[candidate_rule_hash])

    """
    Translates every agent from candidate to hash and adds it to dictionary of agents
    :param candidate: given list of agents
    :return: list of hashes
    """
    def translateToHashes(self, candidate):
        hashes = []
        for agent in candidate:
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
