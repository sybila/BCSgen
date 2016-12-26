# BCSgen
Biochemical Space language software tool

---

This tool serves for interpreting basic functionality to maintain Biochemical Space language. It provides __state space__ and __reactions__ generating which can be used for analysis and visualisation<sup>1</sup>.

## Graphical User Interface

The most proper way is to use __Graphical User Interface__<sup>2</sup> (in GUI directory).

Run it by:

    python gui.py
    
and fill required fields:

* Input
 * Model - file containing a BCS model<sup>3</sup>
* Output
 * Vertices - file for storing states of state space
 * Edges - file for storing edges of state space
 * Reactions - file for storing reactions

## Command Line Interface

1. enter Model directory (serves as user's workspace),
2. write your model as rules and initial conditions (into model.bcs),
3. to obtain __state space__, run script:

        python state_space.py <model> <statesFile> <edgesFile>
        
  where:
    * model - given BCS model<sup>3</sup>
    * statesFile - file for storing states of state space
    * edgesFile - file for storing edges of state space
    
4. to obtain __reactions__, run script:

        python reaction_network.py <model> <reactionsFile>
        
   where:
     * model - given BCS model<sup>3</sup>
     * reactionsFile - file for storing reactions

> in Examples directory, there are several models, to run them just use 'python example.py'

---
> <sup>1</sup> State space might be visualised with [this](https://github.com/mathooo/NetworkVISUAL) utility.

> <sup>2</sup> To execute it, you need to have [Tkinter](https://wiki.python.org/moin/TkInter) python library installed (usually in default library).

> <sup>3</sup> BCS model is simple text file format containing initialized model, i.e. set of rules and initial state. Examples of such models are in Examples directory.
