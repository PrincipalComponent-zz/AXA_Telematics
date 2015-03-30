import csv
import os
import sys


import numpy as np
#import matplotlib.pyplot as plt

from vector_math import *





class Path:

   def __init__(self, driverid, routeid):
      self.driverid = driverid
      self.routeid  = routeid
      self.route        = []
      self.distance     = 0    # start with traveling zero distance
      self.time         = 0    # start with traveling for zero time

      self.feature_loc  = []
      self.angles       = []
      
      self.comparison   = []
      
      self.matched      = 0   # default to not being matched

      self.is_zero      = 0  # if it is a zero distance route   
      
      self.print_flag   = 0
      
   
   #********************
   # This gets the distance traveled along a route   
   #********************
   def get_route_distance(self, start_id, end_id):
   
      total_distance = 0
   
      for cnt in range( start_id+1, end_id):
         x1 = self.route[ cnt-1, 0]
         y1 = self.route[ cnt-1, 1]

         x2 = self.route[ cnt, 0]
         y2 = self.route[ cnt, 1]   
   
         distance1 = get_distance(x1, y1, x2, y2)
         total_distance += distance1
         
      return total_distance
   #********************
   # This gets the distance traveled along a route   
   #********************   
   
   

   #********************
   #**** this function rotates the N x 2  path by a 2x2 rotation matrix
   #********************
   def rotate_path( self, angle_to_rotate):
   
      rotation_matrix = [   [ np.cos(angle_to_rotate), -1 * np.sin(angle_to_rotate) ], 
                            [ np.sin(angle_to_rotate),      np.cos(angle_to_rotate) ]  ]
      
      self.route = np.dot( self.route, rotation_matrix)
      return 
   #********************
   #**** end function rotates the N x 2  path by a 2x2 rotation matrix
   #********************






   #********************
   #**** this function finds the higest point and centers the grap on it
   #********************
   def center_on_highest_point(self):
   
      # find where the tallest point is at
      max_height = -1
      max_x      = -1
      max_index = 0
      for cnt, coords in enumerate(self.route):
          if abs(coords[1] > max_height):
              max_height = abs(coords[1])
              max_index = cnt





      #if ( max_index > self.time/2.5):  # see if we are past halfway, if we are, flip in x
      #   self.flip_x_coords()

      max_index = max( 1,  min( max_index, self.time-2) )
      
      # center on that maximum value
      x_coord =  self.route[max_index,0]
      y_coord =  self.route[max_index,1]
      index_array = np.array([x_coord, y_coord])
      self.route = np.subtract(self.route, index_array)
      
      # see how far away the start and end points are
      dist_from_start = get_distance(x_coord, y_coord, self.route[0,0], self.route[0,1])
      dist_from_end = get_distance(x_coord, y_coord, self.route[-1,0], self.route[-1,1])
    
      # the farther away from the end points we are, the greater arm to center the angle on
      if (dist_from_start > 2500 and dist_from_end > 2500):  
         centering_distance = 1000
      elif (dist_from_start > 1500 and dist_from_end > 1500):
         centering_distance = 500
      elif (dist_from_start > 1000 and dist_from_end > 1000):
         centering_distance = 250
      elif (dist_from_start > 500 and dist_from_end > 500):
         centering_distance = 150
      elif (dist_from_start > 150 and dist_from_end > 150):
         centering_distance = 50
      else :
         centering_distance = 25
    
      loc_ahead  = find_closest_point_at_minimum_distance(self.route,max_index,centering_distance,1.0)
      loc_behind = find_closest_point_at_minimum_distance(self.route,max_index,centering_distance,-1.0)
      
      #print(max_index, loc_ahead, loc_behind)
      
      
      # get the angle between these vectors
      x0 =  self.route[loc_behind,0]
      y0 =  self.route[loc_behind,1]
      
      x1 =  self.route[max_index,0]
      y1 =  self.route[max_index,1]
      
      x2 =  self.route[loc_ahead,0]
      y2 =  self.route[loc_ahead,1]
      
      # get the vector
      v1 = [ x1-x0, y1-y0]
      v2 = [ x1-x2, y1-y2]
      v3 = [ 0, 1]
      
      
      angle1 = angle_between(v1, v2)   # the angle of the angle
      angle2 = angle_between(v3, v2)   # the angle of the vector ahead vs vertical
      
      #print("the angle is ",angle1, angle1 * 180 / np.pi)
      #print("the angle is ",angle2, angle2 * 180 / np.pi)
      
      target_angle = angle1 / 2.0  # we want the vertical to bisect our angle
      angle_diff =  -1 * (target_angle - angle2)
      
      self.rotate_path( angle_diff)  # rotate our path to bisect
       
      return 
   #********************
   #**** end function finds the higest point and centers the grap on it
   #********************




   #********************
   #**** this function flips the y coordinates
   #********************
   def flip_y_coords(self):
      flip_y = [1, -1]
      self.route = np.multiply( self.route, flip_y)
      return
   #********************
   #**** end function flips the y coordinates
   #********************

   #********************
   #**** this function flips the x coordinates
   #********************
   def flip_x_coords(self):
      flip_x = [-1, 1]
      self.route = np.multiply( self.route, flip_x)
      return
   #********************
   #**** end function flips the y coordinates
   #********************

   
   
   
   #**********************
   #*** this gets our list of features using an RDP sort
   #**********************
   def generate_features(self, rdp_tolerance):
   
      tolerance = rdp_tolerance
      simplified = np.array(rdp( self.route.tolist(), tolerance ))
      simplified_loc = match_RDP_to_route( simplified, self.route)
      features = []
      for cnt, item in enumerate(simplified_loc):
         features.append( [ simplified[cnt,0], simplified[cnt,1], item ] )
      self.feature_loc = np.array(features)

      return
   #**********************
   #*** this gets our list of features
   #**********************   






   
   
   #**********************
   #*** this gets our list of features using an RDP sort
   #**********************
   def update_feature_loc(self):
   
      current_loc = self.feature_loc[:,2]

      features = []
      for cnt, item in enumerate(current_loc):
         features.append( [ self.route[item,0], self.route[item,1], item ] )
      self.feature_loc = np.array(features)

      return
   #**********************
   #*** this gets our list of features
   #**********************      
   
   
   

   #**********************
   #*** this calculates angles and distances of the legs of the triangle that will be used for comparison
   #**********************
   def generate_angles(self):
   
      
      for cnt in  range(1, len(self.feature_loc) -1):  # get the angle between consecutive points
         x1 = self.feature_loc[cnt-1,0]
         y1 = self.feature_loc[cnt-1,1]

         x2 = self.feature_loc[cnt,0]
         y2 = self.feature_loc[cnt,1]
         
         x3 = self.feature_loc[cnt+1,0]
         y3 = self.feature_loc[cnt+1,1]         

         angle1, distance1, distance2 = get_angle_between_3_points(x1,y1,x2,y2,x3,y3)
  
         if (distance1> distance2):
            angle_info = [angle1, distance1,  distance2, cnt-1, cnt, cnt+1, len(self.angles)]
         else:
            angle_info = [angle1, distance2,  distance1, cnt+1, cnt, cnt-1, len(self.angles)]

         self.angles.append(angle_info)



      for cnt in  range(1, len(self.feature_loc) -2):  # get the angle between consecutive points, skipping 1
         x1 = self.feature_loc[cnt-1,0]
         y1 = self.feature_loc[cnt-1,1]

         x2 = self.feature_loc[cnt,0]
         y2 = self.feature_loc[cnt,1]
         
         x3 = self.feature_loc[cnt+2,0]
         y3 = self.feature_loc[cnt+2,1]         

         angle1, distance1, distance2 = get_angle_between_3_points(x1,y1,x2,y2,x3,y3)
  
         if (distance1> distance2):
            angle_info = [angle1, distance1,  distance2, cnt-1, cnt, cnt+2, len(self.angles)]
         else:
            angle_info = [angle1, distance2,  distance1, cnt+2, cnt, cnt-1, len(self.angles)]

         self.angles.append(angle_info)



      for cnt in  range(1, len(self.feature_loc) -2):  # get the angle between consecutive points, skipping 1
         x1 = self.feature_loc[cnt-1,0]
         y1 = self.feature_loc[cnt-1,1]

         x2 = self.feature_loc[cnt+1,0]
         y2 = self.feature_loc[cnt+1,1]
         
         x3 = self.feature_loc[cnt+2,0]
         y3 = self.feature_loc[cnt+2,1]         

         angle1, distance1, distance2 = get_angle_between_3_points(x1,y1,x2,y2,x3,y3)
  
         if (distance1> distance2):
            angle_info = [angle1, distance1,  distance2, cnt-1, cnt+1, cnt+2, len(self.angles)]
         else:
            angle_info = [angle1, distance2,  distance1, cnt+2, cnt+1, cnt-1, len(self.angles)]

         self.angles.append(angle_info)


      
      self.angles = np.array(self.angles)

      if (len(self.angles) > 0):
          self.angles = self.angles[ self.angles[:,0].argsort() ]  # sort from smallest angle to biggest angle
          
          for cnt in xrange(0,len(self.angles)):    # remember where this is in the array
             self.angles[cnt,6] = cnt     
      

      return   
   #**********************
   #*** this calculates angles and distances of the legs of the triangle that will be used for comparison
   #**********************   