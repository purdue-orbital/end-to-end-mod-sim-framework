# Import standard external libraries and imports
from astropy.coordinates import earth
from matplotlib.pyplot import close
import numpy as np
import pyquaternion as quat 
from dataclasses import dataclass
import datetime
import scipy.integrate as integrate
import typing as ty
from get_earthgram_data import get_earthgram_data
import sys

def setConstants(inputs):

    # Define global variables
    global mass, coeff_drag, balloon_volume_init, launch_time
    global launch_cart_m, launch_lla_deg, EARTH_RADIUS, earthgram_alt_interval_m, end_mode
    mass, coeff_drag, balloon_volume_init, launch_time, earthgram_alt_interval_m, end_mode = inputs.constants
    EARTH_RADIUS = 6373.455 * 1000

    launch_cart_m = inputs.launch_location_cart
    launch_lla_deg = inputs.launch_location_lla

    return

def enu2xyz(enu_position):
    """
    Convert east, north, up coordinates (labeled e, n, u) to ECEF coordinates.
    The reference point (phi, lambda, h) must be given. All distances are in metres
    """

    origin_ecef =  launch_cart_m  # Location of launch in ECEF meters
    [refLat, refLong] =  launch_lla_deg[0:2] # Location of launch in LLA deg
    [e, n, u] = enu_position

    x = -np.sin(refLong)*e - np.cos(refLong)*np.sin(refLat)*n + np.cos(refLong)*np.cos(refLat)*u + origin_ecef[0]
    y = np.cos(refLong)*e - np.sin(refLong)*np.sin(refLat)*n + np.cos(refLat)*np.sin(refLong)*u + origin_ecef[1]
    z = np.cos(refLat)*n + np.sin(refLat)*u + origin_ecef[2]

    return [x, y, z]


def enu2xyz_vec(enu_vec):
    """
    Convert east, north, up vector (labeled e, n, u) to ECEF vector.
    The reference point (phi, lambda, h) must be given. All values are in m/s
    """

    [refLat, refLong] =  launch_lla_deg[0:2]
    [e, n, u] = enu_vec

    x = -np.sin(refLong)*e - np.cos(refLong)*np.sin(refLat)*n + np.cos(refLong)*np.cos(refLat)*u
    y = np.cos(refLong)*e - np.sin(refLong)*np.sin(refLat)*n + np.cos(refLat)*np.sin(refLong)*u
    z = np.cos(refLat)*n + np.sin(refLat)*u

    cart = [x, y, z]

    if (np.linalg.norm(enu_vec) - np.linalg.norm(cart)) > 0.1:
        print("Conversion not working")
        sys.exit()

    return cart


def call_earthgram_func(current_point_local, vert_vel, current_time):
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

    _geocentric_astropy_obj = earth.EarthLocation.from_geocentric(
        current_point[0],current_point[1],current_point[2],unit='meter')
    long, lat, alt = _geocentric_astropy_obj.geodetic

    _balloon_state = BalloonState(current_time, lat, long, alt.value, vert_vel)

    _gram_grid = GramGrid([], [], [])
    for i in range(int(earthgram_alt_interval_m/10)):
        _gram_grid.long.append(_balloon_state.long)
        _gram_grid.lat.append(_balloon_state.lat)
        if _balloon_state.alt < 0:
            _gram_grid.alt.append((0 + i*10)/1000)
        else:
            _gram_grid.alt.append((_balloon_state.alt + i*10)/1000)

    _grid_out = get_earthgram_data(_balloon_state, _gram_grid)

    return _grid_out


