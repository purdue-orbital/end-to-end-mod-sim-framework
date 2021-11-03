import os, os.path
import time
from pynput.keyboard import Key, Controller as KeyboardController

#Runs GRAM2016.exe with inputs for MyTest
#Make sure not to click off of the pop-up
#Opens the txt file "Absolute File Path.txt" to get inputs
#The file should be in the folder you are working in

#Make sure the order is: 

#exe path
#input path
#Ref file name

def RunningGram():

    f = open("FilePaths.txt", "r")

    lines = f.readlines()
    f.close()
    keyboard = KeyboardController()

    #removes the \n from each line
    lines[0] = lines[0].strip()
    lines[1] = lines[1].strip()
    lines[1] = lines[1].strip()

    #Runs the GRAM2016.exe
    os.startfile(lines[0])

    #in case the file method doesn't work
    #path = "C:\\Users\\rlust\\OneDrive - purdue.edu\\Desktop\\EarthGram\\MyTest\\"
    #filename = "NameRef_2016a.txt"

    #Waits for the program to open
    time.sleep(.5)

    #Types the folder path and filename in the exe
    for char in lines[1]:
        keyboard.type(char)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


    for char in lines[2]:
        keyboard.type(char)

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


    #Waits and then closes the program,
    while True:
        if os.path.isfile("output.txt"): 
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            break
