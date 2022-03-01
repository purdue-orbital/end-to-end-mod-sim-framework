function [vars] = setup(vars)
%cd '\\nas01.itap.purdue.edu\puhome\My Documents\STK 11 (x64)'
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
        rtn = questdlg({'Close the current scenario?', ' ', '(WARNING: If you have not saved your progress will be lost)'});
        if ~strcmp(rtn, 'Yes')
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
    root.NewScenario(vars.scenario.name);
    scenario = root.CurrentScenario;
    scenario.SetTimePeriod(vars.scenario.timePeriod,vars.scenario.lifespan); % Increase to analyze satellite lifespan
end

root.ExecuteCommand('Animate * Reset');
root.ExecuteCommand('Application / Raise');
root.ExecuteCommand('Application / Maximize');
root.ExecuteCommand('Window3D * Maximize');

root.UnitPreferences.Item('DateFormat').SetCurrentUnit('EpSec');
fprintf('...Creating Cape Canaveral Facility\n');
facility = scenario.Children.New('eFacility',vars.objects.other.facility.name);
facility.Position.AssignGeodetic(vars.objects.other.facility.latitude, vars.objects.other.facility.longitude, vars.objects.other.facility.altitude);
facility.Graphics.Color = 255*256;

%adding outputs to vars
vars.objects.other.facility.Object = facility;
vars.stkInterface.scenario = scenario;
vars.stkInterface.root = root;
vars.stkInterface.uiapp = uiapp;

