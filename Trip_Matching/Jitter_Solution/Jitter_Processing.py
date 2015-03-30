import csv
import os
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from path import Path
from vector_math import *
from file_paths import *
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
   








#********************
#**** main code
#********************  
#@profile
def mainloop(driver_id, rdp_tolerance, Input_Path):


    Input_Path =   DATA

    start_time = time.time()
    
    
    list_of_paths = []   
    jitter_count = 0
    jitter_tolerance = 15
    
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



       # only analyze this path if it is not within a 50 meter bound of the starting point
       max_value = np.amax(path.route)
       min_value = np.amin(path.route)
       if ( max_value < 90 and min_value > -90): 
           path.is_zero = 1   # this is a zero length route
           path.matched = 1
           jitter_count+=1

           #plt.figure()
           #plt.plot(path.route[:,0],path.route[:,1],markersize=2.0)
           #plt.savefig("Test_Set\\Driver_" + str(driver_id)+"_" + str(path.routeid) +".png")
           #plt.close()    
    

       # find the total distance along the route
       path.distance = path.get_route_distance(0, path.time)

       list_of_paths.append(path)
       
       
       
    
    #print("here 1")

    num_matched = 0
    final_out = open("Results_Jitter//Driver_" + str(driver_id)+".csv",'wb')
    final_out_csv = csv.writer(final_out)
    for cnt1, path1 in enumerate(list_of_paths):
       final_out_csv.writerow([driver_id, path1.routeid, path1.matched])
       if (path1.matched ==1):
          num_matched+=1
          
    
    fout = open("jitter_match_list.txt",'a')
    fout.write("Driver " + str(driver_id) +"      num jitter           " + str(num_matched) + "\n")
    fout.close()
    
    end_time = time.time()
    
    print("minutes elapsed ",(end_time-start_time) / 60. )
    
    
    
    
    
    
    
    
    
    #plt.show()
    
    #sys.exit(0)
    
    
    #time_vs_distance = []
    #for cnt, path in enumerate(list_of_paths):
    #   time_vs_distance.append( [ path.time, path.distance] )
       
    
    #time_vs_distance = np.array(time_vs_distance)   
    #plt.figure(2)
    #plt.scatter(time_vs_distance[:,0],time_vs_distance[:,1])
    #plt.show()
    
    
    
    #********************
    #**** end main code
    #********************  
    
    
    




# drivers start at 1 and the last one is 3612 however there are gaps in between
# there are a total of 2736 drivers

rdp_tolerance_list = [ 13, 17, 19]
rdp_tolerance_list = [13]

#data_path_file = open("..\\..\\SETTINGS.json",'rb')
#file_paths = data_path_file.readlines()
#for file_path in file_paths:
#   if ('DATA' in file_path):
#      Input_Paths = file_path.split("\"")
#      for cnt1, string1 in enumerate(Input_Paths):
#         if (string1 == 'DATA'):
#            location1 = cnt1
#      Input_Path2 = Input_Paths[location1 +2]
#      Input_Path =''
#      for char1 in Input_Path2:
#         if (char1 == '\\'):
#            Input_Path = Input_Path + '\\' + '\\'
#         else:
#            Input_Path = Input_Path + char1
#            
#      Input_Path = Input_Path +  '\\' + '\\'  
#      try:
#         file_name =  Input_Path +str(1)+"\\" + str(1) + ".csv"
#         fileopen = open(file_name,'rb')      
#         fileopen.close()   # close the file that we read from   
#      except:
#         print("Could not open the raw data from the path read in from Settings.json   ")
#         print("quiting")
#         sys.exit()
      
      

#Input_Path =   "..\\..\\..\\drivers_raw\\" 


if( not os.path.isdir("Results_Jitter")  ):
   os.mkdir("Results_Jitter")

Input_Path =   DATA
    
for driver_id in range(1,3613):

   #rdp_tolerance = 15

   #if (1==1):
   try:
      file_name =  os.path.join(Input_Path,str(driver_id),str(1) + ".csv")
      fileopen = open(file_name,'rb')      
      fileopen.close()   # close the file that we read from  
      
      for rdp_tolerance in rdp_tolerance_list:
         print ("doing driver ",driver_id)
         mainloop(driver_id, rdp_tolerance, Input_Path)
   except:
      pass