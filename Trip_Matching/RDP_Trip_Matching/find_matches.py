import csv
import os
import sys
import time

import numpy as np
import matplotlib.pyplot as plt
#from sklearn.neighbors import NearestNeighbors

from path import Path
from vector_math import *
from find_matches import *
import search_matches




#********************
#**** this compares two sets of angles to see how close the two paths are
#********************   
#@profile
def compare_two_sets_of_angles(path1, path2):


    match_comparison = []
    max_distance = 0

    if len(path2.angles>0):
        angles2 = path2.angles[:,0]
        distances1_2 = path2.angles[:,1]
        distances2_2 = path2.angles[:,2]
        path2_angles = path2.angles[:,0:3]
        
        path2_angles_test = path2.angles[:,0:3].tolist()
        
    else:
        return  # if we don't have any angles then break out of the loop and go to the next path
    
    if len(path1.angles>0):
        path1_angles = path1.angles[:,0:3]
        path1_angles_test = path1.angles[:,0:3].tolist()
    else:
        return  # if we don't have any angles then break out of the loop and go to the next path 
    
    
    angle_tolerance = 4.2
    distance_tolerance = 18.0

    #cdef int cnt2

    matching_angles, num_matched = search_matches.match_angles(path1_angles, path2_angles, angle_tolerance, distance_tolerance)
    match_comparison = matching_angles[0:num_matched,:]

    ## path1 is being compared against path 2
    #for cnt in xrange (0, len(path1.angles)):
    #   angle1      = path1.angles[cnt,0]
    #   matches = np.where( (abs(path2_angles[:,0]-angle1) <= angle_tolerance)  &  (  abs(path2_angles[:,1]-path1_angles[cnt,1]) <=  16) &  ( abs(path2_angles[:,2]-path1_angles[cnt,2]) <=  16) )
    #   if (len(matches[0]) > 0):
    #       match_score = [1, cnt, matches[0][0], 1.0, angle1]     # remember this angle
    #       match_comparison.append(match_score)       
    #       
#
    ##while( path1_angles_test and path2_angles_test ):  # look for matches and pop from the list
    ##   if ( path1_angles_test[-1][0] >  path2_angles_test[-1][0] ):  # pop the highest angle
    ##       path1_angles_test.pop()
    ##   else:
    ##       path2_angles_test.pop()
    #
    #for cnt, match_check in enumerate(match_comparison):
    #   if ( abs(match_check[0]-matching_angles[cnt,0]) > .01   ):
    #      print("here 1",abs(match_check[0]-matching_angles[cnt,0]) )
    #      print(0,cnt, match_check[0], matching_angles[cnt,0])
    #      sys.exit(0)
    #   if ( match_check[1] != matching_angles[cnt,1] ):
    #      print(1,cnt, match_check[1], matching_angles[cnt,1])
    #      sys.exit(0)
    #   if ( match_check[2] != matching_angles[cnt,2] ):
    #      print(2, cnt, match_check[2], matching_angles[cnt,2])
    #      sys.exit(0)
    #   if ( match_check[3] != matching_angles[cnt,3] ):
    #      print(3, cnt, match_check[3], matching_angles[cnt,3])
    #      sys.exit(0)
    #   if ( abs(match_check[4] - matching_angles[cnt,4]) > .01 ):
    #      print(4, cnt, match_check[4], matching_angles[cnt,4])          
    #      sys.exit(0)
#
    #         
