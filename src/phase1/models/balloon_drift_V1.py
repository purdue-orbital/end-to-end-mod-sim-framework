# Import standard external libraries and imports
from astropy.coordinates import earth
import numpy as np
import pyquaternion as quat 
from dataclasses import dataclass
import datetime
import scipy.integrate as integrate
import typing as ty
from get_earthgram_data import get_earthgram_data
import sys


def enu2xyz(enu_position):
  """
  Convert east, north, up coordinates (labeled e, n, u) to ECEF coordinates.
  The reference point (phi, lambda, h) must be given. All distances are in metres
  """
 
  origin_ecef =  cape_cart_m  # Location of Cape Canaveral in ECEF meters
  [refLat, refLong] =  cape_lla_deg[0:2]
  [e, n, u] = enu_position
 
  X = -np.sin(refLong)*e - np.cos(refLong)*np.sin(refLat)*n + np.cos(refLong)*np.cos(refLat)*u + origin_ecef[0]
  Y = np.cos(refLong)*e - np.sin(refLong)*np.sin(refLat)*n + np.cos(refLat)*np.sin(refLong)*u + origin_ecef[1]
  Z = np.cos(refLat)*n + np.sin(refLat)*u + origin_ecef[2]
  
  return [X, Y, Z]


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
        #TODO: Create a more complex gridding shape

    return grid


def call_earthgram_func(current_point_local, current_vel, current_time):
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
    current_point = enu2xyz(current_point_local)

    _geocentric_astropy_obj = earth.EarthLocation.from_geocentric(current_point[0],current_point[1],current_point[2],unit='meter')
    lat, long, alt = _geocentric_astropy_obj.geodetic
    pos_mag = (np.linalg.norm(current_point) - EARTH_RADIUS)
    unit_radial = [i / pos_mag for i in current_point]
    vert_vel = np.dot(current_vel, unit_radial)

    _balloon_state = BalloonState(current_time, lat, long, alt.value, vert_vel)

    #TODO: Fix grid creation in LLA/Cart context
    # grid = earthgram_points(current_point)
    
    _gram_grid = GramGrid([], [], [])
    for i in range(6):
        _geocentric_astropy_obj = earth.EarthLocation.from_geocentric(current_point[0],current_point[1],current_point[2],unit='meter')
        temp = _geocentric_astropy_obj.geodetic
        _gram_grid.long.append(temp.lon.value)
        _gram_grid.lat.append(temp.lat.value)
        if temp.height.value < 0:
            _gram_grid.alt.append((0 + i*100)/1000)
        else:
            _gram_grid.alt.append((temp.height.value + i*100)/1000)

    _grid_out = get_earthgram_data(_balloon_state, _gram_grid)
    
    return _grid_out


def balloon_force_models(balloon_vel, wind_vel, atm_density):
    """
    Function to define and calculate
    forces acting on balloon system
    """
    # Calculate wind velocities relative to the balloon
    rel_vel_x = balloon_vel[0] - wind_vel[0]
    rel_vel_y = balloon_vel[1] - wind_vel[1]
    rel_vel_z = balloon_vel[2] - wind_vel[2]
    
    # Calculate directionality of wind velocities to overcome square of velocity term
    rel_vel_x_dir = np.sign(rel_vel_x)
    rel_vel_y_dir = np.sign(rel_vel_y)
    rel_vel_z_dir = np.sign(rel_vel_z)

    # Force calculations
    gravity = mass * 9.81
    buoyancy = float(atm_density) * balloon_volume
    drag_x = 0.5 * atm_density * np.square(rel_vel_x) * rel_vel_x_dir * coeff_drag * balloon_cross_area
    drag_y = 0.5 * atm_density * np.square(rel_vel_y) * rel_vel_y_dir * coeff_drag * balloon_cross_area
    drag_z = 0.5 * atm_density * np.square(rel_vel_z) * rel_vel_z_dir * coeff_drag * balloon_cross_area

    # accels is the acceleration in [x, y, z]
    accels = [0, 0, 0]
    # Acceleration in x-direction 
    accels[0] = -drag_x / mass
    # Acceleration in y-direction 
    accels[1] = -drag_y / mass
    # Acceleration in z-direction 
    accels[2] = (buoyancy - gravity - drag_z) / mass 

    return accels


