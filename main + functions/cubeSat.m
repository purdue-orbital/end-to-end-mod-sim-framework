function [vars] = cubeSat(vars)
fprintf('...Creating Satellite\n');
satellite = vars.stkInterface.root.CurrentScenario.Children.New('eSatellite', vars.objects.vehicles.satellite.name);
model = satellite.VO.Model;
model.ModelData.Filename = vars.objects.vehicles.satellite.modelPath;
satellite.SetPropagatorType(vars.objects.vehicles.satellite.propagator);

forceModel = satellite.Propagator.ForceModel;
forceModel.CentralBodyGravity.File = vars.objects.vehicles.satellite.forceModel.CentralBodyGravityFile;
forceModel.CentralBodyGravity.MaxDegree = vars.objects.vehicles.satellite.forceModel.MaxDegree;
forceModel.CentralBodyGravity.MaxOrder = vars.objects.vehicles.satellite.forceModel.MaxOrder;
forceModel.Drag.Use = vars.objects.vehicles.satellite.drag.Use;
forceModel.Drag.DragModel.Cd = vars.objects.vehicles.satellite.drag.DragModel.Cd;
forceModel.Drag.DragModel.AreaMassRatio = 0.01; % m^2 / kg
forceModel.SolarRadiationPressure.Use = vars.objects.vehicles.satellite.forceModel.SolarRadiationPressure.Use;
satellite.Propagator.Propagate;

satellite.Propagator.InitialState.Representation.AssignCartesian('eCoordinateSystemICRF', vars.objects.vehicles.icarus.rockX(end), vars.objects.vehicles.icarus.rockY(end), vars.objects.vehicles.icarus.rockZ(end), vars.objects.vehicles.icarus.rockVX(end), vars.objects.vehicles.icarus.rockVY(end), vars.objects.vehicles.icarus.rockVZ(end));
satellite.Propagator.Propagate;
satPock = satellite.Vgt.Events.Factory.CreateSmartEpochFromTime(vars.objects.vehicles.icarus.rockTime(end));
satellite.Propagator.EphemerisInterval.SetStartEpochAndDuration(satPock, vars.objects.vehicles.satellite.epochDuration);
satellite.Propagator.InitialState.OrbitEpoch.SetExplicitTime(vars.objects.vehicles.icarus.rockTime(end));
satellite.Propagator.Propagate;
satPosDP = satellite.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(vars.stkInterface.scenario.StartTime, vars.stkInterface.scenario.StopTime, 60); % seconds
satTime = cell2mat(satPosDP.DataSets.GetDataSetByName('Time').GetValues); % seconds
satX = cell2mat(satPosDP.DataSets.GetDataSetByName('x').GetValues); % kilometers
satY = cell2mat(satPosDP.DataSets.GetDataSetByName('y').GetValues);
satZ = cell2mat(satPosDP.DataSets.GetDataSetByName('z').GetValues);

%satPos2DP = satellite.DataProviders.Item('LLA State').Group.Item('Fixed').Exec(scenario.StartTime, scenario.StopTime, 60); % seconds
% satLat = cell2mat(satPos2DP.DataSets.GetDataSetByName('Lat').GetValues);
% satLon = cell2mat(satPos2DP.DataSets.GetDataSetByName('Lon').GetValues);
% satAlt = cell2mat(satPos2DP.DataSets.GetDataSetByName('Alt').GetValues);

%adding outputs to path
vars.objects.vehicles.satellite.object = satellite;
vars.objects.vehicles.satellite.satPosDP = satPosDP;
vars.objects.vehicles.satellite.satTime = satTime;
vars.objects.vehicles.satellite.satX = satX;
vars.objects.vehicles.satellite.satY = satY;
vars.objects.vehicles.satellite.satZ = satZ;