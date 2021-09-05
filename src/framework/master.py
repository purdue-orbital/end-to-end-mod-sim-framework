# Import standard external libraries and imports
import numpy as np
from dataclasses import dataclass
import datetime as t

# Import external files and functions
import user_input


def single_run_launch_platform_6dof(weather_model):
    """
    Description: Function to call and execute a single run of the 6DOF balloon model

    Inputs:
    - Weather Model to use (historical data or live day-of data)
    
    Outputs:
    - instance of data class structure

    Raises:
    - None yet
    """
    
    # TODO: develop a 6dof model for launch platform ascent

    run_result = 1
    drift_altitude = 25000
    return run_result, drift_altitude


def single_run_rocket_ascent_trajectory():
    """
    Description: Function to call and execute a single run of the 6DOF balloon model

    Inputs:
    - Weather Model to use (historical data or live day-of data)
    
    Outputs:
    - instance of data class structure

    Raises:
    - None yet
    """
    
    # TODO: develop a script to interface with and run ASTOS

    outputs = 1
    return outputs


def single_run_orbit_propagation():
    """
    Description: Function to call and execute a single run of the 6DOF balloon model

    Inputs:
    - Weather Model to use (historical data or live day-of data)
    
    Outputs:
    - instance of data class structure

    Raises:
    - None yet
    """
    
    # TODO: develop a script to interface with and run STK
    
    outputs = 1
    return outputs


def dispersion_analysis():
    
    # TODO: develop logic to run a set of models in sequence, randomly varying all relevant parameters

    outputs = 1
    return outputs


def trade_study_XXX():
    
    # TODO: develop logic to run a set of models in sequence, varying only targeted parameters to investigate effects
    # create multiple functions to consider multiple trade study options

    outputs = 1
    return outputs

@dataclass
class EphemerisDataStruct:
    """ 
    Establishes a standardized data structure class to create common data object instances
    which can be easily compared, fetched, output, and passed between functions/files
    
    """
    current_time: t.datetime
    current_ref_frame: str
    current_position_and_velocity: list[float]
    current_attitude: list[float]


if "__main__":
    """
    Primary code that runs when master.py is ran    

    All high-level framework logic and flow should be defined here

    """
    inputs = user_input.user_input()
    if inputs.mode == 1:
        run_status, drift_altitude = single_run_launch_platform_6dof(inputs.weather_model)
        if run_status == -1:
            print('Run failed!')
        elif run_status == 1:
            print('\nRun succeeded!')
            print("\nBalloon drifted to an altitude of {} km".format(drift_altitude))
