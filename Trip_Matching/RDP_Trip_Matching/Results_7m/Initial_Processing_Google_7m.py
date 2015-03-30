import csv
import os
import sys
import time

import numpy as np
#import matplotlib.pyplot as plt

from path import Path
from vector_math import *
from find_matches import *


#********************
#**** this function reads a CSV file and returns a header, and a list that has been converted to float
#********************
def read_csv_float_with_header(file1,list1):

   fileopen = open(file1,'rb')
   fileobject = csv.reader(fileopen)
   
   # get the header
   header = fileobject.next()  
   
   # read each line in the CSV, and convert the values to float before appending to list1
   for row in fileobject:
      float_line = []
      for subrow in row:
         float_line.append( float(subrow))
      
      list1.append( float_line)
      
   fileopen.close()   # close the file that we read from   
   
   return  header, list1
#********************
#**** end function reads a CSV file and returns a header, and a list that has been converted to float
#********************   
   








#********************
#**** main code
#********************  
#@profile
def mainloop(driver_id, rdp_tolerance, current_results, route1_id, route2_id,old_rdp_tolerance):


    old_scores = []
    old_file = open("Results_"+str(old_rdp_tolerance)+"m/Driver_"+str(driver_id)+".csv",'rb')
    old_csv = csv.reader(old_file)
    for row in old_csv:
       route = int(row[1])
       num_matched = float(row[2])
       old_scores.append([route, num_matched])
       #print(route, num_matched)
    #sys.exit(0)
    
    
    old_scores.sort()


    start_time = time.time()
    
    
    list_of_paths = []   
    list_of_lengths = []
    
    list_of_routes = []
    for cnt in range(100,201):
       list_of_routes.append(cnt)
    for cnt in range(99,0,-1):
       list_of_routes.append(cnt)
    
    
    # read all the routes for this driver
    for cnt in list_of_routes:
    
       # initialize this path
       path = Path(1,cnt)   # start with driver 1, route 1
    
       input_coords=[] 
