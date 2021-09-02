import numpy as np
import user_input


def single_run_launch_platform_6dof(weather_model):

    if weather_model == 'Historical':
        pass
        # Use historical weather data
    # Code for launch platform 6dof goes here!

    run_result = 1
    drift_altitude = 25000
    return run_result, drift_altitude


if "__main__":
    inputs = user_input.user_input()
    if inputs.mode == 1:
        run_status, drift_altitude = single_run_launch_platform_6dof(inputs.weather_model)
        if run_status == -1:
            print('Run failed!')
        elif run_status == 1:
            print('Run succeeded!')
            "Balloon drifted to an altitude of {} km".format(drift_altitude)
