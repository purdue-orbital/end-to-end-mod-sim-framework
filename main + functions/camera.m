function [vars] = camera(vars)
fprintf('...Creating Camera\n');
SatCam = vars.stkInterface.root.CurrentScenario.Children.New('eSatellite', vars.objects.vehicles.camera.name); 
model = SatCam.VO.model;
model.Visible = false;
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera DeleteSegment Propagate');
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera DeleteSegment Initial_State');

%creating the follow segments for astrogator
for i = 1:3
    vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera InsertSegment MainSequence.SegmentList.- Follow');
end

vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.Follow.ComponentName FollowBalloon');
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.Follow1.ComponentName FollowIcarus');
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.Follow2.ComponentName FollowCubeSat');


%Setting the leaders of the follow segments
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.FollowBalloon.Leader Balloon');
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.FollowIcarus.Leader Icarus');
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.FollowCubeSat.Leader CubeSat');

%Setting the offset so the camera doesn't start in the ground
unformatedOffsetCommand = 'Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.FollowBalloon.Zoffset -%d m';
OffsetCommand = sprintf(unformatedOffsetCommand, vars.objects.vehicles.camera.modelOffset);
vars.stkInterface.root.ExecuteCommand(OffsetCommand);

%Specifiying joining and seperation conditions
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.FollowBalloon.JoiningType "Join at Beginning of Leader''s Ephemeris"');
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.FollowBalloon.SeparationType "Separate at End of Leader''s Ephemeris"');
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.FollowIcarus.JoiningType "Join at Beginning of Leader''s Ephemeris"');
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.FollowIcarus.SeparationType "Separate at End of Leader''s Ephemeris"');
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera SetValue MainSequence.SegmentList.FollowCubeSat.JoiningType "Join at Beginning of Leader''s Ephemeris"');

%running mcs
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera RunMCS');

%clearing graphics
vars.stkInterface.root.ExecuteCommand('Astrogator */Satellite/Camera ClearDWCGraphics');
vars.stkInterface.root.ExecuteCommand('VO */Satellite/Camera Pass3D OrbitLead None');
vars.stkInterface.root.ExecuteCommand('VO */Satellite/Camera Pass3D OrbitTrail None');
vars.stkInterface.root.ExecuteCommand('Graphics */Satellite/Camera Show off');

%adding outputs to vars
vars.objects.vehicles.camera.object = SatCam;
