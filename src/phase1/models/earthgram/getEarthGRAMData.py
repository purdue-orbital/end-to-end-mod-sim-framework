import datetime
import os
from dataclasses import dataclass
import typing as ty

def getEarthGRAMData(_balloon_state,_gram_grid):
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

    # open and read input file from repository
    f =  open("InputFile.txt",'r')
    input_txt = f.readlines()
    f.close()

    os.remove("InputFile.txt")      # remove original file

    f = open("InputFile.txt",'w')   # create new file

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

    elapsed_time = []       # elapsed seconds since initial balloon state based on current altitude and vz

    for x in _gram_grid.alt:
        elapsed_time.append((x - _balloon_state.alt)*1000/_balloon_state.vert_speed)
    
    with open('traj_file.txt','w') as f:    # open text file
        f.writelines('')                    # clear file content
        for i in range(len(_gram_grid.alt)):     # write trajectory file in format accepted by EarthGRAM
            f.write("{}\t{}\t{}\t{}\n".format(elapsed_time[i],_gram_grid.alt[i],_gram_grid.lat[i],_gram_grid.long[i]))

    """Placeholder to call EarthGRAM.exe to run trajectory file. Note, the "Input file" passed to Earth gram will be preset in the git repo
    and will not need to be edited between simulations. Only the Trajectory file gets updated, which is automated through the use of this 
    function."""

## output formatting ##
    with open('output.txt', newline = '') as f:     # open and read earthGRAM output file
	    output_txt = f.readlines()

    temporary_var = []  # temporary variable for data storage in for loop

    _grid_out = OutputGrid([],[],[],[],[],[],[],[],[])  # initialize output data object

    for i in range(len(output_txt)):        # find starting line to read data
        if "Positions generated" in output_txt[i]:
            start_line = i + 2
            break
        else:
            start_line = 35

    for i in x:         # store desired output data
        temporary_var = output_txt[start_line + 13*i].split()

        _grid_out.alt.append(temporary_var[0])
        _grid_out.lat.append(temporary_var[1])
        _grid_out.long.append(temporary_var[2])
        _grid_out.p.append(temporary_var[3])
        _grid_out.rho.append(temporary_var[4])
        _grid_out.temp.append(temporary_var[5])
        _grid_out.vE.append(temporary_var[6])
        _grid_out.vN.append(temporary_var[7])
        _grid_out.vz.append(temporary_var[8])

    return _grid_out

@dataclass
class OutputGrid:
    """
    Creates data structure class to organize earthGRAM output data into an output object
    """
    lat: ty.List[float]
    long: ty.List[float]
    alt: ty.List[float]
    vE: ty.List[float]
    vN: ty.List[float]
    vz: ty.List[float]
    rho: ty.List[float]
    temp: ty.List[float]
    p: ty.List[float]