def balloon_EOM(t, vars):
    """
    Function to be numerically integrated.
    Contains state variable assignments 
    and calls to force model functions.
    """
    
    wind_vel = [closest_earth_gram_data.vE, closest_earth_gram_data.vN, closest_earth_gram_data.vz]
    atm_density = closest_earth_gram_data.rho
    
    accels = balloon_force_models(vars[3:6], wind_vel, atm_density)

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

    # Define global variables
    global mass, coeff_drag, balloon_cross_area, balloon_volume, launch_time, cape_cart_m, cape_lla_deg, EARTH_RADIUS
    mass, coeff_drag, balloon_cross_area, balloon_volume, launch_time, cape_cart_m, cape_lla_deg = inputs.constants
    EARTH_RADIUS = 6373.455 * 1000

    # Initialize an instance of the data class to store data
    balloon_data = EphemerisDataStruct_Balloon()
    # Set the data objects launch date, launch duration, and initial state from inputs
    balloon_data.init_time = inputs.launch_date
    balloon_data.duration = inputs.launch_duration
    balloon_data.pos_vel = inputs.launch_init_state
    balloon_data.time = 0

    # Give the balloon data object a short handle (name) for easy future reference
    dat = balloon_data
    
    current_point = np.array(dat.pos_vel[0:3])
    current_vel = np.array(dat.pos_vel[3:6])
    current_time = inputs.launch_date
    earth_gram_data_list = call_earthgram_func(current_point, current_vel, current_time)
    
    # Once closest data point is found, set a temp variable containing the object
    global closest_earth_gram_data
    closest_earth_gram_data = earth_gram_data_list[0]
    last_alt = 0
    out_of_bounds = 0

    # Create an "integration object" of the SciPy libraries RK45 numerical integrator class
    # Provide the integrator the function to be run, initial pos_vel, and integration time, as well as the first earthgram data object
    integration_obj = integrate.RK45(balloon_EOM, 0, dat.pos_vel, dat.duration)

    # While the integration is still running, continue to step through integration
    while integration_obj.status == 'running':
        # Integrator chooses a step time dynamically based on observed patterns
        integration_obj.step()
        
        # Determine if our current location is still within or close enough to data grid, if not, get new data
        if abs(integration_obj.y[2] - last_alt) > 100:
            #TODO: Build function to check if balloon is outside of earthgram data grid
            out_of_bounds = 1
            last_alt = integration_obj.y[2]

        # If outside of grid bounds, call earthgram function and get updated data grid
        if out_of_bounds == 1:
            current_point = np.array(integration_obj.y[0:3])
            current_vel = np.array(integration_obj.y[3:6])
            current_time = inputs.launch_date + datetime.timedelta(seconds=integration_obj.t)
            earth_gram_data_list = call_earthgram_func(current_point, current_vel, current_time)
            closest_earth_gram_data = earth_gram_data_list[0]
            out_of_bounds = 0
        
        # Iterate through list of grid objects where each object contains data at a point
        for gram_data_obj in earth_gram_data_list:
            pass            
            #TODO: Build method to determine which point to use in earthgram data grid
        
        # At each time step, store the current state and time and append to ephemeris data struct
        dat.pos_vel = np.append(dat.pos_vel, integration_obj.y)
        dat.time = np.append(dat.time, integration_obj.t)
        
    print('\nFinal Integration Status: {}'.format(integration_obj.status))
    
    # Once the integration is done, reshape the data struct to an n x 6 where n is the number of time steps
    dat.pos_vel = dat.pos_vel.reshape((int(len(dat.pos_vel)/6), 6))

    # Return data object structure for reference in main code
    return dat


@dataclass
class EphemerisDataStruct_Balloon:
    """ 
    Establishes a standardized data structure class to contain the
    full time range ephemeris for a single balloon model run
    """
    init_time: ty.Optional[datetime.datetime] = None
    duration: ty.Optional[datetime.datetime] = None
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
    date_time: datetime.datetime
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