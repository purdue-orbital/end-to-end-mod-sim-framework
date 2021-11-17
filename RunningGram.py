import os, os.path
from pynput.keyboard import Key, Controller as KeyboardController
import win32com.client
import time
import subprocess
import threading
#Runs GRAM2016.exe with inputs for MyTest
#Make sure not to click off of the pop-up
#Opens the txt file to get inputs
#The file name should be in the folder you are working in

#Make sure the order is: 

#exe path
#input path
#Ref file name


#moniter_memory is called as a thread while RunningGram runs to watch for the total memory use of EarthGram
#When moniter memory finishes, RunningGram closes EarthGram
#There are a few different stages of no memory use while running EarthGram, so this function looks for those stages
#It terminates at the final one
def moniter_memory():
    substring = 'No tasks are running'
    while True:
        memory = str(subprocess.check_output('tasklist /fi "imagename eq GRAM2016.exe"', shell=True))
        if substring not in memory:
            memoryNumber = memory[235] + memory[237] + memory[238] + memory[239]
            #print(memoryNumber)
            while True:
                memoryWait = str(subprocess.check_output('tasklist /fi "imagename eq GRAM2016.exe"', shell=True))
                memoryNumberWait = memoryWait[234] + memoryWait[235] + memoryWait[237] + memoryWait[238] + memoryWait[239]
                #print(memoryNumberWait)
                if memoryNumberWait != memoryNumber:
                    while True:
                        memoryNew = str(subprocess.check_output('tasklist /fi "imagename eq GRAM2016.exe"', shell=True))
                        memoryNumberNew = memoryNew[234] + memoryNew[235] + memoryNew[237] + memoryNew[238] + memoryNew[239] 
                        #print(memoryNumberNew)  
                        if memoryNumberNew != memoryNumberWait:
                            memoryFinal = str(subprocess.check_output('tasklist /fi "imagename eq GRAM2016.exe"', shell=True))
                            memoryNumberFinal = memoryFinal[234] + memoryFinal[235] + memoryFinal[237] + memoryFinal[238] + memoryFinal[239]
                            previous = None
                            while memoryNumberFinal != previous:
                                previous = memoryNumberFinal
                                memoryFinal = str(subprocess.check_output('tasklist /fi "imagename eq GRAM2016.exe"', shell=True))
                                memoryNumberFinal = memoryFinal[234] + memoryFinal[235] + memoryFinal[237] + memoryFinal[238] + memoryFinal[239]
                                #print(memoryNumberFinal)
                                return
                           

#Runs Gram automatically, uses memory usage to close it                                            
def RunningGram():
    
    t1 = threading.Thread(target=moniter_memory)
    t1.start()

    f = open("Absolute File Path.txt", "r")

    lines = f.readlines()
    f.close()
    keyboard = KeyboardController()

    #removes the \n from each line
    lines[0] = lines[0].strip()
    lines[1] = lines[1].strip()
    lines[1] = lines[1].strip()

    #Runs the GRAM2016.exe
    os.startfile(lines[0])

    #Waits for gram to appear in cmd
    while True:
        strComputer = "."
        objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
        objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
        colItems = objSWbemServices.ExecQuery("Select * from Win32_Process")
        for objItem in colItems:
            if objItem.Name == "GRAM2016.exe":

                #Types the folder path and filename in the exe
                for char in lines[1]:
                    keyboard.type(char)

                keyboard.press(Key.enter)
                keyboard.release(Key.enter)


                for char in lines[2]:
                    keyboard.type(char)

                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                t1.join()
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)  
                return              


#function only to be used if the other one breaks, or if running TmeTest
def RunningGramWait():
    
    f = open("Absolute File Path.txt", "r")

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


    #Waits and then closes the program
    time.sleep(.5)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    #while True:
    #    if os.path.isfile("output.txt"): 
    #       keyboard.press(Key.enter)
    #       keyboard.release(Key.enter)
    #       break        
