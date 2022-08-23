function [deorbitTime,burnoutV,stkInterface] = distanceTest(icarusDV, launchLats, distance, areaMassRatio, crossSecArea, z)
%lock delta v, vary latitude, find deorbit time, use default change in degrees from launch location to burnout location
%use the matlab stdist function to calculate the distance we need, and check points along the line of latitude we are on (east) 
%to find one with the same distance. That is our burnout lat/lon
stkInterface = testSetup();

deorbitTime = [];

earthRotationV = .46388;
% icarusDV = 7;

launch.lon = -100;    %goes through texas to cover as much of the us as possible
launch.alt = 22.2201;

burnout.alt = 150;    %km

iteration = 1;

burnoutV = [];

for i = 1:1:length(launchLats)
   launch.lat = launchLats(i);
   burnout.lat = launch.lat;    %we're going along the line of latitude
   
   earthRotationV = earthRotationV * cosd(launch.lat);
   burnout.V = earthRotationV + icarusDV;
   burnoutV(i) = burnout.V;
   newDistance = -1;
   burnout.lon = -100;
   while abs(newDistance - distance) > .1
       burnout.lon = burnout.lon + .01;
       newDistance = stdist([launch.lat burnout.lat], [launch.lon, burnout.lon]);
   end
 
 deorbitTime(iteration) = testRocket(stkInterface, launch, burnout, iteration, areaMassRatio, crossSecArea, z);
 fprintf('Test at a Latitude of %d Degrees North complete!\n', launchLats(i)); 
 iteration = iteration + 1;  
  
end

% figure()
% deorbitTime = deorbitTime./3600;
% plot(launchLats, deorbitTime)
% title('Rocket Launch Latitude vs Time Until Re-entry')
% xlabel('Rocket Launch Latitude (Degrees North')
% ylabel('Time Until Re-entry (Hours)')
% grid on