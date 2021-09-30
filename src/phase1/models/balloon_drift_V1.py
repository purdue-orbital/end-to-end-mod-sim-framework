# Import standard external libraries and imports
import numpy as np
import pyquaternion as quat 
from dataclasses import dataclass
import datetime as t
import random as rand
import scipy.integrate as integrate
import typing as ty
from balloonEphemerisWriter import balloonEphemerisWriter


def balloon_force_models():
    """
    Function to define and calculate
    forces acting on balloon system
    """
    pass

    return


def balloon_EOM(t, vars):
    """
    Function to be numerically integrated.
    Contains state variable assignments 
    and calls to force model functions.
    """
    # First three values: vx, vy, vz [m/s]
    # Second three values: ax, ay, az [m/s^2]
    vars_dot = np.array([0, 0, 0, 0, 0, 0]).astype(float)
    # Assign derivatives of velocity equal to acceleration
    vars_dot[0] = vars[3]
    vars_dot[1] = vars[4]
    vars_dot[2] = vars[5]
    # Assign accelerations as a function of force models
    vars_dot[3] = rand.uniform(-0.01, 0.025)
    vars_dot[4] = rand.uniform(-0.02, 0.01)
    vars_dot[5] = rand.uniform(-0.01, 0.03)
    
    return vars_dot


def balloon_model_V1(inputs):
    """
    Description: Function to run a very simple balloon drift model

    Inputs:
    - TBD
    
    Outputs:
    - final position and velocity

    Raises:
    - None yet
    """

    # Initialize an instance of the data class to store data
    balloon_data = EphemerisDataStruct_Balloon()
    # Set the data objects launch date, launch duration, and initial state from inputs
    balloon_data.init_time = inputs.launch_date
    balloon_data.duration = inputs.launch_duration
    balloon_data.pos_vel = inputs.launch_init_state
    balloon_data.time = 0

    # Give the balloon data object a short handle (name) for easy future reference
    dat = balloon_data

    # Create an "integration object" of the SciPy libraries RK45 numerical integrator class
    # Provide the integrator the function to be run, initial pos_vel, and integration time
    integration_obj = integrate.RK45(balloon_EOM, 0, dat.pos_vel, dat.duration)

    # While the integration is still running, continue to step through integration
    while integration_obj.status == 'running':
        # Integrator chooses a step time dynamically based on observed patterns
        integration_obj.step()
        # At each time step, store the current state and time and append to ephemeris data struct
        dat.pos_vel = np.append(dat.pos_vel, integration_obj.y)
        dat.time = np.append(dat.time, integration_obj.t)

    # Once the integration is done, reshape the data struct to an n x 6 where n is the number of time steps
    dat.pos_vel = dat.pos_vel.reshape((int(len(dat.pos_vel)/6), 6))

    # Finally, send the full ephemeris data to function to create a balloon.e file for STK visualization
    balloonEphemerisWriter('6 Aug 2021 23:59:42.000000', dat.pos_vel, dat.time, 'balloon','Fixed')

    # Return data object structure for reference in main code
    return dat

@dataclass
class EphemerisDataStruct_Balloon:
    """ 
    Establishes a standardized data structure class to contain the
    full time range ephemeris for a single balloon model run
    """
    init_time: ty.Optional[t.datetime] = None
    duration: ty.Optional[t.datetime] = None
    time: ty.Optional[np.array] = None
    pos_vel: ty.Optional[np.array] = None
    attitude: ty.Optional[quat.Quaternion] = None
    model_run_status: ty.Optional[str] = None
    refFrame: ty.Optional[object] = None
