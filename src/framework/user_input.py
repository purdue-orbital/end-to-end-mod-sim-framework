import datetime as t
from dataclasses import dataclass


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
    # Fake Data to test inputs
    inputs = InputStructure(25000.0, [47, 56], t.datetime(2025, 6, 21, 7), 1, 'historical')
    return inputs


@dataclass
class InputStructure:

    launch_alt: float
    launch_location_lla: list[float]
    launch_date: t.datetime
    mode: int
    weather_model: str

    def lla_to_cartesian(self):
        
        #todo: logic to convert from lla to cartesian

        launch_location_cart = self.launch_location_lla

        return launch_location_cart