#

    exact_match_cnt = 0

    matched_points1 = []
    matched_points2 = []
    for cnt, match_score in enumerate(match_comparison):
       if (match_score[0] ==1):
          exact_match_cnt += 1
          loc1 = match_score[1]
          loc2 = match_score[2]
                      
          # remember all of the matching points
          matched_points1.append( match_score[1])
          matched_points2.append( match_score[2])
          
          
    match_found =0
    if ( exact_match_cnt >= 2   ):
       path1_matching = [path2.routeid, 1, loc1]
       for match_point in matched_points1:
          path1_matching.append(match_point)

       path2_matching = [path1.routeid, 1, loc2]
       for match_point in matched_points2:
          path2_matching.append(match_point)          

       path1_matching_angle_list = path1_matching[3:]
       path2_matching_angle_list = path2_matching[3:]


    if ( exact_match_cnt >= 3   ):  # we need at least 3 points to check for an exact match
       # loop through each of the angles that was a good match and see how many of the points line up
       match_found = 0
       for cnt, angle1 in enumerate(path1_matching_angle_list):
          angle2 = path2_matching_angle_list[cnt]
          if (match_found ==0):      
             
             
             #print
             #print
             #print
             
             match_found = align_and_score_two_paths(path1, path2, angle1, angle2, path1_matching_angle_list, path2_matching_angle_list )

             #path1, path2, match_found = align_and_score_two_paths(path1, path2, angle1, angle2, path1_matching_angle_list, path2_matching_angle_list )
             #print
             #print
             #print

             #if (match_found != match_found2):
             #   print("***************** no match*******************",match_found,match_found2)


       if (match_found == 1):      
          path1.comparison.append( path1_matching )  # remember that we matched and remember which RDP points had a good match
          path2.comparison.append( path2_matching )
          if (path1.matched<0):
              path1.matched=0
          if (path2.matched<0):
              path2.matched = 0
          path1.matched += 1
          path2.matched += 1    
          
          path1.print_flag = 1


    # if we don't have a match, check 2 points to see if we have anything resembling a match
    if ( (path1.matched < 0 or path2.matched < 0) and exact_match_cnt >=2):
    #if (match_found ==1):

        if (len(path1_matching_angle_list) < 5):
            pass

        # find the distances between each of these angles and see if we can get any matching pairs
        for cnt1 in range(0,len(path1_matching_angle_list)-1):
            for cnt2 in range(cnt1+1,len(path1_matching_angle_list)):
                angle_id_1_1 = path1_matching_angle_list[cnt1]
                angle_id_1_2 = path1_matching_angle_list[cnt2]

                angle_id_2_1 = path2_matching_angle_list[cnt1]
                angle_id_2_2 = path2_matching_angle_list[cnt2]

                distance1 = path1.angle_distances[angle_id_1_1, angle_id_1_2]
                distance2 = path2.angle_distances[angle_id_2_1, angle_id_2_2]

                #if( abs(distance1-distance2) < 30): # if these angles are the same distance, count it
                #   print ("here 1")

                if(distance1 != 0 and distance2 != 0 and abs(distance1-distance2) < 30): # if these angles are the same distance, count it
                    if (path1.matched < 0):
                        path1.matched = 0  # these could be a match, so move them off of the definitely not matched list
                    if (path2.matched < 0):
                        path2.matched = 0  # these could be match
    
    return
#********************
#**** end this compares two sets of angles to see how close the two paths are
#********************   



#**************************************************************************************
#***** this gets the x, y, location of an rdp point
#**************************************************************************************
def get_RDP_xy(path, RDP_point):

    #x = path.route[path.feature_loc[RDP_point,2], 0]
    #y = path.route[path.feature_loc[RDP_point,2], 1]
    
    # saves time to not assign them to another variable
    return path.route[path.feature_loc[RDP_point,2], 0],  path.route[path.feature_loc[RDP_point,2], 1]


# ****************************************************************************
#  This returns 3 RDP points for each angle
# ********************************************************************
def get_RDP_point_from_angle(path, angle_num):

   #path_rdp1 =  path.angles[angle_num, 3]  # the is the before point
   #path_rdp2 =  path.angles[angle_num, 4]  # center point
   #path_rdp3 =  path.angles[angle_num, 5]  # after point
   
   #return path_rdp1, path_rdp2, path_rdp3
    
    return  path.angles[angle_num, 3], path.angles[angle_num, 4], path.angles[angle_num, 5]



