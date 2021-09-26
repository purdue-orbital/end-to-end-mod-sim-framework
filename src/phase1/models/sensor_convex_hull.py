# program to find convex hull of a set of points using Jarvis' Algorithm.
#
# input: "points[]"
# the input of points[] is an array of class points "Point"
# hence, points[0].x corresponds to the first x-coordinate
# and points[0].y corresponds to the first y-cooridnate
#
# output: "sensor_hull.pattern"

# the smallest value on the x-axis is referred to as "leftmost"

import math

# point class with x, y as point
class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

# left_index function finds the leftmost point in "points"
def left_index(points):
	
	min = 0
	for i in range(1, len(points)):
		if points[i].x < points[min].x:
			min = i
		elif points[i].x == points[min].x:
			if points[i].y > points[min].y:
				min = i
	return min

# orientation function finds orentation of an ordered triplet (p, q, r)
# if the points are collinear, a 0 is returned.
# if the point triplet is clockwise for any other point r, a 1 is returned
# if the point triplet is counterclockwise for any other point r, a 2 is returned
def orientation(p, q, r):

    # val is derived from the slope of the line segments connecting p to q and q to r
	val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

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
def convex_hull(points, n, ref_dis):
     
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
    f = open('sensor_hull.pattern','w')

    f.write('stk.v.12.2\nReferenceDistance ' + str(ref_dis) + '\nNumberPoints ' + str(len(hull) + 1) + '\nPatternData\n')

    for i in hull:
        f.write(str(polar_conversion(points[i].x, points[i].y)[0]) + ' ' + str(polar_conversion(points[i].x, points[i].y)[1]) + '\n')

    f.write(str(polar_conversion(points[hull[0]].x, points[hull[0]].y)[0]) + ' ' + str(polar_conversion(points[hull[0]].x, points[hull[0]].y)[1]) + '\n')

    f.write('EndPatternData')
    f.close

# input points[]
points = []

# test points
'''
points.append(Point(26, 21))
points.append(Point(-86, 49))
points.append(Point(-95, 91))
points.append(Point(-6, -19))
points.append(Point(64, -77))
points.append(Point(-81, -61))
points.append(Point(65, -1))
points.append(Point(29, 1))
points.append(Point(9, -100))
points.append(Point(-14, -11))
points.append(Point(-89, 51))
points.append(Point(-96, -85))
points.append(Point(50, -53))
points.append(Point(34, -38))
points.append(Point(-67, 97))
points.append(Point(47, 39))
points.append(Point(-99, -74))
points.append(Point(-42, 23))
points.append(Point(41, 98))
points.append(Point(-30, -43))
'''

# reference distance
ref_dis = 20

convex_hull(points, len(points), ref_dis)

# STK sesnor pattern reference: https://help.agi.com/stk/#stk/sncustom-01.htm?Highlight=reference%20sensor
# jarvis algorithm reference: https://www.geeksforgeeks.org/convex-hull-set-1-jarviss-algorithm-or-wrapping/