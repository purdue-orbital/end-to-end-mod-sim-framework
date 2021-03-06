import sys
import time
import os, os.path
import signal
import subprocess
from pynput.keyboard import Key, Controller as KeyboardController
import keyboard as key

#Runs GRAM2016.exe with inputs for MyTest
#Make sure not to click off of the pop-up
#Opens the txt file "Absolute File Path.txt" to get inputs
#The file should be in the folder you are working in

#Make sure the order is:

#exe path
#input path
#Ref file name

def RunningGram():

    """
    f = open("earthgram/FilePaths.txt", "r")
    lines = f.readlines()
    f.close()

    #removes the \n from each line
    lines[0] = lines[0].strip()
    lines[1] = lines[1].strip()
    lines[2] = lines[2].strip()

    engine = subprocess.Popen("earthgram/GRAM2016.exe",
     universal_newlines=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
    engine.communicate(input=lines[1] + '\n' + lines[2] + '\n')
    time.sleep(2)

    return
    """

    f = open("earthgram/FilePaths.txt", "r")

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
    time.sleep(3)
    key.send("alt+F4, space")
    #keyboard.press(Key.enter)
    #keyboard.release(Key.enter)

    """
    while True:
        if os.path.isfile("earthgram/output.txt"):
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            break
    """
