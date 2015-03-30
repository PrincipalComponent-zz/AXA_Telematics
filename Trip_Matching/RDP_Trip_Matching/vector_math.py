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
#*** RDP Calculation to generate the turning points from a list of points
#***   Ramer-Douglas-Peucker based on http://en.wikipedia.org/wiki/Ramer-Douglas-Peucker_algorithm
#***************

def distance(point1, point2):
    distance1 =  sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return  distance1

def shortest_distance_to_segment(point1, line_start, line_end):
    if (line_start == line_end):
        return distance(point1, line_start)
    else:
        d1 = abs( (line_start[1] - point1[1]) * (line_end[0] - line_start[0])   - (line_end[1] - line_start[1])  * (line_start[0] - point1[0])   )
        line_distance = sqrt( (line_end[0] - line_start[0]) ** 2 + (line_end[1] - line_start[1]) ** 2  )
        return d1 / line_distance
        
        
# Change a list of points to find the turning points in the series by looking for any point 
# that is more than a certain distance from a straight line between other RDP poitns
def rdp(point_list, epsilon):

    dist_max = 0.0
    index1 = 0
    for i in range(1, len(point_list) - 1):
        dist1 = shortest_distance_to_segment(point_list[i], point_list[0], point_list[-1])
        if dist1 > dist_max:
            index1 = i
            dist_max = dist1
    if dist_max >= epsilon:
        result_list = rdp(point_list[:index1+1], epsilon)[:-1] + rdp(point_list[index1:], epsilon)
    else:
        result_list = [point_list[0], point_list[-1]]
    return result_list







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