# ****************************************************************************
#  This returns 3 RDP points for each angle
# ********************************************************************
def get_one_RDP_point_from_angle(path, angle_num):

   #path_rdp1 =  path.angles[angle_num, 3]  # the is the before point
   #path_rdp2 =  path.angles[angle_num, 4]  # center point
   #path_rdp3 =  path.angles[angle_num, 5]  # after point
   
   #return path_rdp1, path_rdp2, path_rdp3
    
    return   path.angles[angle_num, 4]



#********************
#**** this aligns two paths and gives a score of that alignment
#********************  
#@profile
def align_and_score_two_paths(path1, path2, angle1, angle2, path1_matching_angle_list, path2_matching_angle_list ):

   # assign criteria for how closely we have to match teh vector and distance depending on how close the angle is
   matching_criteria = [ [2.0, 4.5, 30.0], [3.0, 3.0, 20.0], [4.0, 2.5, 17.0], [15.0, 2.0, 15.0] ]
   
   # find out which feature to center on for point 1
   path1_rdp2 = get_one_RDP_point_from_angle(path1, angle1)
   
   # find out which feature to center on for point 2
   path2_rdp2 = get_one_RDP_point_from_angle(path2, angle2)
   
 
   path1_rdp2_x, path1_rdp2_y = get_RDP_xy(path1, path1_rdp2)
   path2_rdp2_x, path2_rdp2_y = get_RDP_xy(path2, path2_rdp2)
   

   # center the path1
   index_array = np.array([path1_rdp2_x, path1_rdp2_y])
   path1.route = np.subtract(path1.route, index_array)

   # center the path2
   index_array = np.array([path2_rdp2_x, path2_rdp2_y])
   path2.route = np.subtract(path2.route, index_array)

   path1_rdp2_x, path1_rdp2_y = get_RDP_xy(path1, path1_rdp2)
   path2_rdp2_x, path2_rdp2_y = get_RDP_xy(path2, path2_rdp2)
   



   match_found = 0


   # try aligning with the other RDP points
   for cnt3, path1_aligning_angle in enumerate(path1_matching_angle_list):

      
      good_angle_found_2 = 0
      good_distance = 1
      
      
      if (match_found ==0):
          path2_aligning_angle = path2_matching_angle_list[cnt3]  # find the MSE error between all of our points

          # find out which feature to center on for point 1
          path1_aligning_rdp2 = get_one_RDP_point_from_angle(path1, path1_aligning_angle)
   
          # find out which feature to center on for point 2
          path2_aligning_rdp2 = get_one_RDP_point_from_angle(path2, path2_aligning_angle)
   
          path1_aligning_rdp2_x, path1_aligning_rdp2_y = get_RDP_xy(path1, path1_aligning_rdp2)     # 
          path2_aligning_rdp2_x, path2_aligning_rdp2_y = get_RDP_xy(path2, path2_aligning_rdp2)     # 

          
          distance1 = get_distance(path1_rdp2_x, path1_rdp2_y, path1_aligning_rdp2_x, path1_aligning_rdp2_y)
          distance2 = get_distance(path2_rdp2_x, path2_rdp2_y, path2_aligning_rdp2_x, path2_aligning_rdp2_y)
      
      
      if (match_found == 0 and  abs(distance1 - distance2) < matching_criteria[0][2]+5 and
          path1_rdp2   != path1_aligning_rdp2     and path2_rdp2 != path2_aligning_rdp2  and
          path1_rdp2_x != path1_aligning_rdp2_x   and  path2_rdp2_x != path2_aligning_rdp2_x ):
   
   
         path1_angle = np.arctan( (path1_rdp2_y-path1_aligning_rdp2_y) / (path1_rdp2_x-path1_aligning_rdp2_x) )
         path2_angle = np.arctan( (path2_rdp2_y-path2_aligning_rdp2_y) / (path2_rdp2_x-path2_aligning_rdp2_x) )
   
         path1.rotate_path(path1_angle)
         path2.rotate_path(path2_angle)   # rotate the paths to the same angle
   
   
   
         path1_aligning_rdp2_x, path1_aligning_rdp2_y = get_RDP_xy(path1, path1_aligning_rdp2)     # 
         path2_aligning_rdp2_x, path2_aligning_rdp2_y = get_RDP_xy(path2, path2_aligning_rdp2)     # 
   
         
         # if the x signs values of our aligning points don't match, flip the x of number 2
         if ( np.sign(path1_aligning_rdp2_x) != np.sign(path2_aligning_rdp2_x) ): 
             path2.flip_x_coords()
   
      
         for rotation in range(0,2):
   
            if (  rotation== 1 or rotation== 3):  # on the second loop, flip the y coordinates of the second path
               path2.flip_y_coords()

   
            close_count = 0
            good_angle_found = 0
            close_list = []
            close_list2 = []
            close_list3 = []
   
            for cnt, path1_angle in enumerate(path1_matching_angle_list):
               path2_angle = path2_matching_angle_list[cnt]  # find the MSE error between all of our points

               path1_angle_degrees = path1.angles[path1_angle][0]
               path2_angle_degrees = path2.angles[path2_angle][0]
               angle_diff = abs(path1_angle_degrees - path2_angle_degrees)

               distance_criteria = 30.0  # initially assume it needs to be within 10 meters
               vector_criteria   = 6.0   # assume it needs to be within 1 degrees

               for criteria in matching_criteria:
                   if (angle_diff <= criteria[0]): # if the angle is less than the criteria, assign the distance and vector criteria
                       vector_criteria = criteria[1]
                       distance_criteria = criteria[2]
                       break

               path1_test_rdp1, path1_test_rdp2, path1_test_rdp3 = get_RDP_point_from_angle(path1, path1_angle)
               path2_test_rdp1, path2_test_rdp2, path2_test_rdp3 = get_RDP_point_from_angle(path2, path2_angle)
         
               
               # get the location of the center points of the angle
               path1_test_rdp2_x, path1_test_rdp2_y = get_RDP_xy(path1, path1_test_rdp2)
               path2_test_rdp2_x, path2_test_rdp2_y = get_RDP_xy(path2, path2_test_rdp2)   
               
               # see how close the center points are               
               distance_off = get_distance(path1_test_rdp2_x, path1_test_rdp2_y, path2_test_rdp2_x, path2_test_rdp2_y)
          
               # see how many points are close to matching, but make sure not to double count any
               if ( distance_off < distance_criteria and path1_test_rdp2 not in close_list and path2_test_rdp2 not in close_list2):

                   if (path1_test_rdp1 < path1_test_rdp2):
                      path1_test_rdp1 = path1_test_rdp2 - 1
                      path1_test_rdp3 = path1_test_rdp2 + 1
                   else:
                      path1_test_rdp1 = path1_test_rdp2 + 1
                      path1_test_rdp3 = path1_test_rdp2 - 1
                   
                   if (path2_test_rdp1 < path2_test_rdp2):
                      path2_test_rdp1 = path2_test_rdp2 - 1
                      path2_test_rdp3 = path2_test_rdp2 + 1
                   else:
                      path2_test_rdp1 = path2_test_rdp2 + 1
                      path2_test_rdp3 = path2_test_rdp2 - 1                  
                   

                   # the the location of the rdp points adjacent to the center for each angle, to calculate vectors
                   path1_test_rdp1_x, path1_test_rdp1_y = get_RDP_xy(path1, path1_test_rdp1)
                   path1_test_rdp3_x, path1_test_rdp3_y = get_RDP_xy(path1, path1_test_rdp3)
                   path2_test_rdp1_x, path2_test_rdp1_y = get_RDP_xy(path2, path2_test_rdp1)   
                   path2_test_rdp3_x, path2_test_rdp3_y = get_RDP_xy(path2, path2_test_rdp3)   
               

                   # get the unit vectors for the path
                   path1_vector1 = [ path1_test_rdp2_x - path1_test_rdp1_x, path1_test_rdp2_y - path1_test_rdp1_y]
                   path1_vector2 = [ path1_test_rdp2_x - path1_test_rdp3_x, path1_test_rdp2_y - path1_test_rdp3_y]
                   path2_vector1 = [ path2_test_rdp2_x - path2_test_rdp1_x, path2_test_rdp2_y - path2_test_rdp1_y]
                   path2_vector2 = [ path2_test_rdp2_x - path2_test_rdp3_x, path2_test_rdp2_y - path2_test_rdp3_y]               
                   
                   # get the angle between path1 vector1 and path2 vector1 and 2
                   # and the angle between path2 vector2 and path2 vector1 and 2
                   angle1_1 = angle_between(path1_vector1, path2_vector1) * 57.2957795130823   # the angle of the angle in degrees
                   angle2_1 = angle_between(path1_vector2, path2_vector1) * 57.2957795130823   # the angle of the angle in degrees
                   
                   angle1_2 = angle_between(path1_vector1, path2_vector2) * 57.2957795130823   # the angle of the angle in degrees
                   angle2_2 = angle_between(path1_vector2, path2_vector2) * 57.2957795130823   # the angle of the angle in degrees
                   
                   not_a_match=1
                   # see if the first vector and the vector from path 2 are mostly aligned
                   if ( angle1_1 < vector_criteria  or angle1_1 > (180-vector_criteria) or angle1_2 < vector_criteria or angle1_2 > (180-vector_criteria)):
                       # see if the second vector from path1 is mostly aligned with a vector from path 1 
                       if ( angle2_1 < vector_criteria  or angle2_1 > (180-vector_criteria) or angle2_2 < vector_criteria or angle2_2 > (180-vector_criteria)):
                           not_a_match=0   # this is a good enough match to continue

                   if (not_a_match ==0):  # if the vectors are properly aligned
                       close_count += 1
                       close_list.append( path1_test_rdp2)
                       close_list2.append( path2_test_rdp2)
                       close_list3.append( [path1_test_rdp2, path2_test_rdp2] )
                       
                       if (path1_angle_degrees < 135):  # look for angles that aren't completely flat
                          good_angle_found =1
                          
                       #if (path1_angle_degrees < 160):  # look for angles that aren't completely flat
                       #   good_angle_found_2 = 1
                          
                       #if ( angle1_1 > 6  and angle1_1 < (180-6) and angle1_2 > 6 and angle1_2 < (180-6)):
                       #   good_distance = 0                          



   
            if ( close_count >= 3):  # hold onto the lowest error case
               
               #close_list3.sort()
               #matching_distance_count = 0
               #for rdp_cnt in range(0,len(close_list3)-1):
               #   rdp1_1 = close_list3[rdp_cnt][0]    # get the path distance betwee these points
               #   rdp1_2 = close_list3[rdp_cnt+1][0]
               #
               #   rdp2_1 = close_list3[rdp_cnt][1]
               #   rdp2_2 = close_list3[rdp_cnt+1][1]
               #   
               #   route_distance1 = path1.get_route_distance(int(path1.feature_loc[rdp1_1,2]), int(path1.feature_loc[rdp1_2,2]))
               #   route_distance2 = path2.get_route_distance(int(path2.feature_loc[rdp2_1,2]), int(path2.feature_loc[rdp2_2,2]))
               #
               #   max_distance = max(route_distance1,route_distance2)
               #   min_distance = min(route_distance1,route_distance2)
               #
               #   if (max_distance/min_distance < 1.25 or max_distance-min_distance < 20):
               #       matching_distance_count+=1
               #
               #if (matching_distance_count < 2):
               #    path1.print_flag = 1


               matching_distance_count = 0
               diff1 = max(close_list) - min(close_list)
               diff2 = max(close_list2) - min(close_list2) 
               if (close_count >=5 or good_angle_found==1 or diff1 > 5 or diff2>5):

                  close_list3.sort()
                  matching_distance_count = 0
                  #print(path1.routeid, path2.routeid)
                  for rdp_cnt in range(0,len(close_list3)-1):
                     rdp1_1 = close_list3[rdp_cnt][0]    # get the path distance betwee these points
                     rdp1_2 = close_list3[rdp_cnt+1][0]
                  
                     rdp2_1 = close_list3[rdp_cnt][1]
                     rdp2_2 = close_list3[rdp_cnt+1][1]
                     
                     #route_distance1 = path1.get_route_distance(int(path1.feature_loc[rdp1_1,2]), int(path1.feature_loc[rdp1_2,2]))
                     #route_distance2 = path2.get_route_distance(int(path2.feature_loc[rdp2_1,2]), int(path2.feature_loc[rdp2_2,2]))
                  
                     path1_segment_start =  int(path1.feature_loc[rdp1_1,2])
                     path1_segment_end   =  int(path1.feature_loc[rdp1_2,2])
                     path2_segment_start =  int(path2.feature_loc[rdp2_1,2])
                     path2_segment_end   =  int(path2.feature_loc[rdp2_2,2])
                     max_distance = 0
                     max_distance = search_matches.max_distance_between_segments(path1.route, path2.route, path1_segment_start, path1_segment_end, \
                                    path2_segment_start, path2_segment_end)
   
                     #print("Max distance is ",max_distance)
                     if ( max_distance < 18):
                         matching_distance_count+=1                  
                  
               
                  #if (matching_distance_count < 2):
                  #    path1.print_flag = 1                  
                     
                      
               if (matching_distance_count >= 2):
               
                   # the current RDP has a problem with matching up gentle curves
                   # to combat this, we will look for either, 4 matching points, or 1 point with a sharp enough turn
                   # which I am starting to SWAG at 145 degrees, or that the three matching RDP points aren't all in a row
                   # for either path1 or path2                   
                   if (close_count >=5 or good_angle_found==1):  # if we have at least 4 matches, or 1 of them was a good angle, count it
                      match_found = 1
                      #if (good_distance ==0):
                      #   path1.print_flag = 1
                      #   #print("here1")
                      return match_found
    
                   else:
                      diff1 = max(close_list) - min(close_list)
                      diff2 = max(close_list2) - min(close_list2)
                      if (diff1 > 5 or diff2>5):  # if all of the RDP points aren't sequential then count it
                         match_found = 1
                         #if (good_distance ==0):
                         #    path1.print_flag = 1     
                         #    #print("here2")
                         return match_found


   return  match_found



