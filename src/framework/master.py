# Import standard external libraries and imports
import numpy as np
import pyquaternion as quat 
from dataclasses import dataclass
import datetime as t

# Import external files and functions
import user_input


def single_run_launch_platform_6dof(inputs):
    """
    Description: Function to call and execute a single run of the 6DOF balloon model

    Inputs:
    - Weather Model to use (historical data or live day-of data)
    
    Outputs:
    - instance of data class structure

    Raises:
    - None yet
    """
    current_model = 'Balloon Drift'
    
    # TODO: develop a 6dof model for launch platform ascent
    
    drift_altitude = 25000
    final_pos_vel = [0, 0, drift_altitude, 0, 0, 0]
    final_orient = [0, 0, 0, 0]
    run_result = 'Success'

    balloon_data_out = EphemerisDataStruct(inputs.launch_date, final_pos_vel, final_orient, current_model, run_result)
    balloon_ref_frame = balloon_data_out.referenceFrame('inertial', 'balloon fixed')
    balloon_data_out.current_position_and_velocity = balloon_ref_frame.inertial_to_balloon_body()

    return balloon_data_out


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
    current_position_and_velocity: list[float]
    current_attitude: quat.Quaternion
    current_model: str
    model_run_status: str

    def __post_init__(self):
        self.refFrame = referenceFrame()

@dataclass
class referenceFrame:
    """ 
    Establishes a standardized data structure class to create common reference frame
    as a subclass of EphemerisDataStruct which can be easily compared, fetched, output,
    and passed between functions/files
    
    """
    current_frame: str
    desired_frame: str

    def inertial_to_balloon_body(self):
        # TODO - develop rotation matrices
        new_position_and_velocity = self.current_position_and_velocity
        return new_position_and_velocity



if "__main__":
    """
    Primary code that runs when master.py is ran    

    All high-level framework logic and flow should be defined here

    """
    inputs = user_input.user_input()
    if inputs.mode == 1:
        run_status, drift_altitude = single_run_launch_platform_6dof(inputs)
        if run_status == 'Failed':
            print('Run failed!')
        elif run_status == 'Success':
            print('\nRun succeeded!')
            print("\nBalloon drifted to an altitude of {} km".format(drift_altitude))
