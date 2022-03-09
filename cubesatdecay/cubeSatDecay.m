function [vars, burnAltArr, eccArr, satDecay, burnVelArr] = cubeSatDecay(vars, burnAmin, burnAmax, burnAspace, eccMin, eccMax, eccSpace, maxTime)
% Plot time for CubeSat to decay as a function of Icarus burn velocity

fprintf('\n...Decaying %d CubeSats\n', burnAspace * eccSpace);
rocket = vars.objects.vehicles.icarus.object;
satellite = vars.objects.vehicles.satellite.object;
mu = 398600.4;
burnAltArr = linspace(burnAmin, burnAmax, burnAspace);
eccArr = linspace(eccMin, eccMax, eccSpace);
satDecay = zeros(burnAspace, eccSpace);
burnVelArr = satDecay;
decayNum = 1;

i = 1;
for indA = 1:burnAspace
    burnA = burnAltArr(indA);
    
    k = 1;
    for indE = 1:eccSpace
        ecc = eccArr(indE);
        
        %pause(.5);
        rocket.Trajectory.InitialState.Burnout.AssignGeodetic(28.2411, 80.5508, burnA);
        %burnV = sqrt((mu * (1 - ecc^2)) / (6378 + burnA)^2);
        burnV = sqrt(((2 * mu) / (6378 + burnA)) - (mu / ((6378 + burnA) / (1 - ecc))));
        burnVelArr(k, i) = burnV;
        rocket.Trajectory.InitialState.BurnoutVel = burnV;
        rockPock = rocket.Vgt.Events.Factory.CreateSmartEpochFromTime(vars.objects.vehicles.balloon.airTime(end));
        rocket.Trajectory.EphemerisInterval.SetStartEpochAndDuration(rockPock, "+10 minutes");
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
        
        satPock = satellite.Vgt.Events.Factory.CreateSmartEpochFromTime(rockTime(end));
        satellite.Propagator.EphemerisInterval.SetStartEpochAndDuration(satPock, '+14 days');
        satellite.Propagator.InitialState.OrbitEpoch.SetExplicitTime(rockTime(end))
        satellite.Propagator.InitialState.Representation.AssignCartesian('eCoordinateSystemICRF', rockX(end), rockY(end), rockZ(end), rockVX(end), rockVY(end), rockVZ(end));
        try
            satellite.Propagator.Propagate;
        catch
            fprintf("");
        end
        satPosDP = satellite.DataProviders.Item('Cartesian Position').Group.Item('ICRF').Exec(vars.stkInterface.scenario.StartTime, vars.stkInterface.scenario.StopTime, 60); % seconds
        satTime = cell2mat(satPosDP.DataSets.GetDataSetByName('Time').GetValues); % seconds
%         satX = cell2mat(satPosDP.DataSets.GetDataSetByName('x').GetValues);
%         satY = cell2mat(satPosDP.DataSets.GetDataSetByName('y').GetValues);
%         satZ = cell2mat(satPosDP.DataSets.GetDataSetByName('z').GetValues);
%         
%         for j = 1:numel(satTime)
%             satAlt = sqrt(satX(j)^2 + satY(j)^2 + satZ(j)^2) - 6378;
%             if satAlt <= 100
%                 if satTime(j) > 0
%                     satDecay(k, i) = satTime(j);
%                 else
%                     satDecay(k, i) = NaN;
%                 end
%                 fprintf('...(%d / %d) CubeSat decayed in %.2f days\n', decayNum, burnAspace * eccSpace, satTime(j) / (60 * 60 * 24));
%                 break;
%             else
%                 satDecay(k, i) = NaN;
%                 if j == numel(satTime)
%                     fprintf('...(%d / %d) CubeSat decay takes longer than scenario time\n', decayNum, burnAspace * eccSpace);
%                 end
%             end
%         end

        if satTime(end) < maxTime
            satDecay(k, i) = satTime(end);
            fprintf('...(%d / %d) CubeSat decayed in %.4f days\n', decayNum, burnAspace * eccSpace, satTime(end) / (60 * 60 * 24));
        else
            satDecay(k, i) = NaN;
            fprintf('...(%d / %d) CubeSat decay takes longer than scenario time\n', decayNum, burnAspace * eccSpace);
        end
        
        decayNum = decayNum + 1;
        k = k + 1;
        
    end
  i = i + 1;
  
end

end



