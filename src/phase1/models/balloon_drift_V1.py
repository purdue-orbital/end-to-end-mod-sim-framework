# Import standard external libraries and imports
import numpy as np
import pyquaternion as quat 
from dataclasses import dataclass
import datetime as t
import random as rand
import scipy.integrate as integrate
import typing as ty


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
    vars_dot[0] = vars[3]
    vars_dot[1] = vars[4]
    vars_dot[2] = vars[5]
    vars_dot[3] = rand.uniform(-0.01, 0.025)
    vars_dot[4] = rand.uniform(-0.01, 0.02)
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

    balloon_data = EphemerisDataStruct_Balloon()
    balloon_data.init_time = inputs.launch_date
    balloon_data.duration = inputs.launch_duration
    #TODO: develop a method to convert lla to cartesian and establish reference frames
    # First 3 values: x, y, z [meters]
    # Second 3 values: vx, vy, vz [m/s]
    balloon_data.pos_vel = inputs.launch_location_cart
    balloon_data.pos_vel = np.append(balloon_data.pos_vel, [0, 0, 0])
    balloon_data.time = 0

    dat = balloon_data

    integration_obj = integrate.RK45(balloon_EOM, 0, dat.pos_vel, dat.duration)

    while integration_obj.status == 'running':
        integration_obj.step()
        dat.pos_vel = np.append(dat.pos_vel, integration_obj.y)
        dat.time = np.append(dat.time, integration_obj.t)

    dat.pos_vel = dat.pos_vel.reshape((int(len(dat.pos_vel)/6), 6))

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
