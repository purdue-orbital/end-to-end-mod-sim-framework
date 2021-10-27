import numpy as np
import datetime as t
from dataclasses import dataclass
import typing as ty

#import libs for user_input_gui() func
from tkinter import *
from tkinter import messagebox
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
    


    #tkinter lib info: https://docs.python.org/3/library/tkinter.html

    ###################GUI Window SETUP######################################
    #create main window
    master = Tk(screenName=None, baseName=None,className= 'MASTRAB GUI',useTk=1)

    #GUI window title
    master.title('MASTRAB GUI')

    #add a grid for entire GUI, size it
    mainframe = Frame(master)
    mainframe.grid(column=0,row=0, sticky=(N,W,E,S))
    mainframe.columnconfigure(0, weight = 1)
    mainframe.rowconfigure(0, weight = 1)
    mainframe.pack(pady = 10, padx = 50)

    #initialize list storing all inputs
    inputs = [] #empty list of inputs

    #LIST INPUT INDEXING FYI
    #index 1 - Phase 1 DS, index 2 - Phase 1 Model, index 3 - Phase 2 DS, so on.

    ################################## DATA SOURCES###########################################
    #DS general label
    Label(mainframe, text="Data Sources").grid(row = 2, column = 1)

    #PHASE 1
    #create variable for phase 1 DS
    P1_DS = StringVar(master)

    #dictionary w/ options for data sources, link/place dropdown
    P1_selDS = {'Earthgram2016','NOAA Historial'}
    popupMenu = OptionMenu(mainframe, P1_DS, *P1_selDS)
    popupMenu.grid(row = 3, column =0)

    #func for on change dropdown value, insert selected value to list
    def P1DS_assignval(*args):
        inputs.insert(1,P1_DS.get())
        
    #link function to change of dropdown
    P1_DS.trace('w', P1DS_assignval)

    #PHASE 2
    P2_DS = StringVar(master)

    #dictionary w/ options for data sources, link/place dropdown
    P2_selDS = {'P2 Option 1'}
    popupMenu = OptionMenu(mainframe, P2_DS, *P2_selDS)
    popupMenu.grid(row = 3, column =1)

    #func for on change dropdown value, insert selected value to list
    def P2DS_assignval(*args):
        inputs.insert(3,P2_DS.get())
        
    #link function to change dropdown
    P2_DS.trace('w', P2DS_assignval)

    #PHASE 3
    P3_DS = StringVar(master)

    #dictionary w/ options for data sources, link/place dropdown
    P3_selDS = {'P3 Option 1'}
    popupMenu = OptionMenu(mainframe, P3_DS, *P3_selDS)
    popupMenu.grid(row = 3, column = 2)

    #func for on change dropdown value, insert selected value to list
    def P3DS_assignval(*args):
        inputs.insert(5,P3_DS.get())
        
    #link function to change dropdown
    P3_DS.trace('w', P3DS_assignval)

    ##############################MODELS#######################################
    #Models general label
    Label(mainframe, text="Models").grid(row = 6, column = 1)

    #PHASE 1
    P1_Mod = StringVar(master)

    #dictionary w/ options for models, link/place dropdown
    P1_selMod = {'6Dof Drift Model','Ephemeris Only Drift Model'}
    popupMenu = OptionMenu(mainframe, P1_Mod, *P1_selMod)
    popupMenu.grid(row = 5, column =0)

    #func for on change dropdown value, insert selected value to list
    def P1Mod_assignval(*args):
        inputs.insert(2,P1_Mod.get())

    #link function to change dropdown
    P1_Mod.trace('w', P1Mod_assignval)

    #PHASE 2
    P2_Mod = StringVar(master)

    #dictionary w/ options for models, link/place dropdown
    P2_selMod = {'P2 option 1','P2 option 2'}
    popupMenu = OptionMenu(mainframe, P2_Mod, *P2_selMod)
    popupMenu.grid(row = 5, column =1)

    #func for on change dropdown value, insert selected value to list
    def P2Mod_assignval(*args):
        inputs.insert(4,P2_Mod.get()) 

    #link function to change dropdown
    P2_Mod.trace('w', P2Mod_assignval)

    #PHASE 3
    P3_Mod = StringVar(master)

    #dictionary w/ options for models, link/place dropdown
    P3_selMod = {'P3 Option 1'}
    popupMenu = OptionMenu(mainframe, P3_Mod, *P3_selMod)
    popupMenu.grid(row = 5, column =2)

    #func for on change dropdown value, insert selected value to list
    def P3Mod_assignval(*args):
        inputs.insert(6,P3_Mod.get()) #change to 4 index later

    #link function to change dropdown
    P3_Mod.trace('w', P3Mod_assignval)

    ################################RUN####################################
    #create variable
    Run = StringVar(master)

    #dictionary w/ options for run options, link/place dropdown
    selRun = {'Single Run','Linear Trade Study','Carpet Study'}
    popupMenu = OptionMenu(mainframe, Run, *selRun)
    Label(mainframe, text="Select Run Type").grid(row = 3, column = 3)
    popupMenu.grid(row = 4, column = 3)

    #func for on change dropdown value, insert selected value to list
    def Run_assignval(*args):
        inputs.insert(4,Run.get()) 

    Run.trace('w', Run_assignval)


    #########################################################################
    #GUI ELEMENTS (EVERYTHING BUT INPUTS and GUI SETUP)
    #header for each phase
    Label(mainframe, text="Phase 1").grid(row = 4, column = 0)
    Label(mainframe, text="Phase 2").grid(row = 4, column = 1)
    Label(mainframe, text="Phase 3").grid(row = 4, column = 2)

    #file menu
    menu = Menu(master)
    master.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label='File', menu=filemenu)
    filemenu.add_separator()
    filemenu.add_command(label='Exit', command=master.destroy)
    helpmenu = Menu(menu)

    menu.add_cascade(label='Help', menu=helpmenu)
    helpmenu.add_command(label='About')

    #submit inputs button
    run_button = Button(mainframe, text="Run MASTRAB")
    run_button.grid(row = 4, column = 4)

    #test for correct returned list when using Run MASTRAB button clicked
    def test_inp(inputs):
        if len(inputs) == 7:
            print('Sample List: ', inputs)
            master.destroy()
        else:
            messagebox.showerror("Error","Please Ensure all Dropdowns have an input selected")

    #assign func to be linked to run button (when clicked)
    run_button['command'] = lambda: test_inp(inputs)

    #infinite loop to keep app. running
    master.mainloop()
    return inputs
    

    


def user_input_terminal():
    # Fake Data to test inputs
    inputs = InputStructure(25000.0, [28.3922, -80.6077, 0], t.datetime(2025, 6, 21, 7), 3600, 1, 'historical')

    inputs.launch_location_cart = inputs.lla_to_cartesian()

    return inputs


@dataclass
class InputStructure:

    launch_alt: float
    launch_location_lla: ty.List[float]
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
