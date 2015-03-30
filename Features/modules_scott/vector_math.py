import numpy as np
from math import sqrt


#********************
#**** this function finds a point which is greater than the min distance
#********************
def find_closest_point_at_minimum_distance(path_array,starting_location,distance_required,pos_or_neg):

   x1 = path_array[starting_location,0]
   y1 = path_array[starting_location,1]

   if (pos_or_neg > 0):
      for loc1 in range(starting_location, len(path_array) ):
         min_loc = loc1
         x2 = path_array[loc1,0]
         y2 = path_array[loc1,1]
         
         distance1 = get_distance(x1,y1,x2,y2)
         if (distance1 > distance_required):   # see if the distance is close enough
            break

   else:
      for loc1 in range(starting_location, 0, -1 ):
         min_loc = loc1
         x2 = path_array[loc1,0]
         y2 = path_array[loc1,1]
         
         distance1 = get_distance(x1,y1,x2,y2)
         if (distance1 > distance_required):   # see if the distance is close enough
            break

   return min_loc
#********************
#**** this function finds a point which is greater than the min distance
#********************


#********************
#**** this function finds a point which is greater than the min distance
#********************
def get_distance( x1, y1, x2, y2):
   distance1 = ((x1 - x2)**2 + (y1 - y2)**2 ) ** (.5)
   return distance1


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    #return vector / np.linalg.norm(vector)
    return vector / ( vector[0]**2 + vector[1]**2) ** (.5)    

#@profile
def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    angle = np.arccos(np.dot(v1_u, v2_u))
    if np.isnan(angle):
        if (v1_u == v2_u).all():
            return 0.0
        else:
            return np.pi
    return angle



#**************
#*** Get the angle between 3 points
#***************
def get_angle_between_3_points(x1,y1,x2,y2,x3,y3):

   # get the vector
   v1 = [ x2-x1, y2-y1]
   v2 = [ x2-x3, y2-y3]      
   angle1 = angle_between(v1, v2) * 57.2957795130823   # the angle of the angle in degrees

   distance1 = get_distance( x1, y1, x2, y2)
   distance2 = get_distance( x2, y2, x3, y3)

   return  angle1, distance1, distance2
    





#********************
#**** this function rotates the N x 2  path by a 2x2 rotation matrix
#********************
def rotate_path( matrix1, angle_to_rotate):

   rotation_matrix = [   [ np.cos(angle_to_rotate), -1 * np.sin(angle_to_rotate) ], 
                         [ np.sin(angle_to_rotate),      np.cos(angle_to_rotate) ]  ]
   
   matrix1 = np.dot( matrix1, rotation_matrix)
   return matrix1 
#********************
#**** end function rotates the N x 2  path by a 2x2 rotation matrix
#********************




#********************
#**** this function flips the y coordinates
#********************
def flip_y_coords(matrix1):
   flip_y = [1, -1]
   matrix1 = np.multiply( matrix1, flip_y)
   return matrix1
#********************
#**** end function flips the y coordinates
#********************

#********************
#**** this function flips the x coordinates
#********************
def flip_x_coords(matrix1):
   flip_x = [-1, 1]
   matrix1 = np.multiply( matrix1, flip_x)
   return matrix1
#********************
#**** end function flips the y coordinates
#********************

   











    
    
    
#**************
#*** RDP Calculation for simplifying a series of points
#***************
"""
The Ramer-Douglas-Peucker algorithm roughly ported from the pseudo-code provided
by http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
"""
def distance(a, b):
    return  sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def point_line_distance(point, start, end):
    if (start == end):
        return distance(point, start)
    else:
        n = abs(
            (end[0] - start[0]) * (start[1] - point[1]) - (start[0] - point[0]) * (end[1] - start[1])
        )
        d = sqrt(
            (end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2
        )
        return n / d

def rdp(points, epsilon):
    """
    Reduces a series of points to a simplified version that loses detail, but
    maintains the general shape of the series.
    """
    dmax = 0.0
    index = 0
    for i in range(1, len(points) - 1):
        d = point_line_distance(points[i], points[0], points[-1])
        if d > dmax:
            index = i
            dmax = d
    if dmax >= epsilon:
        results = rdp(points[:index+1], epsilon)[:-1] + rdp(points[index:], epsilon)
    else:
        results = [points[0], points[-1]]
    return results



def rdp_recursion(points, epsilon,route):
    # as long as there are more than 4 RDP points, step inward 1 point at a time and call it recursively to 
    # try to get the RDP points to line up closer
    
    results = rdp(points, epsilon)
    results_array = np.array(results)
    RDP_index = match_RDP_to_route( results_array, route)
    

    results_hold = []
    point_segment = points
    route_segment = route
    cnt = 0
    
    while(len(results) >= 4):   # while we have at least 4 RDP points in this segment then iterate
       results_hold.insert(cnt,  results[0])      # save the first and last RDP points
       results_hold.insert(cnt+1, results[-1])
       cnt+=1
       
       # generate a route segment starting at the second RDP point and ending at the second to last one
       point_segment = point_segment[ RDP_index[1]: RDP_index[-2]+1]   
       route_segment = route_segment[ RDP_index[1]: RDP_index[-2]+1, :]
       
       results = rdp(point_segment, epsilon)
       results_array = np.array(results)
       RDP_index = match_RDP_to_route( results_array, route_segment)       
    
    
    if (len(results) == 2):
       results_hold.insert(cnt,  results[0])      # save the first and last RDP points
       results_hold.insert(cnt+1, results[-1])
       cnt+=1
    elif (len(results) ==3):                      # save all the RDP Points   
       results_hold.insert(cnt,  results[0])      # save the first and last RDP points
       results_hold.insert(cnt+1,  results[1])      # save the first and last RDP points
       results_hold.insert(cnt+2, results[-1])
       cnt+=1

    return results_hold





def match_RDP_to_route(RDP_points, route):

    match_loc = []
    cnt = 0
    for point_cnt in range(0, len(RDP_points) ):

        #print (RDP_points[point_cnt,0], RDP_points[point_cnt,1] )

        match_found = 0
        while( match_found ==0):
           if( RDP_points[point_cnt,0] == route[cnt,0]  and RDP_points[point_cnt,1] == route[cnt,1] ):  # see if the simp
              match_loc.append(cnt)
              match_found = 1
           cnt=cnt+1

    return match_loc




#**************
#***End RDP Calculation for simplifying a series of points
#***************    