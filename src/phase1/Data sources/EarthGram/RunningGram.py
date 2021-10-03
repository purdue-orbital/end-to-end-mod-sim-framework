#Runs GRAM2016.exe with inputs for MyTest
#Make sure not to click off of the pop-up

import os, os.path
import time
from pynput.keyboard import Key, Controller as KeyboardController

#Runs the GRAM2016.exe
os.startfile(r"C:\Users\rlust\Desktop\EarthGram\MyTest\GRAM2016.exe")

keyboard = KeyboardController()

#These need to be inputted from a file
path = "C:\\Users\\rlust\\Desktop\\EarthGram\\MyTest\\"
filename = "NameRef_2016a.txt"

#Waits for the program to open
time.sleep(1)

#Types the folder path and filename in the exe
for char in path:
    keyboard.type(char)  

keyboard.press(Key.enter)
keyboard.release(Key.enter)


for char in filename:
    keyboard.type(char)

keyboard.press(Key.enter)
keyboard.release(Key.enter)

#Waits and then closes the program, 
time.sleep(4)

keyboard.press(Key.enter)
keyboard.release(Key.enter)