# BCSgen <img src="https://gitlab.fi.muni.cz/xtrojak/BCSgen/raw/f86b612af8a8d1f53eefad9ed680b1666398aa5c/GUI/icons/128x128.png" width="64">  

Biochemical Space language software tool

---

This tool serves for interpreting basic functionality to maintain Biochemical Space language. It provides __state space__ generating which can be used for analysis and visualisation.

## Graphical User Interface

The most proper way is to run the [binary file](https://gitlab.fi.muni.cz/xtrojak/BCSgen/tags/v2.1) with __Graphical User Interface__ suitable for your platform.

<div align="center">
  <img src="http://i.imgur.com/7g2zp9Z.png"><br><br>
</div>

To obtain __state space__:
* write BCS model<sup>1</sup> (or load it from a file),
* choose State space file - JSON file for storing generated state space,
* press Compute button.

To compute __reachability__:
* set entities (with their stoichiometry),
* press Check reachability button.

---

If binary file is not working, build __Graphical User Interface__<sup>2</sup> (in GUI directory) by running:

    python gui.py <PathToParser>
    
* PathToParser - path where RuleParser is located<sup>3</sup>
    
## Command Line Interface

Alternatively, CLI can be used.

* enter CLI directory (serves as user's workspace),
* write your BCS model into a `.bcs` file,
* to obtain __state space__, run script:

        python state_space.py <model.bcs> <stateSpaceOutputFile.json>
        
    * model.bcs - given BCS model
    * stateSpaceOutputFile.json - JSON file for storing generated state space

---

> <sup>1</sup> [BCS model](http://sybila.fi.muni.cz/tools/bcsgen#bcsl_model) is simple text file format containing initialized model, i.e. set of rules and initial state. Examples of such models are in Examples directory.

> <sup>2</sup> To do it, you need to have [PyQt](https://wiki.python.org/moin/PyQt) python library installed. 
For Windows, use [this](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4) binary file, for Linux use [following](http://pythoncentral.io/install-pyside-pyqt-on-windows-mac-linux/) instructions, and for Mac OS use [this](https://sourceforge.net/projects/pyqtx/) installer (with all requirements). Next, [matplotlib](https://matplotlib.org/users/installing.html) is required for plotting simulation results.
Moreover, additional python packages are required (markdown, numpy, sympy, scipy) and might be installed using `pip`.

> <sup>3</sup> [RuleParser](https://gitlab.fi.muni.cz/grp-sybila/rule-parser) improves writing and allows validation of BCSL models inside BCSgen. Therefore path to directory with `RuleParser.py` and `_RuleParser.so` must be specified (alternatively, both files might be placed in Core/Import/ directory).

> `On Linux machines, linux_install.sh script can be used in order to install all required packages.`
