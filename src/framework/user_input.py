import datetime as t


def user_input():
    gui = 'initialize'
    gui = input('Would you like to use the GUI (Yes/No): ')
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
    inputs = None
    return inputs


def user_input_terminal():
    # Fake Date to test inputs
    inputs = InputStructure()
    inputs.launch_date = t.datetime(2025, 6, 21, 7)
    inputs.mode = 1
    inputs.weather_model = 'historical'
    return inputs


class InputStructure:
    def __init__(self):
        self.launch_alt = 20000