#       file_name = "Test_Set\\driver_1\\" + str(cnt) + ".csv"
       file_name = "/home/savvyaffiliate_gmail_com/drivers_raw/drivers_raw/"+str(driver_id)+"/" + str(cnt) + ".csv"
       header, input_coords = read_csv_float_with_header(file_name,input_coords)
       path_array = np.array(input_coords)
       
       
       path.route = path_array
       path.time  = len(path.route)   # 1 second per data file



       # only analyze this path if it is not within a 90 meter bound of the starting point
       max_value = np.amax(path.route)
       min_value = np.amin(path.route)
       if ( max_value < 90 and min_value > -90): 
           path.is_zero = 1   # this is a zero length route
           path.matched = 0   # the jitter is done differently
           
    
    
       #if ( path.is_zero == 0) :
       #   x_coord = path.route[ path.time-1, 0]
       #   y_coord = path.route[ path.time-1, 1]
       #   angle_off_horizontal =  np.arctan( y_coord / x_coord )
    
       #   path.rotate_path(angle_off_horizontal)
    
       #   x_coord = path.route[ path.time-1, 0]
       #   y_coord = path.route[ path.time-1, 1]      
       #   if (x_coord < 0) :   # for quadrant 2 & 3 rotate back to quadrant 1
       #      angle_off_horizontal =  np.pi 
       #      path.rotate_path(angle_off_horizontal)

       #   # make our new 0, 0 point be the highest point in the path, bisecting the angle that makes the tallest
       #   path.center_on_highest_point()
          



       # find the total distance along the route
       path.distance = path.get_route_distance(0, path.time)
       list_of_lengths.append(path.distance)


       if ( path.is_zero == 0) :    
           # get features on this path
           path.generate_features(rdp_tolerance)


           #plt.figure()
           #plt.plot(path.route[:,0],path.route[:,1],markersize=2.0)
         
           #feature_list = []
        
           #for cnt, feature in enumerate(path.feature_loc):
           #   x1 = path.route[   path.feature_loc[cnt,2] ,0]
           #   y1 = path.route[   path.feature_loc[cnt,2] ,1]
           #   feature_list.append( [x1, y1] )
           #feature_list = np.array(feature_list)
           #
           #plt.scatter(feature_list[:,0],feature_list[:,1])




           #plt.figure()
           #plt.plot(path.route[:,0],path.route[:,1],markersize=2.0)
         
           #feature_list = []
        
           #for cnt, feature in enumerate(path.feature_loc):
           #   x1 = path.route[   path.feature_loc[cnt,2] ,0]
           #   y1 = path.route[   path.feature_loc[cnt,2] ,1]
           #   feature_list.append( [x1, y1] )
           #feature_list = np.array(feature_list)
           #
           #plt.scatter(feature_list[:,0],feature_list[:,1])
           
           #plt.show()

    
           # get angles between each of the consective features
           path.generate_angles()         

           if (old_scores[cnt-1][0] == cnt):
              if (old_scores[cnt-1][1] >= 2.999):  # remember and use the old score
                 path.matched = old_scores[cnt-1][1]
    
    
       
       list_of_paths.append(path)
    


    
    list_to_run = []
    #list_to_run.append( [11,19] )
    #list_to_run.append( [17,9,15] )
    #list_to_run.append( [63, 83, 120, 148] )
    #list_to_run.append( [102, 167, 183, 197, 200] )
    
    
    #list_to_run.append( [5,96] )
    
    for cnt, path in enumerate(list_of_paths):
       if ( path.is_zero == 0) :
           for cnt2, run_list in enumerate(list_to_run):
              if ( path.routeid in run_list):
                 #plt.figure(cnt2+1)
                 #plt.plot(path.route[:,0],path.route[:,1],markersize=2.0)
        
                 feature_list = []
        
                 for cnt, feature in enumerate(path.feature_loc):
                    x1 = path.route[   path.feature_loc[cnt,2] ,0]
                    y1 = path.route[   path.feature_loc[cnt,2] ,1]
                    feature_list.append( [x1, y1] )
                 feature_list = np.array(feature_list)
                 
                 #plt.scatter(feature_list[:,0],feature_list[:,1])
        
                 # make CSV files of our angles
                 #file_name = open("Angle_Info_" + str(path.routeid) + ".csv",'wb')
                 #file_object = csv.writer(file_name)
                 #
                 #for angle in path.angles:
                 #   file_object.writerow(angle)
                 #   
                 #file_name.close()
    
    
    
    
    for cnt1, path1 in enumerate(list_of_paths):
       for cnt2, path2 in enumerate(list_of_paths[cnt1+1:]):

        #if (path1.routeid == route1_id and path2.routeid == route2_id ):
          

          if (path1.matched < 3 or path2.matched < 3):  # if one of the two paths aren't matched, check it
             if ( path1.is_zero == 0 and path2.is_zero == 0) :  # make sure we don't run a zero length path          

                 path2.print_flag = 0 # default to not making a picture
                 path1.print_flag = 0                 
                 
                 if (path1.routeid != path2.routeid):  # don't compare a path against itself
                    compare_two_sets_of_angles(path1, path2)   # Compare these two paths and record the score in path 1
    
    
             #path1.print_flag = 1
             #if (path1.matched ==1 or path2.matched ==1):   # if we matched this time, see if it is a new match
             #if (path1.print_flag==1 or path2.print_flag==1):
             #
             # 
             # 
             #   driver_and_route1 = str(driver_id)+"_"+str(path1.routeid)
             #   driver_and_route2 = str(driver_id)+"_"+str(path2.routeid)
             #   index1 = current_results_drivers.index(driver_and_route1)
             #   index2 = current_results_drivers.index(driver_and_route2)
             #   previous_value1 = current_results[index1][1]
             #   previous_value2 = current_results[index2][1]