#********************
#**** this aligns and orients two matching paths the same before plotting and saving them two a file for viewing
#********************  
def align_two_paths(path1, path2,driver_id,rdp_tolerance):
   
   
   path1_matching_angle_list = path1.comparison[-1][3:]
   path2_matching_angle_list = path2.comparison[-1][3:]
   # loop through each of the angles that was a good match, and see which one makes the lowest error when they are aligned
   match_found = 0
   for cnt, angle1 in enumerate(path1_matching_angle_list):
      angle2 = path2_matching_angle_list[cnt]

      if (match_found ==0):      
         match_found = align_and_score_two_paths(path1, path2, angle1, angle2, path1_matching_angle_list, path2_matching_angle_list )

   #print ("here2")
   #print("match_found is ",match_found)

   if (match_found == 1):

      # if one path is a lot longer than the other, zoom in on the shorter one
      #if (path1.distance < path2.distance / 5.0   or  path2.distance < path1.distance / 5.0):
      x1_max = np.amax ( path1.route[:,0] )
      x1_min = np.amin ( path1.route[:,0] )
      x2_max = np.amax ( path2.route[:,0] )
      x2_min = np.amin ( path2.route[:,0] )
       
      y1_max = np.amax ( path1.route[:,1] )
      y1_min = np.amin ( path1.route[:,1] )
      y2_max = np.amax ( path2.route[:,1] )
      y2_min = np.amin ( path2.route[:,1] )   
          
      x_upper_bound = min( x1_max, x2_max) + 500
      x_lower_bound = max( x1_min, x2_min) - 500
      y_upper_bound = min( y1_max, y2_max) + 500
      y_lower_bound = max( y1_min, y2_min) - 500   
      
      
      x_upper_bound2 = min( x1_max + 250, x2_max + 250, 1000) 
      x_lower_bound2 = max( x1_min - 250, x2_min - 250, -1000) 
      y_upper_bound2 = min( y1_max + 250, y2_max + 250, 1000) 
      y_lower_bound2 = max( y1_min - 250, y2_min - 250, -1000)   
      
      
      
      plt.figure()
      plt.plot(path1.route[:,0],path1.route[:,1],markersize=2.0)
      plt.plot(path2.route[:,0],path2.route[:,1],markersize=2.0)
   
   
   
      feature_list1 = []
      feature_list2 = []
      for cnt, path1_angle in enumerate(path1_matching_angle_list):
         path2_angle = path2_matching_angle_list[cnt]  # find the MSE error between all of our points
      
         path1_test_rdp1, path1_test_rdp2, path1_test_rdp3 = get_RDP_point_from_angle(path1, path1_angle)
         path2_test_rdp1, path2_test_rdp2, path2_test_rdp3 = get_RDP_point_from_angle(path2, path2_angle)
      
         path1_test_rdp2_x, path1_test_rdp2_y = get_RDP_xy(path1, path1_test_rdp2)
         path2_test_rdp2_x, path2_test_rdp2_y = get_RDP_xy(path2, path2_test_rdp2)
      
         feature_list1.append( [path1_test_rdp2_x, path1_test_rdp2_y] )
         feature_list2.append( [path2_test_rdp2_x, path2_test_rdp2_y] )
      


