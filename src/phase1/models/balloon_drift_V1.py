# Import standard external libraries and imports
import numpy as np
import pyquaternion as quat 
from dataclasses import dataclass
import datetime as t
import random as rand
import scipy.integrate as integrate

def balloon_EOM(t, vars):
    """
    Function to be numerically integrated.
    Contains dynamics model of balloon system
    """
    # First three values: vx, vy, vz [m/s]
    # Second three values: ax, ay, az [m/s^2]
    vars_dot = np.array([0, 0, 0, 0, 0, 0])
    vars_dot[0] = vars[3]
    vars_dot[1] = vars[4]
    vars_dot[2] = vars[5]
    vars_dot[3] = 0.2
    vars_dot[4] = 0.5
    vars_dot[5] = 1
    
    return vars_dot

def balloon_model_V1():
    """
    Description: Function to run a very simple balloon drift model

    Inputs:
    - TBD
    
    Outputs:
    - final position and velocity

    Raises:
    - None yet
    """

    # First 3 values: x, y, z [meters]
    # Second 3 values: vx, vy, vz [m/s]
    initial_pos_vel = np.array([0, 0, 0, 0, 0, 1])

    integration_obj = integrate.RK45(balloon_EOM, 0, initial_pos_vel, 3600)

    while integration_obj.status == 'running':
        integration_obj.step()
        # if integration_obj.t % 1 == 0:
        # print(integration_obj.t)

    return integration_obj