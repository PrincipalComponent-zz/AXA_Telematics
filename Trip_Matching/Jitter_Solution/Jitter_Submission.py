import csv
import os
import sys
import time

import numpy as np
import matplotlib.pyplot as plt
from file_paths import *





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
   



sample_open = open('sampleSubmission1.csv','rb')      
sample_csv = csv.reader(sample_open)

list_ids = []
header = sample_csv.next()
for row in sample_csv:
   driver_ids = row[0].split('_')
   driver_ids = int(driver_ids[0])
   
   if (driver_ids not in list_ids):
      list_ids.append(driver_ids)

#list_ids.sort()
#for driver_id in list_ids:
#   print driver_id

sample_open.close()   # close the file that we read from  

jitter_tolerance = 3
filename = 'Final_Results_All_Jitter.csv'

file_path = os.path.join(MODELS,filename)

out_file = open(file_path,'wb')
out_csv = csv.writer(out_file)
out_csv.writerow(header)

cnt_1 = 0    
cnt_driver = 0
    
open_file = open("junk.txt",'wb')    

jitter_count = 0


    
for driver_id in list_ids:
   try:
      file_name = 'Results_Jitter\Driver_' + str(driver_id) + '.csv'
      file_open = open(file_name,'rb')      
      file_csv = csv.reader(file_open)

      cnt_driver+=1

      driver_info = []
      jitter_count = 0
      for row in file_csv:
         driver_info.append(row)
         if (int(row[2]) ==1):
            jitter_count +=1
            
         
      for row in driver_info:   
         if (jitter_count >= 0):   # if there are enough jitters for this driver
             if (int(row[2]) > 0):
                out_csv.writerow( [ str(row[0]) + '_' + str(row[1]), jitter_count ] )
             else:
                out_csv.writerow( [ str(row[0]) + '_' + str(row[1]), 0 ] )
             result = int(row[2])
             if (result == 1):
                cnt_1 +=1
         else:  # assume just noise
             out_csv.writerow( [ str(row[0]) + '_' + str(row[1]), 0 ] )


      open_file.write(str(driver_id)+",    "+str(jitter_count)+"\n")
      
      file_open.close()   # close the file that we read from  
      
   except:
      for route in range(1,201):
          out_csv.writerow( [ str(driver_id) + '_' + str(route), 0 ] )
      open_file.write("driver not in list     " + str(driver_id) + "\n")
          
          
print("Number of 1s     " + str(cnt_1))     


print("Number of drivers processed "  + str(cnt_driver) )

out_file.close()