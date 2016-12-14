import sys
from itertools import groupby

stateSpace1 = sys.argv[-2]
stateSpace2 = sys.argv[-1]

the_first_time = True

def getStates(inputFile):
	output = []
	with open(inputFile) as states:
		new_state = set()
		for line in states:
			line = line.rstrip()
			if line:
				if "vertex" in line:
					if new_state:
						output.append(new_state)
					new_state = set()
				else:
					new_state.add(line)
	output.append(new_state)
	return output

states1 = getStates(stateSpace1)
states2 = getStates(stateSpace2)

unique1 = []
for value in states1:
    if value not in unique1:
        unique1.append(value)

unique2 = []
difference = []
for value in states2:
    if value not in unique2:
        unique2.append(value)
    else:
    	difference.append(value)

print 'states 1: ', len(states1), len(unique1)
print 'states 2: ', len(states2), len(unique2)

print "\n".join(map(lambda state: str(state), difference))