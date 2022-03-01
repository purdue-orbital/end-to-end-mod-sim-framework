function [vars] = balloon(vars)

% cd '\\nas01.itap.purdue.edu\puhome\My Documents\STK 11 (x64)'
fprintf('...Creating Balloon\n');
aircraft = vars.stkInterface.scenario.Children.New('eAircraft', vars.objects.vehicles.balloon.name);
%string for root command to set the ephemeris (has to be done to pass the
%path into the command
ephemCommandString = 'SetState */Aircraft/Balloon FromFile "%s"';
formatedEphemCommandString = sprintf(ephemCommandString, vars.objects.vehicles.balloon.ephemPath);
vars.stkInterface.root.ExecuteCommand(formatedEphemCommandString);
model = aircraft.VO.Model;
model.ModelData.Filename = vars.objects.vehicles.balloon.modelPath;
vars.stkInterface.root.ExecuteCommand('SetAttitude */Aircraft/Balloon Profile AlignConstrain Axis 0 0 1 "Nadir(Detic)" Axis 1 0 0 "Velocity(CBF)"');

unFormatedOffsetCommand = 'VO */Aircraft/Balloon ModelOffset Translational On 0 0 -%d';
offsetCommand = sprintf(unFormatedOffsetCommand, vars.objects.vehicles.balloon.altOffset);
vars.stkInterface.root.ExecuteCommand(offsetCommand);

airPosDP = aircraft.DataProviders.Item('LLA State').Group.Item('Fixed').Exec(vars.stkInterface.scenario.StartTime, vars.stkInterface.scenario.StopTime, 60);
airTime = cell2mat(airPosDP.DataSets.GetDataSetByName('Time').GetValues);
airLat = cell2mat(airPosDP.DataSets.GetDataSetByName('Lat').GetValues);
airLon = cell2mat(airPosDP.DataSets.GetDataSetByName('Lon').GetValues);
airAlt = cell2mat(airPosDP.DataSets.GetDataSetByName('Alt').GetValues);


%adding outputs to vars
vars.objects.vehicles.balloon.object = aircraft;
vars.objects.vehicles.balloon.airPosDP = airPosDP;
vars.objects.vehicles.balloon.airTime = airTime;
vars.objects.vehicles.balloon.airLat = airLat;
vars.objects.vehicles.balloon.airLon = airLon;
vars.objects.vehicles.balloon.airAlt = airAlt;
