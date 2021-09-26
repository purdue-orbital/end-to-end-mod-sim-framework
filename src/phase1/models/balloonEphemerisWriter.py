#!/usr/bin/env python3
def balloonEphemerisWriter(propStartDate, ephemStates, ephemTimes, fname): #Takes in UTCG propagation start date, ephemeris states, ephemeris time, and filename for output
    ephemHeader = f"""stk.v.12.0
    
    # WrittenBy    STK_v12.2.0
    
    BEGIN Ephemeris
        NumberOfEphemerisPoints		 193
        ScenarioEpoch		 {propStartDate}
        InterpolationMethod		 Lagrange
        InterpolationSamplesM1		 7
        CentralBody		 Earth
        CoordinateSystem		 ICRF
    
        EphemerisTimePosVel	"""

    with open(f"{fname}.e", "w") as f:
        f.write(ephemHeader)
        f.write("\n")
        for i, point in enumerate(ephemStates):
            f.write(f"{ephemTimes[i]} {point[0]} {point[1]} {point[2]} {point[3]} {point[4]} {point[5]}\n")


balloonEphemerisWriter('6 Aug 2021 23:59:42.000000', [[7000, 0, 0, 10, 0, 0], [8000, 0, 0, 0, 0, 0]], [0, 100], 'balloon')