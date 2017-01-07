# BCSgen
Biochemical Space language software tool

---

This tool serves for interpreting basic functionality to maintain Biochemical Space language. It provides __state space__ and __reactions__ generating which can be used for analysis and visualisation<sup>1</sup>.

## Graphical User Interface

The most proper way is to use __Graphical User Interface__<sup>2</sup> (in GUI directory).

<div align="center">
  <img src="http://i.imgur.com/VnFpmuj.png"><br><br>
</div>

Run it by:

    python gui.py
    
To obtain __state space__:
* fill 
  * Model - file containing a BCS model<sup>3</sup>
  * State space file - JSON file for storing generated state space
  
and press Compute button. The state space is consequently saved in choosen file.

To obtain __reactions__:
* fill 
  * Model - file containing a BCS model<sup>3</sup>
  * Reactions file - text file for storing reactions
  * Save log<sup>4</sup> (optional)

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

---
> <sup>1</sup> State space might be visualised with [this](https://github.com/mathooo/NetworkVISUAL) utility.

> <sup>2</sup> To execute it, you need to have [PyQt](https://wiki.python.org/moin/PyQt) python library installed (usually in default library).

> <sup>3</sup> BCS model is simple text file format containing initialized model, i.e. set of rules and initial state. Examples of such models are in Examples directory.

> <sup>4</sup> During computation, static analysis is applied to the model in order to detect some conflicts in rules. These conflict might be saved in a log file.

> In order to disable useless stderr command line output, use 2> /dev/null (UNIX machines) or 2> nul (Windows machines). Otherwise, ignore those messages.
