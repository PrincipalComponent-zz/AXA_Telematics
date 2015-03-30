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
   

tolerance_list = [  9, 10, 11,12, 13,14, 15, 17, 19, 21, 25, 30, 35, 7, 8]
#tolerance_list = [ 35]

for tolerance in tolerance_list:

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
    
    out_file_name = 'Final_Results_' + str(tolerance) +'m_New.csv'
    out_file_path = os.path.join(MODELS,out_file_name)
    
    out_file = open(out_file_path,'wb')
    out_csv = csv.writer(out_file)
    out_csv.writerow(header)
    
    cnt_1 = 0    
    cnt_driver = 0
        
    open_file = open("junk.txt",'wb')    
        
    for driver_id in list_ids:
       #try:
          file_name = 'Results_' + str(tolerance) +'m\Driver_' + str(driver_id) + '.csv'
          file_open = open(file_name,'rb')      
          file_csv = csv.reader(file_open)
    
          cnt_driver+=1
    
          cnt_row = 0
          for row in file_csv:
             cnt_row+=1         
             
             out_csv.writerow( [ str(row[0]) + '_' + str(row[1]), row[2] ] )
             result = float(row[2])
             if (result >= 1):
                cnt_1 +=1

          if (cnt_row != 200):
             print("tolerance",tolerance," driver ",driver_id," number ",cnt_row )



          
          file_open.close()   # close the file that we read from  
          
       #except:
       #   for route in range(1,201):
       #       out_csv.writerow( [ str(driver_id) + '_' + str(route), 0 ] )
       #   open_file.write("driver not in list     " + str(driver_id) + "\n")
       #   print("driver not in list ",driver_id)
              
              
    print("Tolerance ",tolerance," Number of 1s " + str(driver_id) + "    " + str(cnt_1))     
    
    
    print("Number of drivers processed "  + str(cnt_driver) )
    
    out_file.close()