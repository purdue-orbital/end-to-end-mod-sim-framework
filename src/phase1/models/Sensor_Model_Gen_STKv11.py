# In[]
import os
import math
import random
import numpy as np
from numpy.linalg import svd
from random import randrange

# position class
class Point:
    def __init__(self, pos, t):     
        self.pos = pos # [x, y, z]
        self.t = t # time

# position on the plane at time_int class
class PointPlane:
    def __init__(self, pos):     
        self.pos = pos # [x, y, z]

#input
points = [] # balloon position coordinates

# test points
points.append(Point([4, 5, 9], 1))
points.append(Point([9, 8, 9], 1))
points.append(Point([4, 3, 9], 1))
points.append(Point([8, 0, 9], 1))
points.append(Point([1, 7, 9], 1))
points.append(Point([1, 6, 10], 1))
points.append(Point([4, 5, 12], 2))
points.append(Point([9, 8, 12], 2))
points.append(Point([4, 3, 12], 2))
points.append(Point([8, 0, 12], 2))
points.append(Point([0, 7, 12], 2))
points.append(Point([-7, 7, 13], 2))
points.append(Point([-2, -2, 16], 3))
points.append(Point([9, 8, 16], 3))
points.append(Point([3, 5, 16], 3))
points.append(Point([-6, 3, 16], 3))
points.append(Point([3, 7, 16], 3))
points.append(Point([0, 8, 17], 3))

# plane_fit function returns the point cloud center and the normal vector [point, n_vector] to the plane given an array of points at time_int
def plane_fit(points_og, time_int):

    # conversion for function acceptance of points in class Points
    points_curt = [] # [points[i]...]
    x = []
    y = []
    z = []
    #r = 0
    t = 0
    for i in range(0, len(points_og)):
        #print('time_int: ' + str(time_int))
        if points_og[i].t == time_int:
            points_curt.append(points_og[i])
            if len(points_curt) == 1:
                t = 0
            else:
                t = t + 1

            #for l in range(0, len(points_curt)):
            #    print(str(points_curt[l].pos) + ' ' + str(points_curt[l].t) + ', ')
            #print('place in points_og: ' + str(i))
            #print('if iteration: ' + str(r))
            #print('t: ' + str(t))
            #r = r + 1

            x.append(points_curt[t].pos[0])
            y.append(points_curt[t].pos[1])
            z.append(points_curt[t].pos[2])
    
    points = []
    points.append(x)
    points.append(y)
    points.append(z)

    # reshapes points to single plane and calculates center coordinate and normal vector to the plane fit
    points = np.reshape(points, (np.shape(points)[0], -1)) # collapse trialing dimensions
    ctr = points.mean(axis=1)
    x = points - ctr[:,np.newaxis]
    M = np.dot(x, x.T)
    return ctr, svd(M)[0][:,-1]

# sensor_pointer writes a .sp file which points the sensor at a specific azimuth and elevation
def sensor_pointer(n, point_num, time_max, time_int):

    x = n[0]
    y = n[1]
    z = n[2]

    # what is the angle of azimuth U from the x-axis towards the y-axis
    #if x > 0:
    #    U = np.deg2rad(np.arctan(y/x))
    #elif x < 0 and y > 0:
    #    U = np.deg2rad(np.arctan(y/x)) + 180
    #elif x < 0 and y < 0:
    #    U = np.deg2rad(np.arctan(y/x)) - 180
    #elif x == 0 and y > 0:
    #    U = 90
    #else:
    #    U = -90
    U = np.rad2deg(np.arctan(x / y))

    # what is the angle of elevation V
    #if z > 0:
    #    V = 90 - np.deg2rad(np.arctan(np.sqrt(x**2 + y**2)/z))
    #else:
    #    V = 0
    if z > 0:
        V = 90 + np.rad2deg(np.arctan(y / z))
    else:
        V = 0

    # write angles to STK sensor pointing file
    f = open('sensorpointer_' + str(point_num) + '.sp','w')

    f.write('stk.v.3.0\nBegin Attitude\nNumberofAttitudePoints ' + str(int(time_max + 1 - time_int)) + '\nSequence 323\nAttitudeTimeAzElAngles\n')

    for i in range(int(time_int), int(time_max) + 1):
        #print(i)
        f.write(str(i) + ' ' + str(U)+ ' ' + str(V) + '\n')

    f.write('End Attitude')
    f.close

# frame_conv function converts a 3d point to a 2d point relative to the plane at time_int
def frame_conv(points, time_int):

    p = plane_fit(points, time_int)[0]

    points_curt = [] # [points[i]...] only at time_int
    for i in range(0, len(points)):
        if points[i].t == time_int:
            points_curt.append(points[i])

    # reference coordinates
    num = len(points_curt)
    if num != 0:
        #print('k: ' + str(num))
        i = random.randrange(num)
        j = random.randrange(num)
        while j == i:
            j = random.randrange(num)

        #print('random i: ' + str(i))
        #print('random j: ' + str(j))

    # 3d to 2d conversion
    points_curt_2d = []
    for k in range(0, len(points_curt)):
        u = [points_curt[i].pos[0], points_curt[i].pos[1], points_curt[i].pos[2]] - p
        v = [points_curt[j].pos[0], points_curt[j].pos[1], points_curt[j].pos[2]] - p
        u /= np.linalg.norm(u)
        v /= np.linalg.norm(v)
        w = np.cross(u, v)
        u = np.cross(v, w)

        # 2d coordinates relative to plane with origin p
        q = [np.dot(u, [points_curt[k].pos[0], points_curt[k].pos[1], points_curt[k].pos[2]] - p), np.dot(v, [points_curt[k].pos[0], points_curt[k].pos[1], points_curt[k].pos[2]] - p)]
        points_curt_2d.append(q)

    return(points_curt_2d)