#
#
             #   if (previous_value1 ==0 and rdp_tolerance==15):
             #       path1.print_flag = 1
             #   else:
             #       path1.print_flag = 0
             #   if (previous_value2 ==0 and rdp_tolerance==15):
             #       path2.print_flag = 1
             #   else:
             #       path2.print_flag = 0
             #   #
             #   if (path1.print_flag==1 or path2.print_flag==1):  # if the new values are a match that wasn't a previous match, print it
             #       print(path1.routeid, path2.routeid)
             #       align_two_paths(path1, path2,driver_id,rdp_tolerance)
             #      
             #       path2.print_flag = 0
             #       path1.print_flag = 0
    ##
    #

    
    #print ("not writing results")
    #sys.exit(0)


    list_of_lengths.sort()
    for cnt1, path1 in enumerate(list_of_paths):
       if (path1.distance > list_of_lengths[190] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -2
       elif (path1.distance > list_of_lengths[180] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -1
       elif (path1.distance > list_of_lengths[170] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -3
       elif (path1.distance > list_of_lengths[160] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -4
       elif (path1.distance > list_of_lengths[150] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -5
       elif (path1.distance > list_of_lengths[140] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -6
       elif (path1.distance > list_of_lengths[120] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -7
       elif (path1.distance > list_of_lengths[100] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -8    
       elif (path1.distance > list_of_lengths[80] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -9
       elif (path1.distance > list_of_lengths[60] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -9.5
       elif (path1.distance > list_of_lengths[40] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -9.7
       elif (path1.distance > list_of_lengths[20] and path1.matched <=0):   # if it is a long path and not matched, move it down the ranking
          path1.matched += -9.8    
    

    num_matched = 0
    final_out = open("Results_"+str(rdp_tolerance)+"m//Driver_" + str(driver_id)+".csv",'wb')
    final_out_csv = csv.writer(final_out)
    for cnt1, path1 in enumerate(list_of_paths):
       final_out_csv.writerow([driver_id, path1.routeid, path1.matched])
       if (path1.matched >=1):
          num_matched+=1
          
    
    fout = open("intial_match_list.txt",'a')
    fout.write("Driver " + str(driver_id) +"      num matched           " + str(num_matched) + "\n")
    fout.close()
    
    end_time = time.time()
    print("matches ",num_matched)
    print("minutes elapsed ",(end_time-start_time) / 60. )
    











    
    
    #match_list_file = open("Matching_Routes.csv",'wb')
    #match_list_csv = csv.writer(match_list_file)    
    #match_list_csv.writerow(['Route','Matches'])
#
    #for cnt1, path1 in enumerate(list_of_paths):
    #   matching_routes = [path1.routeid]
    #   for cnt2 in path1.comparison:
    #      matching_routes.append(cnt2[0])
    #   
    #   match_list_csv.writerow(matching_routes)
    #
    #
    #match_list_file.close()
    










    
    
    #plt.show()
    
    #sys.exit(0)
    
    
    #time_vs_distance = []
    #color_list=[]
    #for cnt, path in enumerate(list_of_paths):
    #   if (path.matched==1):
    #      time_vs_distance.append( [ path.time, path.distance] )
    #      color_list.append("red")
    #   elif(path.is_zero ==1):
    #      time_vs_distance.append( [ path.time, path.distance] )       
    #      color_list.append("blue")       
    #   else:
    #      time_vs_distance.append( [ path.time, path.distance] )       
    #      color_list.append("green")
    #
    #time_vs_distance = np.array(time_vs_distance)   
    #plt.figure(2)
    #plt.scatter(time_vs_distance[:,0],time_vs_distance[:,1],c=color_list,s=100)
    #plt.show()
    #plt.close()
    #
    #
    
    #********************
    #**** end main code
    #********************  
    
    
    


current_results = []
#current_results_drivers = [] # just the driver ids
#
#current_results_file = "..\Current_Best_Path_Solution.csv"
##current_results = read_csv_float_with_header(current_results_file,current_results)
#
#fileopen = open(current_results_file,'rb')
#fileobject = csv.reader(fileopen)
## get the header
#header = fileobject.next()
## read each line in the CSV, and convert the values to float before appending to list1
#for row in fileobject:
#    current_results.append( [row[0],int(float(row[1]))] )
#    current_results_drivers.append(row[0])      
#fileopen.close()
#


#not_matches = []
#not_matches_drivers = []
#current_results_file = "Not_Matches.csv"
#
#fileopen = open(current_results_file,'rb')
#fileobject = csv.reader(fileopen)
## read each line in the CSV, and convert the values to float before appending to list1
#for row in fileobject:
#    not_matches.append( [row[0],int(row[1]),int(row[2])] )
#    not_matches_drivers.append(row[0])      
#fileopen.close()



# drivers start at 1 and the last one is 3612 however there are gaps in between
# there are a total of 2736 drivers

rdp_tolerance_list = [ 11, 13, 14, 15, 17, 19 ]
#rdp_tolerance_list = [17]

rdp_tolerance_list = [7]
old_rdp_tolerance = 10

# 1-1701
# 1701 - 2651
# 2561 - 3613
    
for driver_id in range( 3416, 1, -3):

#for driver_info in not_matches:
#   driver_id = int(driver_info[0])
#   route1_id = int(driver_info[1])
#   route2_id = int(driver_info[2])

   route1_id = 1
   route2_id = 2

   #rdp_tolerance = 15

   #if (driver_id <= 1700):
   #   print("here 1")
   run_it = 1
   try: 
      file_name = "/home/savvyaffiliate_gmail_com/drivers_raw/drivers_raw/"+str(driver_id)+"/" + str(1) + ".csv"
      fileopen = open(file_name,'rb')      
      fileopen.close()   # close the file that we read from  
   except:
      run_it = 0
   
   if (run_it ==1):
      for rdp_tolerance in rdp_tolerance_list:
         print ("doing driver ",driver_id, "   rdp ",rdp_tolerance)
         mainloop(driver_id, rdp_tolerance, current_results, route1_id, route2_id,old_rdp_tolerance)
