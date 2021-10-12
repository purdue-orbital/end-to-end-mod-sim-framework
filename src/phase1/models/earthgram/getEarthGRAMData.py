def getEarthGRAMData(BALLOON,CONE1):
    """-----------------------------------------------------------------------------------------
    CONE_OUT = writeTrajFile(T,V,CONE)
    Function to write txt file with atmosphere cone to input to EarthGRAM
    Inputs:
        BALLOON     - structure state at current time (object with fields below):
            .T      - current time (datetime)
            .LAT    - degrees latitude (+N,-S)
            .LONG   - degrees longitude (+E,-W)
            .ALT    - altitude (km)
            .VZ     - current vertical speed (m/s)
        CONE - desired atmospheric data points (object with fields below):
            .LAT    - degrees latitude (+N,-S)
            .LONG   - degrees longitude (+E,-W)
            .ALT    - altitude (km)
    Outputs:
        CONE_OUT    - atmospheric properties at each cone point (object with fields below):
            .LAT    - degrees latitude (+N,-S)
            .LONG   - degrees longitude (+E,-W)
            .ALT    - altitude (km)
            .VX     - E-W wind speed (m/s)
            .VY     - N-S wind speed (m/s)
            .VZ     - vertical wind speed (m/s)
            .RHO    - atmospheric density (kg/m^3)
            .TEMP   - temperature (K)
            .P      - pressure (N/m^2)
    -----------------------------------------------------------------------------------------"""

    elapsed_time = []       # elapsed seconds since initial balloon state based on current altitude and vz

    for x in CONE1.ALT:
        elapsed_time.append((x - BALLOON.ALT)*1000/BALLOON.VZ)
    
    with open('cone_file.txt','w') as f:    # open text file
        f.writelines('')                    # clear file content
        for i in range(len(CONE1.ALT)):     # write trajectory file in format accepted by EarthGRAM
            f.write("{}\t{}\t{}\t{}\n".format(elapsed_time[i],CONE1.ALT[i],CONE1.LAT[i],CONE1.LONG[i]))

    """Placeholder to call EarthGRAM.exe to run trajectory file. Note, the "Input file" passed to Earth gram will be preset in the git repo
    and will not need to be edited between simulations. Only the Trajectory file gets updated, which is automated through the use of this 
    function."""

    