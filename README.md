# BCSgen
Biochemical Space language software tool

This tool serves for interpreting basic functionality to maintain Biochemical Space language. It provides several utilities:

## Explicit State space generator

To generate state space of a model, the most proper way is:

1. go into folder Example,
2. write rules and initial_cond in appopriate text files (see inputs/ for an example),
3. in my_model.py, set parallel<sup>1</sup> and memoization attributes to True/False in case want/don't want to use them,
4. set boundary of the model (in case of potentially infinite state space),
4. run the file (python my_model.py).

> For an example, run python example.py file and see input in folder inputs and results in folder outputs

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

---

> Both state space or reaction network might be visualised with [this](https://github.com/mathooo/NetworkVISUAL) utility.

> <sup>1</sup> In order to use parallel computing, you need to use [anaconda](http://conda.pydata.org/docs/install/quick.html) (Python distribution) and install [pathos](https://github.com/uqfoundation/pathos) library (use pip install git+https://github.com/uqfoundation/pathos.git@master on __unix machines__ (including Linux and OS X) — it should install all dependencies required by the package. Under __Windows__, multiprocessing is [not supported](http://i.imgur.com/s3OimLn.png).

> **WARNING**: Installing anaconda python distribution will replace your default python distribution (which can be usually found and still used in /usr/bin/).
