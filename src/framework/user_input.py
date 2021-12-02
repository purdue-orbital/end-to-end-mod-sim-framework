import numpy as np
import datetime as t
from dataclasses import dataclass
import typing as ty
import math
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
    
    # Select the run mode
    # Mode = 1: Single balloon run
    # Mode = 2: Multiple balloon runs spread out through the year
    mode = 2
    
    # Initial time
    init_time = '15 May 2023 12:00:00.000000'
    launch_time = datetime2STK.UTCG2datetime(init_time)
    
    # Lat/Long/Alt of Cape Canaveral
    cape_lla_deg = [28.3922, -80.6077, 0]
    # Cartesian Position for Cape Canaveral (from STK)
    cape_cart_km = [916.357, -5539.88, 3014.8]
    cape_cart_m = [i * 1000 for i in cape_cart_km]

    # Constant values [mass [kg], coefficient of drag, cross-sectional balloon area [m^2], balloon volume [m^3], time of launch, location of launch]
    # From google drive, prelim Raven specs say diameter of 61.5 ft for 205 lb system (160 lb payload, 45 lb balloon)
    radius = 9.3845 # meters
    area = np.square(radius)*np.pi
    volume = 4/3*np.pi*np.power(radius,3)
    constants = [93, 0.5, area, volume, launch_time, cape_cart_m, cape_lla_deg]

    # Fake Data to test inputs
    inputs = InputStructure(25000.0, [0, 0, 0], 'Cartesian', launch_time, 3600, mode, 'historical', constants)

    # If inputs are Cartesian then directly translate
    if inputs.launch_location_type == 'Cartesian':
        inputs.launch_location_cart = inputs.launch_location_lla

    # If inputs are Lat-Long-Alt then use the coordinate transition method
    if inputs.launch_location_type == 'Lat-Long-Alt':
        inputs.launch_location_cart = inputs.lla_to_cartesian()
    
    # Set initial velocity to assume zero in all directions
    init_vel = [0, 0, 1]

    # append position and velocity vectors to create initial state vector
    inputs.launch_init_state = inputs.launch_location_cart + init_vel

    return inputs


@dataclass
class InputStructure:

    launch_alt: float
    launch_location_lla: ty.List[float]
    launch_location_type: str
    launch_date: str
    launch_duration: int
    mode: int
    weather_model: str
    constants: ty.List[float]
    launch_location_cart: ty.Optional[ty.List[float]] = None
    launch_init_state: ty.Optional[ty.List[float]] = None

    def lla_to_cartesian(self):     
        latitude, longitude = np.deg2rad(self.launch_location_lla[0:2])
        altitude = self.launch_location_lla[2]
        cart = []
        R = 6378137.0 + altitude  # relative to centre of the earth     
        cart.append(R * math.cos(longitude) * math.cos(latitude))
        cart.append(R * math.sin(longitude) * math.cos(latitude))
        cart.append(R * math.sin(latitude))
        return cart
