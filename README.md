# BCSgen <img src="https://gitlab.fi.muni.cz/xtrojak/BCSgen/raw/f86b612af8a8d1f53eefad9ed680b1666398aa5c/GUI/icons/128x128.png" width="64">  

Biochemical Space language software tool

---

This tool serves for interpreting basic functionality to maintain Biochemical Space language. It provides __state space__ and __reactions__ generating which can be used for analysis and visualisation<sup>1</sup>.

## Graphical User Interface

The most proper way is to run the [binary file](https://gitlab.fi.muni.cz/xtrojak/BCSgen/tags/v2.0) with __Graphical User Interface__ suitable for your platform.

<div align="center">
  <img src="http://i.imgur.com/qLJlAHu.png"><br><br>
</div>

To obtain __state space__:
* Choose State space file - JSON file for storing generated state space,
* press Compute button.

To obtain __reactions__:
* Choose Reactions file - text file for storing reactions,
* press Compute button<sup>3</sup>.
  
---

If binary file is not working, build __Graphical User Interface__<sup>4</sup> (in GUI directory) by running:

    python gui.py
    
## Command Line Interface

Alternatively, CLI can be used.

* enter Model directory (serves as user's workspace),
* write your model as rules and initial conditions (into model.bcs),
* to obtain __state space__, run script:

        python state_space.py <model> <stateSpaceFile>
        
    * model - given BCS model
    * stateSpaceFile - JSON file for storing generated state space

* to obtain __reactions__, run script:

        python reaction_network.py <model> <reactionsFile>
        
    * model - given BCS model<sup>3</sup>
    * reactionsFile - text file for storing reactions

> in Examples directory, there are several models, to run them just use 'python example.py'

---
> <sup>1</sup> State space might be visualised with [this](https://github.com/mathooo/NetworkVISUAL) utility.

> <sup>2</sup> [BCS model](http://sybila.fi.muni.cz/tools/bcsgen#bcsl_model) is simple text file format containing initialized model, i.e. set of rules and initial state. Examples of such models are in Examples directory.

> <sup>3</sup> Additionally, some static analysis about conflicts in the model are computed. In GUI, you can disable this feature by checking `Ignore conflicts` checkbox.

> <sup>4</sup> To do it, you need to have [PyQt](https://wiki.python.org/moin/PyQt) python library installed. 
For Windows, use [this](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) binary file, for Unix machines use [following](http://pythoncentral.io/install-pyside-pyqt-on-windows-mac-linux/) instructions.
Moreover, additional python packages are required (markdown, numpy) and might be installed using `pip`.
