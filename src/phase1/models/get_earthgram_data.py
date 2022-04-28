import datetime
import sys
import os
from dataclasses import dataclass
import typing as ty
from RunningGram import RunningGram

def get_earthgram_data(_balloon_state,_gram_grid):
    """-----------------------------------------------------------------------------------------
    CONE_OUT = getEarthGRAMData(_balloon_state,_gram_grid)
    Function to write txt file with atmosphere cone to input to EarthGRAM
    Inputs:
        _balloon_state  - structure state at current time (object with required fields below):
            .date_time  - current time (datetime)
            .vert_speed - current vertical speed (m/s)
        _gram_grid      - desired atmospheric data points (object with fields below):
            .lat    - degrees latitude (+N,-S)
            .long   - degrees longitude (+E,-W)
            .alt    - altitude (km)
    Outputs:
        _grid_out   - atmospheric properties at each cone point (object with fields below):
            .lat    - degrees latitude (+N,-S)
            .long   - degrees longitude (+E,-W)
            .alt    - altitude (km)
            .vx     - E-W wind speed (m/s)
            .vy     - N-S wind speed (m/s)
            .vz     - vertical wind speed (m/s)
            .rho    - atmospheric density (kg/m^3)
            .temp   - temperature (K)
            .p      - pressure (N/m^2)
    -----------------------------------------------------------------------------------------"""

## input file ##

    try:
        os.chdir('../phase1/models/')
    except:
        'Already in correct directory'
    
    # open and read input file from repository
    f =  open("earthgram/InputFile.txt",'r')
    input_txt = f.readlines()
    f.close()

    os.remove("earthgram/InputFile.txt")      # remove original file

    f = open("earthgram/InputFile.txt",'w')   # create new file

    # update starting date and time
    input_txt[23] = f'  mn = {_balloon_state.date_time.month}\n'
    input_txt[24] = f'  ida = {_balloon_state.date_time.day}\n'
    input_txt[25] = f'  iyr = {_balloon_state.date_time.year}\n'
    input_txt[26] = f'  ihro = {_balloon_state.date_time.hour}\n'
    input_txt[27] = f'  mino = {_balloon_state.date_time.minute}\n'
    input_txt[28] = f'  seco = {_balloon_state.date_time.second}\n'

    # update and close new input file
    f.writelines(input_txt)
    f.close()

## initialization ##

    elapsed_time = [] # elapsed seconds since initial balloon state based on current altitude and vz

    for x in _gram_grid.alt:
        if _balloon_state.alt < 0:
            _balloon_state.alt = 0
        elapsed_time.append((x*1000 - _balloon_state.alt)/_balloon_state.vert_speed)

    with open('earthgram/traj_file.txt','w') as f:    # open text file
        f.writelines('')                    # clear file content
        for i in range(len(_gram_grid.alt)): # write trajectory file in format accepted by EarthGRAM
            f.write("{}\t{}\t{}\t{}\n".format(
                elapsed_time[i],_gram_grid.alt[i],_gram_grid.lat[i],_gram_grid.long[i]))

## Run EarthGRAM.exe to generate atmospheric data

    RunningGram()

## output formatting ##
    with open('earthgram/output.txt', newline = '') as f:   # open and read EarthGRAM output file
        output_txt = f.readlines()

    # os.remove('earthgram/output.txt')

    start_line = 0
    for i in range(len(output_txt)):
        if "-------" in output_txt[i]:
            if "Position" in output_txt[i+1]:
                start_line = i + 3
                break
            elif "Ruv" in output_txt[i+1]:
                continue
            else:
                start_line = i + 1
                break

    if start_line == 0:
        print("Issue with Output.txt Formatting")
        sys.exit()

    grid_out_list = []  # initialize output data list

    for i in range(len(_gram_grid.alt)):         # store desired output data
        temporary_var = output_txt[start_line + 13*i].split()   # pull data from correct output text file lines
  
        floats = []
        for val in temporary_var[0:9]:
            floats.append(float(val))   # convert strings to floats

        # append current point's data to output list
        grid_out_list.append(OutputGrid(floats[0],floats[1],floats[2],floats[3],floats[4],floats[5],floats[6],floats[7],floats[8]))

    return grid_out_list

## output data class ##
@dataclass
class OutputGrid:
    """
    Creates data structure class to organize earthGRAM output data into an output object
    """
    alt: ty.List[float]
    lat: ty.List[float]
    long: ty.List[float]
    p: ty.List[float]
    rho: ty.List[float]
    temp: ty.List[float]
    vE: ty.List[float]
    vN: ty.List[float]
    vz: ty.List[float]