#      #* Temporary
      path1.update_feature_loc()
      path2.update_feature_loc()
  
      path1_features = path1.feature_loc[:,0:2]
      path2_features = path2.feature_loc[:,0:2]

      #plt.scatter(path1_features[:,0],path1_features[:,1])
      #plt.scatter(path2_features[:,0],path2_features[:,1])
#      #* Temporary


      #file1 = open("test1.csv",'wb')
      #file1_csv = csv.writer(file1)
      #for angle in path1.angles:
      #   file1_csv.writerow(angle)
      #file1.close()         

      #file2 = open("test2.csv",'wb')
      #file2_csv = csv.writer(file2)
      #for angle in path2.angles:
      #   file2_csv.writerow(angle)
      #file2.close()
      
      feature_list1 = np.array(feature_list1)
      plt.scatter(feature_list1[:,0],feature_list1[:,1],c='red')
      
      feature_list2 = np.array(feature_list2)
      plt.scatter(feature_list2[:,0],feature_list2[:,1],c='red')
   
      plt.show()
   
      #print ("here 3")
   
   
      # if one path is a lot longer than the other, zoom in on the shorter one
      if (path1.distance < path2.distance / 5.0   or  path2.distance < path1.distance / 5.0):   
          plt.axis( (x_lower_bound, x_upper_bound, y_lower_bound, y_upper_bound) )
      #else:
      #    plt.axis( (x_lower_bound2, x_upper_bound2, y_lower_bound2, y_upper_bound2) )
      
      
      #plt.show()
      plt.savefig("Test_Set\\Driver_" + str(driver_id)+"_" + str(path1.routeid) + "__" + str(path2.routeid) +"__"+ str(rdp_tolerance)+"m.png")
      #plt.savefig("Test_Set\\Driver_1_" + str(path2.routeid) + "__" + str(path1.routeid) +".png")
      plt.close()

   return
#********************
#**** end aligns and orients two matching paths the same before plotting and saving them two a file for viewing
#********************  