# left_index function finds the leftmost point in "points"
def left_index(points):
	
	min = 0
	for i in range(1, len(points)):
		if points[i].pos[0] < points[min].pos[0]:
			min = i
		elif points[i].pos[0] == points[min].pos[0]:
			if points[i].pos[1] > points[min].pos[1]:
				min = i
	return min

# orientation function finds orentation of an ordered triplet (p, q, r)
# if the points are collinear, a 0 is returned.
# if the point triplet is clockwise for any other point r, a 1 is returned
# if the point triplet is counterclockwise for any other point r, a 2 is returned
def orientation(p, q, r):

    # val is derived from the slope of the line segments connecting p to q and q to r
	val = (q.pos[1] - p.pos[1]) * (r.pos[0] - q.pos[0]) - (q.pos[0] - p.pos[0]) * (r.pos[1] - q.pos[1])

	if val == 0:
		return 0
	elif val > 0:
		return 1
	else:
		return 2

# polar_conversion function converts cartesian coordinates into
# polar coordinates for use in STK
def polar_conversion(x, y):

    pol = []

    radius = math.sqrt(x * x + y * y)

    if x > 0:
        theta = math.atan(y/x)
    elif x < 0:
        theta = math.atan(y/x) + math.pi
    else:
        theta = math.pi/2

    theta = 180 * theta/math.pi

    # append the radius and theta in degrees to a 2 x 1 array
    pol.append(radius)
    pol.append(theta)

    return pol

# convex_hull function starts from the leftmost point and moves counterclockwise,
# using orientation function, until the start point p is reached again
# the loop will run equal to the number of points in resulting hull
def convex_hull(points, n, ref_dis, pat_num):
     
    # there must be at least 3 points
    if n < 3:
        return
 
    # find the leftmost point
    left = left_index(points)
 
    # the exterior shape of the input object
    hull = []
     
    p = left
    q = 0

    while(True):
         
        # append current point to hull[]
        hull.append(p)
 
        # as a new point i is more counterclockwise than previous point q
        # then q is updated
        q = (p + 1) % n
 
        for i in range(n):
             
            # If i is more counterclockwise
            # than current q, then update q
            if(orientation(points[p],
                           points[i], points[q]) == 2):
                q = i
 
        # q is now the most counterclockwise point with respect to p
        # append q to hull
        # update as q for the next iteration
        p = q
 
        # maintains that we have not reached the leftmost point again
        if(p == left):
            break
 
    # write covex hull points to STK pattern file
    f = open('sensorpattern_' + str(pat_num) + '.Pattern','w')

    f.write('stk.v.3.0\nReferenceDistance ' + str(ref_dis) + '\nNumberPoints ' + str(len(hull) + 1) + '\nPatternData\n')

    for i in hull:
        f.write(str(polar_conversion(points[i].pos[0], points[i].pos[1])[0]) + ' ' + str(polar_conversion(points[i].pos[0], points[i].pos[1])[1]) + '\n')

    f.write(str(polar_conversion(points[hull[0]].pos[0], points[hull[0]].pos[1])[0]) + ' ' + str(polar_conversion(points[hull[0]].pos[0], points[hull[0]].pos[1])[1]) + '\n')

    f.write('EndPatternData')
    f.close

# Main Function

x = int(input('Would you like to generate files related to height (0), time (2), or both (1)?\n'))

if x <= 1:

    os.chdir(r'H:\Orbital\STK_Height_Files')
    ref_dis = 1
    pat_num = 1
    ref_dis = 0
    max_height = float(input('For the patterns related to height, enter the maximum height:\n'))

    while ref_dis <= max_height:

        temp = []

        for i in range(0, len(points)):

            if points[i].pos[2] == ref_dis:

                temp.append(points[i])

        if len(temp) != 0:

            convex_hull(temp, len(temp), ref_dis, pat_num)
            pat_num += 1

        ref_dis += 1

    f = open('README.txt','w')
    f.write('Move these files, not the folder itself, to the following directory:\nnas01.itap.purdue.edu\puhome\My Documents\STK 11 (x64)')

if x >= 1:

    os.chdir(r'H:\Orbital\STK_Time_Files')
    ref_dis = 1
    pat_num = 1
    time_int = 0
    time_step = 1
    time_max = float(input('For the patterns and pointers related to time, enter the stopping time:\n'))

    while time_int <= time_max:

        temp = frame_conv(points, time_int)
        points_plane = []

        for i in range(0, len(temp)):

            points_plane.append(PointPlane([temp[i][0], temp[i][1], 0]))

        p, n = plane_fit(points, time_int)
        ref_dis = (p[0]**2 + p[1]**2 + p[2]**2)**.5

        if len(points_plane) != 0:

            convex_hull(points_plane, len(points_plane), ref_dis, pat_num)
            sensor_pointer(n, pat_num, time_max, time_int)
            pat_num += 1

        time_int += time_step

    f = open('README.txt','w')
    f.write('Move these files, not the folder itself, to the following directory:\nnas01.itap.purdue.edu\puhome\My Documents\STK 11 (x64)')

print('...Finished!')

# %%
