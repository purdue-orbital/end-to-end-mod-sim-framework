# Import standard external libraries and imports
from astropy.coordinates import earth
import numpy as np
import pyquaternion as quat 
from dataclasses import dataclass
import astropy.coordinates as coord
import datetime as t
import random as rand
import scipy.integrate as integrate
import typing as ty
from balloonEphemerisWriter import balloonEphemerisWriter
# Import global constants from main
from main import mass, coeff_drag, balloon_cross_area, balloon_volume, launch_time, EARTH_RADIUS


def cardinal_to_cart(_grid_out):

    for i in range(len(_grid_out.lat)):
        pass

    return wind_vel_cart

def earthgram_points(current_point):
    """
    Description: Function to create a grid of points for EarthGRAM to generate data

    Inputs:
    - current_point: [x, y, z] points in a numpy array
    
    Outputs:
    - grid: a list of points in the format [[x,y,z],[x,y,z],...] which represents the grid
    """

    grid = []

    # Simple straight line of points going up in increments of 10 meters up to 50 meters
    for i in range(6):
        grid.append([current_point[0], current_point[1] + i * 10, current_point[2]])    

    return grid


def call_earthgram_func(current_point, current_vel, current_time):
    """
    Description: Function to organize data and call function to fetch EarthGRAM data

    Inputs:
    - current_point: [x, y, z] points in a numpy array
    - current_vel: [vx, vy, vz] points in a numpy array
    - current_time: current time in datetime format
    
    Outputs:
    - wind_vel: wind velocity [N-S, E-W, Radial] in a list
    - atm_density: atmospheric density as a float
    """

    _geocentric_astropy_obj = earth.from_geocentric(current_point)
    lat, long, alt = _geocentric_astropy_obj.geodetic
    pos_mag = (np.linalg.norm(current_point) - EARTH_RADIUS)
    unit_radial = [i / pos_mag for i in current_point]
    vert_vel = np.dot(current_vel, unit_radial)

    _balloon_state = BalloonState(current_time, lat, long, alt, vert_vel)

    grid = earthgram_points(current_point)
    grid_points = []
    for point in grid:
        _geocentric_astropy_obj = earth.from_geocentric(point)
        grid_points.append(_geocentric_astropy_obj.geodetic)
    _gram_grid = GramGrid(grid_points[:][0], grid_points[:][1], grid_points[:][2])

    _grid_out = get_earthgram_data(_balloon_state, _gram_grid)
    wind_vel = cardinal_to_cart(_grid_out)
    atm_density = _grid_out.rho
    
    return wind_vel, atm_density


def balloon_force_models(vel_vert, wind_vel, atm_density):
    """
    Function to define and calculate
    forces acting on balloon system
    """

    # Force calculations
    gravity = mass * 9.18
    buoyancy = atm_density * balloon_volume
    drag_x = 0.5 * atm_density * wind_vel[1]^2 * coeff_drag * balloon_cross_area
    drag_y = 0.5 * atm_density * wind_vel[0]^2 * coeff_drag * balloon_cross_area
    drag_z = 0.5 * atm_density * (wind_vel[2] - vel_vert)^2 * coeff_drag * balloon_cross_area

    # accels is the acceleration in [x, y, z]
    accels = [0, 0, 0]
    # Acceleration in x-direction 
    accels[0] = drag_x / mass
    # Acceleration in y-direction 
    accels[1] = drag_y / mass
    # Acceleration in z-direction 
    accels[2] = (buoyancy - gravity - drag_z) / mass 

    return accels


def balloon_EOM(t, vars):
    """
    Function to be numerically integrated.
    Contains state variable assignments 
    and calls to force model functions.
    """
    
    current_point = np.array(vars[0:3])
    current_vel = np.array(vars[2:6])
    current_time = launch_time + t

    #TODO: Build function to check if balloon is outside of earthgram data grid
    out_of_bounds = 1

    if out_of_bounds == 1:
        earth_gram_data = call_earthgram_func(current_point, current_vel, current_time)
    
    #TODO: Build method to determine which point to use in earthgram data grid
    wind_vel = [earth_gram_data.vx, earth_gram_data.vy, earth_gram_data.vz]
    atm_density = earth_gram_data.rho
    
    accels = balloon_force_models(vars[5], wind_vel, atm_density)

    # First three values: vx, vy, vz [m/s]
    # Second three values: ax, ay, az [m/s^2]
    vars_dot = np.array([0, 0, 0, 0, 0, 0]).astype(float)
    # Assign derivatives of velocity equal to acceleration
    vars_dot[0] = vars[3]
    vars_dot[1] = vars[4]
    vars_dot[2] = vars[5]
    # Assign accelerations as a function of force models
    vars_dot[3] = accels[0]
    vars_dot[4] = accels[1]
    vars_dot[5] = accels[2]
    
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
    balloonEphemerisWriter(inputs.launch_date, dat.pos_vel, dat.time, 'balloon','Fixed')

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


@dataclass
class BalloonState:
    """ 
    Establishes a standardized data structure class to contain the
    instantaneous balloon state at a given time
    """
    date_time: t.datetime
    lat: float
    long: float
    alt: float
    vert_speed: float    


@dataclass
class GramGrid:
    """ 
    Establishes a standardized data structure class to contain the
    grid of points that will be passed to EarthGram to fetch next set of data
    """
    lat: ty.List[float]
    long: ty.List[float]
    alt: ty.List[float]