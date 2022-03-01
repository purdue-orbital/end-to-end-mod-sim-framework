function [vars] = icarus(vars)

fprintf('...Creating Rocket\n');
rocket = vars.stkInterface.root.CurrentScenario.Children.New('eLaunchVehicle', vars.objects.vehicles.icarus.name);
rocket.Trajectory.InitialState.Launch.AssignGeodetic(vars.objects.vehicles.balloon.airLat(end), vars.objects.vehicles.balloon.airLon(end), vars.objects.vehicles.balloon.airAlt(end));
model = rocket.VO.Model;
model.ModelData.Filename = vars.objects.vehicles.icarus.modelPath;
rockPock = rocket.Vgt.Events.Factory.CreateSmartEpochFromTime(vars.objects.vehicles.balloon.airTime(end));
rocket.Trajectory.EphemerisInterval.SetStartEpochAndDuration(rockPock, vars.objects.vehicles.icarus.epochDuration);
rocket.Trajectory.Propagate;

rockPosDP = rocket.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(vars.stkInterface.scenario.StartTime, vars.stkInterface.scenario.StopTime, 60); % seconds
rockVelDP = rocket.DataProviders.Item('Cartesian Velocity').Group.Item('ICRF').Exec(vars.stkInterface.scenario.StartTime, vars.stkInterface.scenario.StopTime, 60);
rockTime = cell2mat(rockPosDP.DataSets.GetDataSetByName('Time').GetValues);
rockX = cell2mat(rockPosDP.DataSets.GetDataSetByName('x').GetValues); % seconds
rockY = cell2mat(rockPosDP.DataSets.GetDataSetByName('y').GetValues); % kilometers
rockZ = cell2mat(rockPosDP.DataSets.GetDataSetByName('z').GetValues);
rockVX = cell2mat(rockVelDP.DataSets.GetDataSetByName('x').GetValues);
rockVY = cell2mat(rockVelDP.DataSets.GetDataSetByName('y').GetValues);
rockVZ = cell2mat(rockVelDP.DataSets.GetDataSetByName('z').GetValues);

%adding output to vars
vars.objects.vehicles.icarus.object = rocket;
vars.objects.vehicles.icarus.rockPosDP = rockPosDP;
vars.objects.vehicles.icarus.rockVelDP = rockVelDP;
vars.objects.vehicles.icarus.rockTime = rockTime;
vars.objects.vehicles.icarus.rockX = rockX;
vars.objects.vehicles.icarus.rockY = rockY;
vars.objects.vehicles.icarus.rockZ = rockZ;
vars.objects.vehicles.icarus.rockVX = rockVX;
vars.objects.vehicles.icarus.rockVY = rockVY;
vars.objects.vehicles.icarus.rockVZ = rockVZ;