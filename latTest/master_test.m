clear
clc
launchLats = linspace(28,50,46);
icarusDV = linspace(7,8,22);
defaultLats = [28.6084 25.051];    %launch, burnout
defaultLons = [-80.6042 -51.326];    %launch, burnout
distance = stdist(defaultLats, defaultLons);    %average standard distance along Earth's surface
cubeSatMass = 2;    %kg
deorbitTime = [];
areaMassRatio = .1*.1/cubeSatMass;    %m^2/kg
for i = 1:1:length(icarusDV)
    fprintf('For a delta V of %.4d m/s:\n', icarusDV(i) * 1000);
    [deorbitTimeArray, burnoutV, stkInterface] = distanceTest(icarusDV(i), launchLats, distance, cubeSatMass, areaMassRatio, i);
    deorbitTime = [deorbitTime; deorbitTimeArray];
end

deorbitTime = (deorbitTime./60)./95;
launchLatsFlipped = flip(launchLats);
icarusDVFlipped = flip(icarusDV);
fprintf('Test Complete!\n');
deorbitTimeFlipped = fliplr(deorbitTime);

figure()
imagesc(launchLatsFlipped, icarusDVFlipped, deorbitTimeFlipped)
xlabel('Launch Latitude')
ylabel('Icarus Delta V (km/s)')
a = colorbar;
ylabel(a, 'Number of Orbits')
colormap bone
yt = get(gca, 'YTick');
set(gca, 'YTickLabel',flip(yt))
title('Icarus Delta V and Launch Latitude vs Number of Orbits')

array = [];

for j = 3:2:46    %NOTE! ONLY WORKS FOR launchLats = linspace(28,50,46); fix later to work for all ranges
   for k = 1:1:22
       if deorbitTime(k, j) > 5
            array = [array k-1];
            break;
       end
   end
end
array = 7 + (array * (icarusDV(2)-icarusDV(1)));
increases = [];
for l = 2:1:length(array)
    increase = 100* (array(l) - array(l-1))/array(1);
    increases = [increases increase];
end
averageIncrease = mean(increases);