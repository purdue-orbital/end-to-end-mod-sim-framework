def writeTrajFile(BALLOON,CONE):
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

    elapsed_time = []       # elapsed seconds since initial balloon state based on altitude and vz

    for x in CONE.ALT:
        elapsed_time.append((x - BALLOON.ALT)*1000/BALLOON.VZ)
    
    with open('cone_file.txt','w') as f:  # open text file
        f.writelines('')

    for i in range(len(CONE.LAT)):
        f.write("{}\t{}\t{}\t{}".format(elapsed_time(i),CONE.ALT(i),CONE.LAT(i),CONE.LONG(i)))