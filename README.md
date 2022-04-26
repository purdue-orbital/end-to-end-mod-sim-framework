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

# Balloon Model Code
* user_input.py controls all input data, see "user_input_terminal" for all defined inputs like payload specifications, launch location, etc.
* main.py is the file you will run to execute analysis. It also coordinates high-level model runs. The definition of dispersion analysis, trade study, and single studies are all captured in this file along with the structure for the outputs (in the "main" section at the bottom of the file)
* For balloon model analysis, balloon_drift_V1.py is the core engine that controls balloon model drift prediction. There are a number of functions but the general logic is as follows:
** the function balloon_model_V1 controls and manages all the initial inputs and begins/manages the RK45 integrator process. Within this process, the function updates values related to Earthgram data and stores all data as ephemeris for future reference and plotting.
** balloon_EOM is the core physics engine that defines the functions to be numerically integrated. This function really only contains the variable assignments. This function collects earthgram data to be used at the current time step and sends all relevant data to the function balloon_force_models for actual physics calculations.
** balloon_force_models containts the core force calculations for bouyancy, gravity, and drag in all directions. 
** earthgram_points is responsible for constructing the spatial grid of data points which informs the function call_earthgram_func on where to obtain data points for future reference in the physics force models.
** call_earthgram_func configures all directionality and input data to be ready for the eventual call of the function get_earthgram_data, which manages the back-end earthgram calling and data fetching.

# Running the Balloon Model Code
* The first step to running the balloon model code is to ensure you have all of the proper dependencies and libraries installed through pip or annaconda. 
* After you have all the libraries installed, ensure you have the required Earthgram files stored in the correct file path (???)
* Configure input values in framework/user_input.py
* Run framework/main.py from the console by navigating to the files directory and running "python main.py"
* Enter "No" when asked to use the GUI (for future development)
* Once the drift model is done running (this may take a while) the balloon.e file saved in phase1/models will contain a data structure portable to STK for visualization


