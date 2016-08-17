# BCSgen
Biochemical Space language software tool

This tool serves for interpreting basic functionality to maintain Biochemical Space language. It provides several utilities:

**Explicit State space generator**

To generate state space of a model, the most proper way is to edit state_space.py file in the Explicit_state_space_generator folder as following (untill import is done):

* define agents, rules and (if any) states of your model,
* set parallel and memoization attributes to True/False in case want/don't want to use them,
* set initial state(s), rules, output files names (vertices and edges) and boundary of the model (in case of potentially infinite state space),
* run the file (python state_space.py).

For an example, see examply.py file.

**Explicit Reaction network generator**

To generate reaction network explicitely, use following insturctions:

* in folder Explicit_reaction_network_generator, run the script explicit.py with the following parameters:
  * input vertices - from State space generator
  * input edges - from State space generator
  * output vertices - file name
  * output reactions - file name
  
**Implicit Reaction network generator**

- in development
