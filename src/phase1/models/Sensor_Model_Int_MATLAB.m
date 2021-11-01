
fprintf('...Calling STK\n');
try
    % Grab an existing instance of STK
    uiapp = actxGetRunningServer('STK11.application');
    %Attach to the STK Object Model
    root = uiapp.Personality2;
    checkempty = root.Children.Count;
    if checkempty == 0
        %If a Scenario is not open, create a new scenario
        uiapp.visible = 1;
        root.NewScenario('ASTG_OM_Test');
        scenario = root.CurrentScenario;
    else
        %If a Scenario is open, prompt the user to accept closing it or not
        rtn = questdlg({'Close the current scenario?',' ','(WARNING: If you have not saved your progress will be lost)'});
        if ~strcmp(rtn,'Yes')
            return
        else
            root.CurrentScenario.Unload
            uiapp.visible = 1;
            root.NewScenario('ASTG_OM_Test');
            scenario = root.CurrentScenario;
        end
    end

catch
    uiapp = actxserver('STK11.application');
    root = uiapp.Personality2;
    uiapp.visible = 1;
    root.NewScenario('Balloon_Drift_Sensor_Model');
    scenario = root.CurrentScenario;
    scenario.SetTimePeriod('20 Jan 2020 17:00:00.000','+2 hours')
end

root.ExecuteCommand('Animate * Reset')
root.ExecuteCommand('Application / Raise')
root.ExecuteCommand('Application / Maximize')
root.ExecuteCommand('Window3D * Maximize')

fprintf('...Adding Cape Canaveral Facility\n');
facility = scenario.Children.New('eFacility','Cape_Canaveral');
facility.Position.AssignGeodetic(28.3922, -80.6077, 0.0);

fprintf('...Adding Sensors\n');

ref_dis = 1;
pat_num = 1;
red = 0;
blue = 255;

x = input('Project data in terms of height (0) or time (1) steps?\n');

if x == 1
    time_int = 0;
    time_step = 1;
    time_max = input('How many pointer files are present?\n');
    color_shift = 255 / (time_max / time_step);
    for pat_num = 1:time_max
        sensor = facility.Children.New('eSensor', 'Sensor_' + string(pat_num) + 's');
        sensor.Graphics.Color = red*65536 + blue;
        sensor.CommonTasks.SetPatternCustom('sensorpattern_' + string(pat_num) + '.Pattern')
        sensor.SetPointingExternalFile('sensorpointer_' + string(pat_num) + '.sp')
        sensor.VO.SpaceProjection = ref_dis;
        sensor.Graphics.LineWidth = 5;
        sensor.VO.PercentTranslucency = 100;
        sensor.VO.TranslucentLinesVisible = 0;
        blue = blue - color_shift;
        red = red + color_shift;
        time_int = time_int + time_step;
    end  
end

if x == 0
    ref_dis = 0;
    max_height = float(input('How many pattern files are present?\n'));
    color_shift = 255 / (max_height - ref_dis);
    for pat_num = 1:max_height
        sensor = facility.Children.New('eSensor', 'Sensor_' + string(pat_num) + 's');
        sensor.Graphics.Color = red*65536 + blue;
        sensor.CommonTasks.SetPatternCustom('sensorpattern_' + string(pat_num) + '.Pattern')
        sensor.SetPointingExternalFile('sensorpointer_' + string(pat_num) + '.sp')
        sensor.VO.SpaceProjection = ref_dis;
        sensor.Graphics.LineWidth = 5;
        sensor.VO.PercentTranslucency = 100;
        sensor.VO.TranslucentLinesVisible = 0;
        blue = blue - color_shift;
        red = red + color_shift;
        ref_dis = ref_dis + 1;
    end
end

fprintf('...Finished!')