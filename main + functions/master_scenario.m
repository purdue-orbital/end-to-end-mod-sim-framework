clear;
clc;

%Scenario properties
vars.scenario.name = 'WIP_Scenario';
vars.scenario.timePeriod = '20 Jan 2020 17:00:00.000';
vars.scenario.lifespan = '+365 days';

%Facility properties
vars.objects.other.facility.name = 'Launch';
vars.objects.other.facility.latitude = 28.3922;
vars.objects.other.facility.longitude = -80.6077;
vars.objects.other.facility.altitude = 0.0;

%Balloon properties
vars.objects.vehicles.balloon.name = 'Balloon';
vars.objects.vehicles.balloon.ephemPath = 'U:\Orbital\scenario_files\balloon_ephem.e';
vars.objects.vehicles.balloon.modelPath = '\\nas01.itap.purdue.edu\puhome\Orbital\scenario_files\weather_balloon.mdl';
vars.objects.vehicles.balloon.altOffset = 36;    %meters up

%Icarus properties
vars.objects.vehicles.icarus.name = 'Icarus';
%vars.objects.vehicles.icarus.ephemPath = 
vars.objects.vehicles.icarus.modelPath = '\\nas01.itap.purdue.edu\puhome\Orbital\scenario_files\int2_less1.mdl';
vars.objects.vehicles.icarus.epochDuration = '+1d';

%Satellite properties
vars.objects.vehicles.satellite.name = 'CubeSat';
vars.objects.vehicles.satellite.modelPath = '\\nas01.itap.purdue.edu\puhome\Orbital\scenario_files\cubesat_1u.dae';
vars.objects.vehicles.satellite.propagator = 'ePropagatorHPOP';
vars.objects.vehicles.satellite.forceModel.CentralBodyGravityFile = 'C:\Program Files\AGI\STK 11\STKData\CentralBodies\Earth\WGS84_EGM96.grv';
vars.objects.vehicles.satellite.forceModel.MaxDegree = 21;
vars.objects.vehicles.satellite.forceModel.MaxOrder = 21;
vars.objects.vehicles.satellite.drag.Use = 1;
vars.objects.vehicles.satellite.drag.DragModel.Cd = 0.01;
vars.objects.vehicles.satellite.drag.AreaMassRatio = 0.01; % m^2 / kg
vars.objects.vehicles.satellite.forceModel.SolarRadiationPressure.Use = 0;
vars.objects.vehicles.satellite.epochDuration = '+14d';

%Camera properties
vars.objects.vehicles.camera.name = 'Camera';
vars.objects.vehicles.camera.modelOffset = 10;    %m up






%Set up scenario and create launch facility with (facilLat, facilLon, facilAlt), returning
%scenario object and root
[vars] = setup(vars);

%Creating the balloon with the above paths,returning the aircraft object and
%properties
[vars] = balloon(vars);

%Creating icarus with the above paths, returning the rocket object and
%properties
[vars] = icarus(vars);

%Creating the satellite with above model path
[vars] = cubeSat(vars);

%Creating the camera and getting rid of the model
[vars] = camera(vars);

