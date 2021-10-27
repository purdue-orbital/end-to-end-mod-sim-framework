# end-to-end-mod-sim-framework (MASTRAB)
This Python modeling and simulation framework will integrate a variety of internal and external toolsets to target and model ephemeris and vehicle dynamics from balloon ground launch to orbital re-entry.

MASTRAB (Modeling and Simulation of Trajectories for Rocket and Balloon)

# Repo Structure
* src/ contains all actual python code and data sources for models
* docs/ contains relevant documentation and reference files
* external_libraries/ contains all external libraries and dependencies not obtainable through pip install or useful random functions
* .gitignore specifies all documents and folders that will not be version controlled or tracked by git

# Rules
* Always develop new code on a development branch, *NOT MAIN*
* Always create a Pull Request to merge your code into main
* All new code should have associated unit tests
* Follow the PEP8 Python style guide documented here: https://www.python.org/dev/peps/pep-0008/

# Phases
* phase 1 represents the mission phase beginning from the ground and ending with the launch platform and rocket being GO for launch
* phase 2 represents the mission phase beginning with the rocket launch and ending with orbit insertion
* phase 3 represents the mission phase beginning with orbit insertion and ending with orbit decay and deorbit


