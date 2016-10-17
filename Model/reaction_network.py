import os

if not os.path.isdir('network/'):
    os.mkdir('network/')

execfile('../Explicit_reaction_network_generator/explicit.py')