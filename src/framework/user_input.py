import numpy as np
import datetime as t
from dataclasses import dataclass
import typing as ty
import math


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
    
    # Lat/Long/Alt of Cape Canaveral
    cape_lla_deg = [28.3922, -80.6077, 0]

    # Cartesian Position for Cape Canaveral (from STK)
    cape_cart_km = [916.357, -5539.88, 3014.8]
    cape_cart_m = [i * 1000 for i in cape_cart_km]

    # Fake Data to test inputs
    inputs = InputStructure(25000.0, cape_cart_m, 'Cartesian', t.datetime(2025, 6, 21, 7), 3600, 1, 'historical')

    if inputs.launch_location_type == 'Cartesian':
        inputs.launch_location_cart = inputs.launch_location_lla

    if inputs.launch_location_type == 'Lat-Long-Alt':
        inputs.launch_location_cart = inputs.lla_to_cartesian()

    return inputs


@dataclass
class InputStructure:

    launch_alt: float
    launch_location_lla: ty.List[float]
    launch_location_type: str
    launch_date: int
    launch_duration: int
    mode: int
    weather_model: str
    launch_location_cart: ty.Optional[ty.List[float]] = None

    def lla_to_cartesian(self):     
        latitude, longitude = np.deg2rad(self.launch_location_lla[0:2])
        altitude = self.launch_location_lla[2]
        cart = []
        R = 6378137.0 + altitude  # relative to centre of the earth     
        cart.append(R * math.cos(longitude) * math.cos(latitude))
        cart.append(R * math.sin(longitude) * math.cos(latitude))
        cart.append(R * math.sin(latitude))
        return cart