def balloon_force_models(balloon_vel, wind_vel, atm_density, press, temp):
    """
    Function to define and calculate
    forces acting on balloon system
    """

    # Calculate wind velocities relative to the balloon
    rel_vel_e = wind_vel[0] - balloon_vel[0]
    rel_vel_n = wind_vel[1] - balloon_vel[1]
    rel_vel_u = wind_vel[2] - balloon_vel[2]
    
    # Calculate directionality of wind velocities to overcome square of velocity term
    rel_vel_e_dir = np.sign(rel_vel_e)
    rel_vel_n_dir = np.sign(rel_vel_n)
    rel_vel_u_dir = np.sign(rel_vel_u)

    # Balloon Expansion
    global balloon_volume
    balloon_volume = k * temp / press
    balloon_cross_area = np.cbrt(0.75 / np.pi * balloon_volume)

    # Force calculations
    gravity = mass * 9.81
    buoyancy = float(atm_density) * balloon_volume
    drag_e = 0.5 * atm_density * np.square(rel_vel_e) * rel_vel_e_dir * coeff_drag * balloon_cross_area
    drag_n = 0.5 * atm_density * np.square(rel_vel_n) * rel_vel_n_dir * coeff_drag * balloon_cross_area
    drag_u = 0.5 * atm_density * np.square(rel_vel_u) * rel_vel_u_dir * coeff_drag * balloon_cross_area

    # accels is the acceleration in [x, y, z]
    accels = [0, 0, 0]
    # Acceleration in x-direction
    accels[0] = drag_e / mass
    # Acceleration in y-direction
    accels[1] = drag_n / mass
    # Acceleration in z-direction
    accels[2] = (buoyancy - gravity + drag_u) / mass

    """
    print("atm_dens = "+str(atm_density))
    print("vel balloon "+str(balloon_vel[2]))
    print("balloon_volume "+str(balloon_volume))
    print("vel e = "+str(rel_vel_e))
    print("vel n = "+str(rel_vel_n))
    print("vel u = "+str(rel_vel_u))
    print("drag e = "+str(drag_e))
    print("drag n = "+str(drag_n))
    print("drag u = "+str(drag_u))
    print("bouy ="+str(buoyancy))
    print("grav = "+str(gravity))
    print("accel in e n u ="+str(accels))
    # print("accel in x y z ="+str(accels))
    """

    return accels


