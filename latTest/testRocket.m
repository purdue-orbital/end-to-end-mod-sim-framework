function deorbitTime = testRocket(stkInterface, launch, burnout, iteration, cubeSatMass, areaMassRatio, z)

rocketName = 'TestRocket%d';
rocketName = sprintf(rocketName, iteration);

rocket = stkInterface.root.CurrentScenario.Children.New('eLaunchVehicle', rocketName);
rocket.Trajectory.InitialState.Launch.AssignGeodetic(launch.lat, launch.lon, launch.alt);
rocket.Trajectory.InitialState.Burnout.AssignGeodetic(burnout.lat, burnout.lon, burnout.alt);
rocket.Trajectory.InitialState.BurnoutVel = burnout.V;
xV.burnoutV = burnout.V;
rocket.Trajectory.Propagate;

xV.rockPosDP = rocket.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(stkInterface.scenario.StartTime, stkInterface.scenario.StopTime, 60); % seconds
xV.rockVelDP = rocket.DataProviders.Item('Cartesian Velocity').Group.Item('ICRF').Exec(stkInterface.scenario.StartTime, stkInterface.scenario.StopTime, 60);
xV.rockTime = cell2mat(xV.rockPosDP.DataSets.GetDataSetByName('Time').GetValues);
xV.rockX = cell2mat(xV.rockPosDP.DataSets.GetDataSetByName('x').GetValues); % seconds
xV.rockY = cell2mat(xV.rockPosDP.DataSets.GetDataSetByName('y').GetValues); % kilometers
xV.rockZ = cell2mat(xV.rockPosDP.DataSets.GetDataSetByName('z').GetValues);
xV.rockVX = cell2mat(xV.rockVelDP.DataSets.GetDataSetByName('x').GetValues);
xV.rockVY = cell2mat(xV.rockVelDP.DataSets.GetDataSetByName('y').GetValues);
xV.rockVZ = cell2mat(xV.rockVelDP.DataSets.GetDataSetByName('z').GetValues);

deorbitTime = testSat(stkInterface, xV, iteration, cubeSatMass, areaMassRatio);
