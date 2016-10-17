# BCSgen
Biochemical Space language software tool

This tool serves for interpreting basic functionality to maintain Biochemical Space language. It provides several utilities:

## Explicit State space generator

To generate state space of a model, the most proper way is:

1. enter Model directory (serves as user's workspace),
2. write your model as rules (into rules.txt) and initial conditions (into initial_cond.txt),
3. run script:

 `python state_space.py bound memoization parallel`

 where 
 * bound (Interger) - indicates maximal bound of the model
 * memoization (True/False) - True if you want to apply memoization during computation
 * parallel<sup>1</sup> (True/False) - True if you want to apply parallel cumputing

> in Example directory, there are several models, to run them just use 'python example.py'

## Explicit Reaction network generator

To generate reaction network explicitely, use following insturctions:

in Model directory, run the script reaction_network.py with the following parameters:
* input vertices - from State space generator
* input edges - from State space generator
* output vertices - file name
* output reactions - file name
  
Example

 `python reaction_network.py outputs/vertices.txt outputs/edges.txt network/reactants.txt network/reactions.txt`

**Implicit Reaction network generator**

- in development
- works similarly to state space generator but it has output of explicit reaction network generator

---

> Both state space or reaction network might be visualised with [this](https://github.com/mathooo/NetworkVISUAL) utility.

> <sup>1</sup> In order to use parallel computing, you need to use [anaconda](http://conda.pydata.org/docs/install/quick.html) (Python distribution) and install [pathos](https://github.com/uqfoundation/pathos) library (use pip install git+https://github.com/uqfoundation/pathos.git@master on __unix machines__ (including Linux and OS X) — it should install all dependencies required by the package. Under __Windows__, multiprocessing is [not supported](http://i.imgur.com/s3OimLn.png).

> **WARNING**: Installing anaconda python distribution will replace your default python distribution (which can be usually found and still used in /usr/bin/).
