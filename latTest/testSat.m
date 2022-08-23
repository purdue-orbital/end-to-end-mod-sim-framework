function deorbitTime = testSat(stkInterface, xV, iteration, cubeSatMass, areaMassRatio)

satName = 'testCubeSat%d';
satName = sprintf(satName, iteration);
satellite = stkInterface.root.CurrentScenario.Children.New('eSatellite', satName);
satellite.SetPropagatorType('ePropagatorHPOP');

forceModel = satellite.Propagator.ForceModel;
forceModel.CentralBodyGravity.File = 'C:\Program Files\AGI\STK 11\STKData\CentralBodies\Earth\WGS84_EGM96.grv';
forceModel.CentralBodyGravity.MaxDegree = 21;
forceModel.CentralBodyGravity.MaxOrder = 21;
forceModel.Drag.Use = 1;
forceModel.Drag.DragModel.Cd = 2.2;
forceModel.Drag.DragModel.AreaMassRatio = areaMassRatio;
forceModel.SolarRadiationPressure.Use = 0;
forceModel.MoreOptions.Static.SatelliteMass = cubeSatMass;


satellite.Propagator.Propagate;
satellite.Propagator.InitialState.Representation.AssignCartesian('eCoordinateSystemICRF', xV.rockX(end), xV.rockY(end), xV.rockZ(end), xV.rockVX(end), xV.rockVY(end), xV.rockVZ(end));
keplerian = satellite.Propagator.InitialState.Representation.ConvertTo('eOrbitStateClassical');

m = 3.986*10^5;
disp(xV.burnoutV);
r = 6371+150;

SMA = -(m*r)/(r*xV.burnoutV^2 - 2*m);
disp(SMA);
keplerian.SizeShape.SemimajorAxis = SMA;
%e = 
%keplerian.SizeShape.eccentricity = e;
satellite.Propagator.InitialState.Representation.Assign(keplerian);
try
    satellite.Propagator.Propagate;
catch
end

% returns = satellite.Propagator.InitialState.Representation.ConvertTo('eOrbitStateCartesian');
% satellite.Propagator.InitialState.Representation.Assign(returns);
try
    satellite.Propagator.Propagate;
catch
end

satPock = satellite.Vgt.Events.Factory.CreateSmartEpochFromTime(xV.rockTime(end));
satellite.Propagator.EphemerisInterval.SetStartEpochAndDuration(satPock, '+14d');
satellite.Propagator.InitialState.OrbitEpoch.SetExplicitTime(xV.rockTime(end));

try
    satellite.Propagator.Propagate;
catch
end


satPosDP = satellite.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(stkInterface.scenario.StartTime, stkInterface.scenario.StopTime, 60); % seconds
deorbitTime = cell2mat(satPosDP.DataSets.GetDataSetByName('Time').GetValues); % seconds
deorbitTime = deorbitTime(end);

 
% if deorbitTime/60/95 >= 6 
%     deorbitTime = NaN;
% end

% style = 'vehicleTemp';
% file1 = 'C:\Users\rlusthau\OneDrive - purdue.edu\Desktop\TempGraphs\file1';
% file2 = 'C:\Users\rlusthau\OneDrive - purdue.edu\Desktop\TempGraphs\file2';
% command1 = 'GraphCreate */Satellite/testCubeSat1 Type Save Style "%s" File "%s"';
% command2 = 'GraphCreate */Satellite/testCubeSat%d Type Save Style "%s" File "%s"';
% format1 = sprintf(command1, style, file1);
% format2 = sprintf(command1, style, file2);
% if z == 1    
%     if iteration == 1
%         stkInterface.root.ExecuteCommand(format1);
%     end     
%     if iteration == 5
%         stkInterface.root.ExecuteCommand(format2);
%     end
% end
%satX = cell2mat(satPosDP.DataSets.GetDataSetByName('x').GetValues); % kilometers
%satY = cell2mat(satPosDP.DataSets.GetDataSetByName('y').GetValues);
%satZ = cell2mat(satPosDP.DataSets.GetDataSetByName('z').GetValues);