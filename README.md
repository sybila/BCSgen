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
 * State space file - JSON file for storing generated state space
 * Reactions file - text file for storing reactions
 
> __Short tutorial__: Fill all the required fields and press _Compute_ button. Then, [analysis](https://github.com/sybila/BCSgen#note) is applied. Computation is completed when _Compute_ button changes to _Finish_ button. The process can be cancelled by pressing _Cancel_ button only before the computation starts.

## Command Line Interface

1. enter Model directory (serves as user's workspace),
2. write your model as rules and initial conditions (into model.bcs),
3. to obtain __state space__, run script:

        python state_space.py <model> <stateSpaceFile>
        
  where:
    * model - given BCS model<sup>3</sup>
    * stateSpaceFile - JSON file for storing generated state space
    
4. to obtain __reactions__, run script:

        python reaction_network.py <model> <reactionsFile>
        
   where:
     * model - given BCS model<sup>3</sup>
     * reactionsFile - text file for storing reactions

> in Examples directory, there are several models, to run them just use 'python example.py'

#### Note

During computation, static analysis is applied to the model in order to detect some conflicts in rules. If there are such conflicts, they are announced and the user is asked whether continue (generate state space) or stop (save conflicts in log file and exit) the computation.

---
> <sup>1</sup> State space might be visualised with [this](https://github.com/mathooo/NetworkVISUAL) utility.

> <sup>2</sup> To execute it, you need to have [Tkinter](https://wiki.python.org/moin/TkInter) python library installed (usually in default library).

> <sup>3</sup> BCS model is simple text file format containing initialized model, i.e. set of rules and initial state. Examples of such models are in Examples directory.
