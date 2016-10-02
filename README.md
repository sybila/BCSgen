# BCSgen
Biochemical Space language software tool

This tool serves for interpreting basic functionality to maintain Biochemical Space language. It provides several utilities:

## Explicit State space generator

To generate state space of a model, the most proper way is to edit state_space.py file in the Explicit_state_space_generator folder as following (untill import is done):

1. define agents, rules and (if any) states of your model,
2. set parallel<sup>1</sup> and memoization attributes to True/False in case want/don't want to use them,
3. set initial state(s), rules, output files names (vertices and edges) and boundary of the model (in case of potentially infinite state space),
4. run the file (python state_space.py).

> For an example, see example.py file.

## Explicit Reaction network generator

To generate reaction network explicitely, use following insturctions:

1. in folder Explicit_reaction_network_generator, run the script explicit.py with the following parameters:
  * input vertices - from State space generator
  * input edges - from State space generator
  * output vertices - file name
  * output reactions - file name
  
Example

 `python explicit.py vertices.txt edges.txt reactants.txt reactions.txt`

**Implicit Reaction network generator**

- in development
- works similarly to state space generator but it has output of explicit reaction network generator

> Both state space or reaction network might be visualised with [this](https://github.com/mathooo/NetworkVISUAL) utility.

> <sup>1</sup> IN order to use parallel computing, you need to install [pathos](https://github.com/uqfoundation/pathos) library (use pip install git+https://github.com/uqfoundation/pathos.git@master on linux machines)
