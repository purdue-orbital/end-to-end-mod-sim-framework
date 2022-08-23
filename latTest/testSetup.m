function [stkInterface] = testSetup()
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
    root.NewScenario('WIP_Scenario');
    scenario = root.CurrentScenario;
    scenario.SetTimePeriod('20 Jan 2020 17:00:00.000','+14 days'); % Increase to analyze satellite lifespan
end

root.ExecuteCommand('Animate * Reset');
root.ExecuteCommand('Application / Raise');
root.ExecuteCommand('Application / Maximize');
root.ExecuteCommand('Window3D * Maximize');

root.UnitPreferences.Item('DateFormat').SetCurrentUnit('EpSec');

stkInterface.scenario = scenario;
stkInterface.root = root;
stkInterface.uiapp = uiapp;