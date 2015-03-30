import csv
import os
import sys
import time

import numpy as np
#import matplotlib.pyplot as plt

from modules_scott.path import Path
from modules_scott.vector_math import *
from modules_janto.paths import *
#from find_matches import *


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
   

#*************** get the 10, 30, 50, 70, 90 percent numbers
def get_quintiles(float_list):
   float_list.sort()
   
   quintiles = []
   list_length = len(float_list)
   
   if ( list_length > 5):
   
      for x in range( 10, 110, 20):
        index1 = int(list_length * x / 100.)
        value1 = float_list[index1]
        
        quintiles.append(value1)
   
   
   else:
      quintiles = [0, 0, 0, 0, 0]


   return quintiles




#********************
#**** main code
#********************  
#@profile
def mainloop(driver_id, final_out_csv, Input_Path):


    start_time = time.time()
    
    
    list_of_paths = []   
    list_of_lengths = []
    
    # read all the routes for this driver
    for cnt in range(1,201):
    
       # initialize this path
       path = Path(1,cnt)   # start with driver 1, route 1
    
       input_coords=[] 
#       file_name = "Test_Set\\driver_1\\" + str(cnt) + ".csv"
       file_name = os.path.join(Input_Path,str(driver_id),str(cnt) + ".csv")
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
           
    


       # find the total distance along the route
       path.distance = path.get_route_distance(0, path.time)
       
       speed_hold = path.speed
       accel_hold = path.acceleration
       
       path.speed_quintiles = get_quintiles(speed_hold)
       path.acceleration_quintiles = get_quintiles(accel_hold)
       
       path.energy_per_distance = path.total_energy / path.distance
       path.energy_per_time = path.total_energy / path.time
       
       list_of_lengths.append(path.distance)


       #if ( path.is_zero == 0) :    
       #    # get features on this path
       #    path.generate_features(rdp_tolerance)
       #
       #    # get angles between each of the consective features
       #    path.generate_angles()         
    
       
       list_of_paths.append(path)
    

    

    for cnt1, path1 in enumerate(list_of_paths):
       path1.distance = round(path1.distance,4)
       path1.time = round(path1.time,4)
       path1.is_zero = round(path1.is_zero,4)
       
       speed1 = round(path1.speed_quintiles[0],4)
       speed2 = round(path1.speed_quintiles[1],4)
       speed3 = round(path1.speed_quintiles[2],4)
       speed4 = round(path1.speed_quintiles[3],4)
       speed5 = round(path1.speed_quintiles[4],4)
       
       accel1 = round(path1.acceleration_quintiles[0],4)
       accel2 = round(path1.acceleration_quintiles[1],4)
       accel3 = round(path1.acceleration_quintiles[2],4)
       accel4 = round(path1.acceleration_quintiles[3],4)
       accel5 = round(path1.acceleration_quintiles[4],4)  
       
       time_at_speed =[]
       for i in range(0,10):
          time_at_speed.append(  round(path1.time_in_speed[i] / (path1.time-2),5) )
       
       total_energy = round(path1.total_energy,4)
       energy_per_distance = round(path1.energy_per_distance,4)
       energy_per_time = round(path1.energy_per_time,4)
       
       final_out_csv.writerow([driver_id, path1.routeid, path1.distance, path1.time, path1.is_zero,speed1,speed2,speed3,speed4,speed5,accel1,accel2,accel4,accel5,total_energy,energy_per_distance,energy_per_time,time_at_speed[0],time_at_speed[1],time_at_speed[2],time_at_speed[3],time_at_speed[4],time_at_speed[5],time_at_speed[6],time_at_speed[7],time_at_speed[8],time_at_speed[9] ])
    
         
    

    
    end_time = time.time()
    print "\tMinutes elapsed ",(end_time-start_time) / 60.,"\n" 
    



    
    #********************
    #**** end main code
    #********************  
    

# Path to raw data
Input_Path =   DATA
    


final_out = open("featurematrix2.csv",'wb')
final_out_csv = csv.writer(final_out)          
final_out_csv.writerow(['driver','route','distance','time','is_jitter','speed10pct','speed30pct','speed50pct','speed70pct','speed90pct','accel10pct','accel30pct','accel70pct','accel90pct','total_energy','energy_per_distance','energy_per_time'])


# data_path_file = open("..\\..\\..\\SETTINGS.json",'rb')
# file_paths = data_path_file.readlines()
# for file_path in file_paths:
#    if ('DATA' in file_path):
#       Input_Paths = file_path.split("\"")
#       for cnt1, string1 in enumerate(Input_Paths):
#          if (string1 == 'DATA'):
#             location1 = cnt1
#       Input_Path2 = Input_Paths[location1 +2]
#       Input_Path =''
#       for char1 in Input_Path2:
#          if (char1 == '\\'):
#             Input_Path = Input_Path + '\\' + '\\'
#          else:
#             Input_Path = Input_Path + char1
            
#       Input_Path = Input_Path +  '\\' + '\\'  
#       try:
#          file_name =  Input_Path +str(1)+"\\" + str(1) + ".csv"
#          fileopen = open(file_name,'rb')      
#          fileopen.close()   # close the file that we read from   
#       except:
#          print("Could not open the raw data from the path read in from Settings.json   ")
#          print("quiting")
#          sys.exit()
      
print "\n\nExtracting feature set 2...\n\n"  
    
for driver_id in range(1,3613):


   #if (driver_id <= 3613):
   #   print("here 1")
   try: 
      file_name =  os.path.join(Input_Path,str(driver_id),str(1) + ".csv")
      fileopen = open(file_name,'rb')      
      fileopen.close()   # close the file that we read from  
      

      print "Processing driver ",driver_id
      mainloop(driver_id, final_out_csv, Input_Path)
   except:
      x=1
   
   
final_out.close()     

print '\nfeaturematrix 2 created.'