def user_input():
    GUI = 'initialize'
    while GUI != 'Yes' or 'No':
        GUI = input('Would you like to use the GUI (Yes/No): ')
        if GUI != 'Yes' or 'No':
            print('Incorrect input, expected /"Yes/" or /"No/"')
    if GUI == 'Yes':
        input = user_input_GUI()
    elif GUI == 'No':
        input = user_input_terminal()
    return input

def user_input_GUI():
    pass
    # TODO: develop a GUI interface for MASTRAB (lmao terrible name)

def user_input_terminal():
    pass