% Plot time for CubeSat to decay as a function of Icarus burn velocity
% i = 1;
% k = .01; % burnV steps
% satDecay = 7.4:k:8.6; % km
% for burnV = 7.4:k:8.6
%     rocket.Trajectory.InitialState.BurnoutVel = burnV;
%     rocket.Trajectory.Propagate;
%     rockPosDP = rocket.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(scenario.StartTime, scenario.StopTime, 60); % seconds
%     rockVelDP = rocket.DataProviders.Item('Cartesian Velocity').Group.Item('ICRF').Exec(scenario.StartTime, scenario.StopTime, 60);
%     rockTime = cell2mat(rockPosDP.DataSets.GetDataSetByName('Time').GetValues);
%     rockX = cell2mat(rockPosDP.DataSets.GetDataSetByName('x').GetValues); % seconds
%     rockY = cell2mat(rockPosDP.DataSets.GetDataSetByName('y').GetValues); % kilometers
%     rockZ = cell2mat(rockPosDP.DataSets.GetDataSetByName('z').GetValues);
%     rockVX = cell2mat(rockVelDP.DataSets.GetDataSetByName('x').GetValues);
%     rockVY = cell2mat(rockVelDP.DataSets.GetDataSetByName('y').GetValues);
%     rockVZ = cell2mat(rockVelDP.DataSets.GetDataSetByName('z').GetValues);
%     satPock = satellite.Vgt.Events.Factory.CreateSmartEpochFromTime(rockTime(end));
%     satellite.Propagator.EphemerisInterval.SetStartEpochAndDuration(satPock, '+1d');
%     satellite.Propagator.InitialState.OrbitEpoch.SetExplicitTime(rockTime(end))
%     satellite.Propagator.InitialState.Representation.AssignCartesian('eCoordinateSystemICRF', rockX(end), rockY(end), rockZ(end), rockVX(end), rockVY(end), rockVZ(end));
%     satellite.Propagator.Propagate;
%     satLife = root.ExecuteCommand('Lifetime */Satellite/CubeSat');
%     satReport = satLife.Item(0);
%     char = strlength(satReport);
%     if char > 53
%         satDecay(i) = sscanf(satReport((char - 9):(char - 7)), '%f'); % years
%         fprintf('...CubeSat %d/%d decayed\n', i, numel(satDecay));
%     elseif char == 52
%         satDecay(i) = 0; % large value representing no decay
%         fprintf('...CubeSat %d/%d does not decay within the 99999 orbit limit\n', i, numel(satDecay));
%     else
%         satDecay(i) = 0;
%         fprintf('...CubeSat %d/%d decayed before Lifetime computations could begin\n', i, numel(satDecay));
%     end
%         
%     root.ExecuteCommand('SetUnits / km sec EpSec')
%     root.ExecuteCommand('ReportOptions */Satellite/CubeSat UseTimeArrayGrid On');
%     satLife = root.ExecuteCommand('SetUnits / km sec EpSec Report_RM */Satellite/CubeSat Style "Lifetime"');
%     satDeorbit = satLife.Item(satLife.Count - 2);
%     satDP = satellite.DataProviders.Item('Lifetime').Exec(scenario.StartTime, scenario.StopTime, 60);
%     satTime = cell2mat(satDP.DataSets.GetDataSetByName('Time').GetValues);
%         
%     i = i + 1;
% end
% burnV = 7.4:k:8.6;
% plot(burnV, satDecay, 'b', 'linewidth', 1.5);
% title('CubeSat Lifetime due to Icarus Burn Velocity')
% xlabel('Icarus Burn Velocity (km/s)') 
% ylabel('CubeSat Time to Decay (years)')

