# Import standard external libraries and imports
import sys
from dataclasses import dataclass
import datetime as t
import typing as ty
from importlib.machinery import SourceFileLoader
import numpy as np
import pyquaternion as quat

sys.path.append('../phase1/models/')
sys.path.append('../phase2/models/')
sys.path.append('../phase3/models/')
from balloon_drift_V1 import balloon_model_V1
from balloonEphemerisWriter import balloonEphemerisWriter
import user_input
datetime2STK = SourceFileLoader('datetime2STK', 'helper_functions/datetime2STK.py').load_module()


def single_run_launch_platform_3dof(inputs):
    """
    Description: Function to call and execute a single run of the 6DOF balloon model

    Inputs:
    - Weather Model to use (historical data or live day-of data)

    Outputs:
    - instance of data class structure

    Raises:
    - None yet
    """

    # Create a data structure to contain data to be passed between models
    transition_data = FinalStateDataStruct(inputs.launch_date, inputs.launch_init_state)

    # Pass the inputs to the balloon model code (function is in phase1/models)
    balloon_data_out = balloon_model_V1(inputs)

    # Set the final time step values from balloon model as the "current state"
    transition_data.current_pos_vel = balloon_data_out.output_ephem[-1][0:6]
    transition_data.current_time = balloon_data_out.time[-1]

    # If we make it to this point, seems like model ran successfully
    transition_data.model_run_status = 'Success'

    # return transitionary data structure as well as full balloon ephemeris
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

    #TODO: develop a script to interface with and run ASTOS

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

    #TODO: develop a script to interface with and run STK

    outputs = 1
    return outputs


def dispersion_analysis(inputs):

    dates = ['1 Jan 2021 00:00:00.000000',
             '1 Feb 2021 00:00:00.000000',
             '1 Mar 2021 00:00:00.000000',
             '1 Apr 2021 00:00:00.000000',
             '1 May 2021 00:00:00.000000',
             '1 Jun 2021 00:00:00.000000',
             '1 Jul 2021 00:00:00.000000',
             '1 Aug 2021 00:00:00.000000',
             '1 Sep 2021 00:00:00.000000',
             '1 Oct 2021 00:00:00.000000',
             '1 Nov 2021 00:00:00.000000',
             '1 Dec 2021 00:00:00.000000']

    for i in range(len(dates)):
        inputs.launch_date = datetime2STK.UTCG2datetime(dates[i])
        final_balloon_data_out, balloon_ephemeris = single_run_launch_platform_3dof(inputs)
        balloonEphemerisWriter(inputs.launch_date, balloon_ephemeris.pos_vel, balloon_ephemeris.time,
         'balloon_ephem_'+str(i),'Custom TopoCentric Facility/Launch')
        print('\nRun '+str(i)+' is complete')

    return balloon_ephemeris


def trade_study_XXX():

    #TODO: develop logic to run a set of models in sequence, varying only targeted parameters to investigate effects
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


if __name__ == "__main__":
    # Primary code that runs when master.py is run from terminal
    # All high-level framework logic and flow should be defined here

    inputs = user_input.user_input()
    # If user specifies mode = 1, they want a single run of balloon 3DoF model
    if inputs.mode == 1:
        # Assign the returned data from function to data structs
        final_balloon_data, balloon_ephemeris = single_run_launch_platform_3dof(inputs)
        # Finally, send the full ephemeris data to function to create a balloon.e file for STK visualization
        balloonEphemerisWriter(inputs.launch_date, balloon_ephemeris.output_ephem, balloon_ephemeris.time, 'balloon','ICEF')
        # If run failed, alert user
        if final_balloon_data.model_run_status == 'Failed':
            print('Run failed!')
        # If run was successful, provide relevant information to user
        elif final_balloon_data.model_run_status == 'Success':
            """
            print("\nRun succeeded!")
            print("\nAfter {} mins balloon is:".format(final_balloon_data.current_time/60))
            print("x-position = {} km".format(final_balloon_data.current_pos_vel[0]/1000))
            print("y-position = {} km".format(final_balloon_data.current_pos_vel[1]/1000))
            print("z-position = {} km".format(final_balloon_data.current_pos_vel[2]/1000))
            print("x-velocity = {} m/s".format(final_balloon_data.current_pos_vel[3]))
            print("y-velocity = {} m/s".format(final_balloon_data.current_pos_vel[4]))
            print("z-velocity = {} m/s".format(final_balloon_data.current_pos_vel[5]))
            """

    elif inputs.mode == 2:
        # Run sequence of runs
        balloon_ephemeris = dispersion_analysis(inputs)
