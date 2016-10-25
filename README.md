# BCSgen
Biochemical Space language software tool

This tool serves for interpreting basic functionality to maintain Biochemical Space language. It provides state space generating and subsequent reaction network abstraction which can be used for analysis and visualisation<sup>1</sup>. For instance, there is Example directory, where can be seen functionality applied on several models. Users might enter Model directory, which serves as user's workspace. Here, a model can be defined and generating utilities applied on it. 

## Explicit State space generator

1. To generate state space of a model, the most proper way is to use *Graphical User Interface*<sup>2</sup> (in GUI directory). Run it by:

 `python gui.py`

Alternatively use *Command Line Intereface*:

1. enter Model directory (serves as user's workspace),
2. write your model as rules (into rules.txt) and initial conditions (into initial_cond.txt),
3. run script:

 `python state_space.py bound memoization parallel`

 where 
 * bound (Interger) - indicates maximal bound of the model
 * memoization (True/False) - True if you want to apply memoization during computation
 * parallel<sup>3</sup> (True/False) - True if you want to apply parallel cumputing

> in Example directory, there are several models, to run them just use 'python example.py'

## Explicit Reaction network generator

To generate reaction network explicitely, use the following instructions:

1. in Model directory, run the script reaction_network.py with the following parameters:
* input vertices - from State space generator
* input edges - from State space generator
* output vertices - file name
* output reactions - file name
  
Example

`python reaction_network.py outputs/vertices.txt outputs/edges.txt network/reactants.txt network/reactions.txt`

## Implicit Reaction network generator

- in development
- works similarly to state space generator but it has output of explicit reaction network generator

---
> <sup>1</sup> To execute it, you need to have [Tkinter](https://wiki.python.org/moin/TkInter) python library installed. 

> <sup>2</sup> Both state space or reaction network might be visualised with [this](https://github.com/mathooo/NetworkVISUAL) utility.

> <sup>3</sup> In order to use parallel computing, you need to use [anaconda](http://conda.pydata.org/docs/install/quick.html) (Python distribution) and install [pathos](https://github.com/uqfoundation/pathos) library (use pip install git+https://github.com/uqfoundation/pathos.git@master on __unix machines__ (including Linux and OS X) — it should install all dependencies required by the package. Under __Windows__, multiprocessing is [not supported](http://i.imgur.com/s3OimLn.png).

> **WARNING**: Installing anaconda python distribution will replace your default python distribution (which can be usually found and still used in /usr/bin/).