%Plot time for CubeSat to decay as a function of Icarus burn velocity
% i = 1;
% k = .1; % burnV steps
% for burnV = 6:k:10
%     rocket.Trajectory.InitialState.BurnoutVel = burnV;
%     rocket.Trajectory.Propagate;
%     rockPosDP = rocket.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(scenario.StartTime, scenario.StopTime, 60); % seconds
%     rockVelDP = rocket.DataProviders.Item('Cartesian Velocity').Group.Item('ICRF').Exec(scenario.StartTime, scenario.StopTime, 60);
%     rockTime = cell2mat(rockPosDP.DataSets.GetDataSetByName('Time').GetValues);
%     rockX = cell2mat(rockPosDP.DataSets.GetDataSetByName('x').GetValues); % seconds
%     rockY = cell2mat(rockPosDP.DataSets.GetDataSetByName('y').GetValues); % kilometers
%     rockZ = cell2mat(rockPosDP.DataSets.GetDataSetByName('z').GetValues);
%     rockVX = cell2mat(rockVelDP.DataSets.GetDataSetByName('x').GetValues);
%     rockVY = cell2mat(rockVelDP.DataSets.GetDataSetByName('y').GetValues);
%     rockVZ = cell2mat(rockVelDP.DataSets.GetDataSetByName('z').GetValues);
%     satPock = satellite.Vgt.Events.Factory.CreateSmartEpochFromTime(rockTime(end));
%     satellite.Propagator.EphemerisInterval.SetStartEpochAndDuration(satPock, '+14d');
%     satellite.Propagator.InitialState.OrbitEpoch.SetExplicitTime(rockTime(end))
%     satellite.Propagator.InitialState.Representation.AssignCartesian('eCoordinateSystemICRF', rockX(end), rockY(end), rockZ(end), rockVX(end), rockVY(end), rockVZ(end));
%     satellite.Propagator.Propagate;
%     satPosDP = satellite.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(scenario.StartTime, scenario.StopTime, 60); % seconds
%     satTime = cell2mat(satPosDP.DataSets.GetDataSetByName('Time').GetValues); % seconds
%     satX = cell2mat(satPosDP.DataSets.GetDataSetByName('x').GetValues);
%     satY = cell2mat(satPosDP.DataSets.GetDataSetByName('y').GetValues);
%     satZ = cell2mat(satPosDP.DataSets.GetDataSetByName('z').GetValues);
%     
%     for j = 1:numel(satTime)
%         satAlt = sqrt(satX(j)^2 + satY(j)^2 + satZ(j)^2) - 6371;
%         if satAlt <= 100
%             satDecay(i) = satTime(j);
%             fprintf('...CubeSat %d/%d decayed\n', i, numel(satDecay));
%             break;
%         end
%     end
%     
%     i = i + 1;
% end
% burnV = 6:k:10;
% plot(burnV, satDecay, 'b', 'linewidth', 1.5);
% title('CubeSat Lifetime due to Icarus Burn Velocity')
% xlabel('Icarus Burn Velocity (km/s)') 
% ylabel('CubeSat Time to Decay (sec)')

% % %     rocket.Trajectory.InitialState.BurnoutVel = 7.4;
% % %     rocket.Trajectory.Propagate;
% % %     rockPosDP = rocket.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(scenario.StartTime, scenario.StopTime, 60); % seconds
% % %     rockVelDP = rocket.DataProviders.Item('Cartesian Velocity').Group.Item('ICRF').Exec(scenario.StartTime, scenario.StopTime, 60);
% % %     rockTime = cell2mat(rockPosDP.DataSets.GetDataSetByName('Time').GetValues);
% % %     rockX = cell2mat(rockPosDP.DataSets.GetDataSetByName('x').GetValues); % seconds
% % %     rockY = cell2mat(rockPosDP.DataSets.GetDataSetByName('y').GetValues); % kilometers
% % %     rockZ = cell2mat(rockPosDP.DataSets.GetDataSetByName('z').GetValues);
% % %     rockVX = cell2mat(rockVelDP.DataSets.GetDataSetByName('x').GetValues);
% % %     rockVY = cell2mat(rockVelDP.DataSets.GetDataSetByName('y').GetValues);
% % %     rockVZ = cell2mat(rockVelDP.DataSets.GetDataSetByName('z').GetValues);
% % %     satPock = satellite.Vgt.Events.Factory.CreateSmartEpochFromTime(rockTime(end));
% % %     satellite.Propagator.EphemerisInterval.SetStartEpochAndDuration(satPock, '+1d');
% % %     satellite.Propagator.InitialState.OrbitEpoch.SetExplicitTime(rockTime(end))
% % %     satellite.Propagator.InitialState.Representation.AssignCartesian('eCoordinateSystemICRF', rockX(end), rockY(end), rockZ(end), rockVX(end), rockVY(end), rockVZ(end));
% % %     satellite.Propagator.Propagate;
% % %     satPosDP = satellite.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(scenario.StartTime, scenario.StopTime, 60); % seconds
% % %     satTime = cell2mat(satPosDP.DataSets.GetDataSetByName('Time').GetValues); % seconds
% % %     satX = cell2mat(satPosDP.DataSets.GetDataSetByName('x').GetValues);
% % %     satY = cell2mat(satPosDP.DataSets.GetDataSetByName('y').GetValues);
% % %     satZ = cell2mat(satPosDP.DataSets.GetDataSetByName('z').GetValues);
% % %     
% % %     satAlt = (satX.^2 + satY.^2 + satZ.^2).^.5 - 6371;
% % %     plot(satTime, satAlt, 'b', 'linewidth', 1.5);
    
fprintf('...All Done!\n');



