# Import standard external libraries and imports
import numpy as np
import pyquaternion as quat 
from dataclasses import dataclass
import datetime as t
import typing as ty

# Import external files and functions
import sys
sys.path.append('../phase1/models/')
sys.path.append('../phase2/models/')
sys.path.append('../phase3/models/')
import user_input
from balloon_drift_V1 import balloon_model_V1
from balloonEphemerisWriter import balloonEphemerisWriter


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
    drift_altitude = 25000
    
    # TODO: develop a 3dof model for launch platform ascent
    
    initial_pos_vel = [0, 0, 0, 0, 0, 0]

    transition_data = FinalStateDataStruct(inputs.launch_date, initial_pos_vel)
    transition_data.refFrame = referenceFrame('inertial', 'balloon body')
    transition_data.current_pos_vel = transition_data.refFrame.inertial_to_balloon_body(transition_data)

    balloon_data_out = balloon_model_V1(inputs)
    
    transition_data.current_pos_vel = balloon_data_out.pos_vel[-1][0:6]
    transition_data.current_time = balloon_data_out.time[-1]
    
    transition_data.model_run_status = 'Success'

    balloonEphemerisWriter('6 Aug 2021 23:59:42.000000', balloon_data_out.pos_vel, balloon_data_out.time, 'balloon')

    return transition_data, balloon_data_out


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
class FinalStateDataStruct:
    """ 
    Establishes a standardized data structure class to create objects for
    final model data, which can be passed between models (e.i. balloon to rocket)
    """
    current_time: ty.Optional[t.datetime] = None
    current_pos_vel: ty.Optional[np.array] = None
    current_attitude: ty.Optional[quat.Quaternion] = None
    current_model: ty.Optional[str] = None
    model_run_status: ty.Optional[str] = None
    refFrame: ty.Optional[object] = None


@dataclass
class referenceFrame:
    """ 
    Establishes a standardized data structure class to create common reference frame
    as a subclass of FinalStateDataStruct which can be easily compared, fetched, output,
    and passed between functions/files
    """
    current_frame: ty.Optional[str] = None
    desired_frame: ty.Optional[str] = None

    def inertial_to_balloon_body(self, object):
        # TODO - develop rotation matrices
        new_pos_vel = object.current_pos_vel + np.array([1, 0, 1, 0, 0, 1])
        return new_pos_vel


if "__main__":
    """
    Primary code that runs when master.py is run from terminal

    All high-level framework logic and flow should be defined here
    """
    inputs = user_input.user_input()
    if inputs.mode == 1:
        final_balloon_data, balloon_ephemeris = single_run_launch_platform_6dof(inputs)
        if final_balloon_data.model_run_status == 'Failed':
            print('Run failed!')
        elif final_balloon_data.model_run_status == 'Success':
            print("\nRun succeeded!")
            print("\nAt time {} mins balloon is:".format(final_balloon_data.current_time/60))
            print("x-position = {} km".format(final_balloon_data.current_pos_vel[0]/1000))
            print("y-position = {} km".format(final_balloon_data.current_pos_vel[1]/1000))
            print("z-position = {} km".format(final_balloon_data.current_pos_vel[2]/1000))
            print("x-velocity = {} m/s".format(final_balloon_data.current_pos_vel[3]))
            print("y-velocity = {} m/s".format(final_balloon_data.current_pos_vel[4]))
            print("z-velocity = {} m/s".format(final_balloon_data.current_pos_vel[5]))
