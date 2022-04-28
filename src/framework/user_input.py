import sys
import numpy as np
import datetime as t
from dataclasses import dataclass
import typing as ty
import math
import pyproj
from importlib.machinery import SourceFileLoader
datetime2STK = SourceFileLoader('datetime2STK', 'helper_functions/datetime2STK.py').load_module()


def user_input():
    gui = 'initialize'
    gui = input('\n\nWould you like to use the GUI (Yes/No): ')
    while gui not in ['Yes', 'No']:
        print('\nIncorrect input, expected "Yes" or "No"\n')
        gui = input('Would you like to use the GUI (Yes/No): ')
    if gui == 'Yes':
        input_data = user_input_gui()
    elif gui == 'No':
        input_data = user_input_terminal()
    else:
        input_data = None
    return input_data


def user_input_gui():
    pass
    # TODO: develop a GUI interface for MASTRAB (lmao terrible name)
    inputs = 1
    return inputs


def user_input_terminal():
    """
    This function contains all important user inputs to be configured prior to running
    """

    # Select the run mode
    # Mode = 1: Single balloon run
    # Mode = 2: Multiple balloon runs spread out through the year
    mode = 1
    earthgram_alt_interval_m = 1000

    # Initial time
    init_time = '1 Jan 2022 12:00:00.000000'
    launch_time = datetime2STK.UTCG2datetime(init_time)
    launch_altitude = 2000 # meters altitude
    launch_duration = 3600 # seconds
    # 1 = end at altitude, 2 = end at time
    end_mode = 1

    # Lat/Long/Alt of Launch Location
    launch_lla_deg = [28, -80, 0]
    # ECEF xyz of Launch Location
    launch_cart_m = [0, 0, 0]

    # Either 'Cartesian', 'Lat-Long-Alt', or 'Cape Canaveral'
    launch_location_type = 'Lat-Long-Alt'
    # Set initial velocity to assume 1 m/s in z direction (upwards)
    init_vel = [0, 0, 1]

    # Constant values [mass [kg], coefficient of drag, cross-sectional balloon area [m^2],
    #  balloon volume [m^3], time of launch, location of launch]
    # From google drive, prelim Raven specs say diameter of 61.5 ft for 205 lb system
    # (160 lb payload, 45 lb balloon)
    radius = 8 # meters
    volume = 4/3*np.pi*np.power(radius,3)
    payload_mass = 260

    # Fake Data to test inputs
    inputs = InputStructure(launch_altitude, launch_location_type,
     launch_time, launch_duration, mode, 'historical')

    # If inputs are Lat-Long-Alt then use the coordinate transition method
    if inputs.launch_location_type == 'Lat-Long-Alt':
        inputs.launch_location_lla = launch_lla_deg
        inputs.launch_location_cart = inputs.lla_to_cartesian()
    elif inputs.launch_location_type == 'Cartesian':
        inputs.launch_location_cart = launch_cart_m
        inputs.launch_location_lla = inputs.cart_to_lla()
    elif inputs.launch_location_type == 'Cape Canaveral':
        # Cartesian Position for Cape Canaveral (from STK)
        cape_cart_km = [916.357, -5539.88, 3014.8]
        cape_cart_m = [i * 1000 for i in cape_cart_km]
        inputs.launch_location_cart = cape_cart_m
        inputs.launch_location_lla = [28.410351, -80.618813, 0]
    
    inputs.constants = [payload_mass, 0.5, volume, launch_time,
     earthgram_alt_interval_m, end_mode]

    # append position and velocity vectors to create initial state vector
    inputs.launch_init_state = inputs.launch_location_cart + init_vel

    return inputs


@dataclass
class InputStructure:

    launch_alt: float
    launch_location_type: str
    launch_date: str
    launch_duration: int
    mode: int
    weather_model: str
    constants: ty.Optional[ty.List[float]] = None
    launch_location_lla: ty.Optional[ty.List[float]] = None
    launch_location_cart: ty.Optional[ty.List[float]] = None
    launch_init_state: ty.Optional[ty.List[float]] = None

    def lla_to_cartesian(self):
        """
        Conversion function for lat-long-alt state to x-y-z ecef state
        """
        latitude, longitude = np.deg2rad(self.launch_location_lla[0:2])
        altitude = self.launch_location_lla[2]
        cart = []
        R = 6373.455 * 1000 + altitude  # relative to centre of the earth
        cart.append(R * math.cos(longitude) * math.cos(latitude))
        cart.append(R * math.sin(longitude) * math.cos(latitude))
        cart.append(R * math.sin(latitude))
        return cart

    def cart_to_lla(self):
        """
        Conversion function for x-y-z ecef state to lat-long-alt state
        """
        x, y, z = self.launch_location_cart
        transformer = pyproj.Transformer.from_crs(
        {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
        {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'})

        lon1, lat1, alt1 = transformer.transform(x,y,z,radians=False)

        return [lon1, lat1, alt1]