def balloon_EOM(t, vars):
    """
    Function to be numerically integrated.
    Contains state variable assignments
    and calls to force model functions.
    """
    
    # Pull out useful earthgram data
    wind_vel = [closest_earth_gram_data.vE, closest_earth_gram_data.vN, closest_earth_gram_data.vz]
    atm_density = closest_earth_gram_data.rho
    press = closest_earth_gram_data.p
    temp = closest_earth_gram_data.temp
    
    accels = balloon_force_models(vars[3:6], wind_vel, atm_density, press, temp)

    # First three values: vx, vy, vz [m/s]
    # Second three values: ax, ay, az [m/s^2]
    vars_dot = np.array([0, 0, 0, 0, 0, 0]).astype(float)
    # Assign derivatives of aceleration equal to velocity
    vars_dot[0] = vars[3]
    vars_dot[1] = vars[4]
    vars_dot[2] = vars[5]
    # Assign accelerations as a function of force models
    vars_dot[3] = accels[0]
    vars_dot[4] = accels[1]
    vars_dot[5] = accels[2]

    """
    print("pos e = "+str(vars[0]))
    print("pos n = "+str(vars[1]))
    print("pos u = "+str(vars[2])+"\n\n")
    """

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

    setConstants(inputs)

    # Initialize an instance of the data class to store data
    balloon_data = EphemerisDataStruct_Balloon()
    # Set the data objects launch date, launch duration, and initial state from inputs
    balloon_data.init_time = inputs.launch_date
    if end_mode == 2:
        balloon_data.duration = inputs.launch_duration
    elif end_mode == 1:
        # Set super large so that integration ends on altitude
        balloon_data.duration = 86400
    else:
        print("\n!!! end_mode value is invalid !!!\n\n")
        sys.exit()
    balloon_data.pos_vel = [0, 0, 0] + inputs.launch_init_state[3:6]
    balloon_data.output_ephem = np.array(inputs.launch_init_state)
    balloon_data.time = 0

    # Give the balloon data object a short handle (name) for easy future reference
    dat = balloon_data

    current_point = np.array(dat.pos_vel[0:3])
    vert_vel = dat.pos_vel[5]
    current_time = inputs.launch_date
    earth_gram_data_list = call_earthgram_func(current_point, vert_vel, current_time)

    # Once closest data point is found, set a temp variable containing the object
    global closest_earth_gram_data, k
    closest_earth_gram_data = earth_gram_data_list[0]
    last_alt = 0
    alt_t = 0
    out_of_bounds = 0
    # Source: https://northstar-www.dartmouth.edu/~klynch/pmwiki-gc/uploads/
    # BalloonCalulations.pdf#:~:text=As%20the%20balloon%20raises%2C%20the%20pressure%20outside%20the
    # ,of%20the%20reason%20theStandard%20Atmospherewas%20introducedin%20section%201
    # .?msclkid=2816be06c70911ecadc179d030c47d5b
    init_temp = closest_earth_gram_data.temp
    init_p = closest_earth_gram_data.p
    k = init_p * balloon_volume_init / init_temp

    # Create an "integration object" of the SciPy libraries RK45 numerical integrator class
    # Provide the integrator the function to be run, initial pos_vel, and integration time, 
    # as well as the first earthgram data object
    integration_obj = integrate.RK45(balloon_EOM, 0, dat.pos_vel, dat.duration)

    # While the integration is still running, continue to step through integration
    while integration_obj.status == 'running':
        # Integrator chooses a step time dynamically based on observed patterns
        integration_obj.step()

        if abs(integration_obj.y[2] - alt_t) < 0:
            print("Balloon is descending")
            sys.exit()
        else:
            alt_t = integration_obj.y[2]
        
        # Determine if our current location is still within or close enough to data grid, if not, get new data
        if abs(integration_obj.y[2] - last_alt) > earthgram_alt_interval_m:
            #TODO: Build function to check if balloon is outside of earthgram data grid
            out_of_bounds = 1
            last_alt = integration_obj.y[2]

        # If outside of grid bounds, call earthgram function and get updated data grid
        if out_of_bounds == 1:
            current_point = np.array(integration_obj.y[0:3])
            vert_vel = dat.pos_vel[5]
            current_time = inputs.launch_date + datetime.timedelta(seconds=integration_obj.t)
            earth_gram_data_list = call_earthgram_func(current_point, vert_vel, current_time)
            closest_earth_gram_data = earth_gram_data_list[0]
            out_of_bounds = 0

        # Find closest earthgram data point
        #TODO: Build a better method to determine which point to use in earthgram data grid
        alt_fraction = (integration_obj.y[2] - last_alt)/earthgram_alt_interval_m
        gram_interval = int(np.floor(alt_fraction * len(earth_gram_data_list)))
        closest_earth_gram_data = earth_gram_data_list[gram_interval]

        # At each time step, store the current state and time and append to ephemeris data struct
        dat.pos_vel = integration_obj.y
        pos_xyz = enu2xyz(integration_obj.y[0:3])
        vel_xyz = enu2xyz_vec(integration_obj.y[3:6])
        ephem_xyz = np.append(pos_xyz, vel_xyz)

        dat.output_ephem = np.append(dat.output_ephem, ephem_xyz)
        dat.time = np.append(dat.time, integration_obj.t)

        if integration_obj.y[2] >= inputs.launch_alt:
            break
    
    if end_mode == 1:
        print('\nFinal Integration Status: Complete\n')
    else:
        print('\nFinal Integration Status: {}'.format(integration_obj.status))

    # Once the integration is done, reshape the data struct to an n x 6 where n is the number of time steps
    dat.output_ephem = dat.output_ephem.reshape((int(len(dat.output_ephem)/6), 6))
    print("\nRun succeeded!")
    print("\nAfter {} mins balloon is:".format(dat.time[-1]/60))
    print("Final Altitude = {} km".format(dat.pos_vel[2]/1000))
    print("Balloon Volume Ratio = {}".format(balloon_volume/balloon_volume_init))
    print("Drift in East {} km".format(dat.pos_vel[0]/1000))
    print("Drift in North {} km".format(dat.pos_vel[1]/1000))

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
    output_ephem: ty.Optional[np.array] = None
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