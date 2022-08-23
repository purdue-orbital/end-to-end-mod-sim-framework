launchLats = [28 28.5 29 29.5 30 30.5];
earthRotationV = .46388;
deltaV = [(7+(.46388*cos(28))) (7.05 + (.46388*cos(28.5))) (7.1 + (.46388*cos(29))) (7.15 + (.46388*cos(29.5))) (7.2 + (.46388*cos(30))) (7.25 + (.46388*cos(30.5)))];
burnout.alt = 150;
launch.lon = -100;
launch.alt = 22.2201;

defaultLats = [28.6084 25.051];    %launch, burnout
defaultLons = [-80.6042 -51.326];    %launch, burnout
distance = stdist(defaultLats, defaultLons);    %average standard distance along Earth's surface

[stkInterface] = testSetup();
burnoutLats = [];
iteration = 1;
for i = 1:1:length(launchLats)
   burnout.lat = launchLats(i);    %we're going along the line of latitude
   launch.lat = launchLats(i);
   burnout.V = deltaV(i);
   newDistance = -1;
   burnout.lon = -100;
   while abs(newDistance - distance) > .01
       burnout.lon = burnout.lon + .001;
       newDistance = stdist([launch.lat burnout.lat], [launch.lon, burnout.lon]);
   end
   
 testRocket(stkInterface, launch, burnout, iteration);
 iteration = iteration + 1;
 
end
