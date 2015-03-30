import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from random import sample
import os
import sys
import time
import csv

from modules_janto.paths import *

blockresults = os.path.join(FEATURES,"blocks","results")

print '\n\nCombining block outputs Random Forest (feature set 3)...\n'

def break_input_file_features(combined_file):


   output_file = open(combined_file, 'wb')
   output_csv = csv.writer(output_file)

   cnt=0

   for i in range(1,29):
   


         input_found = 0
         try:
            telematics_input = open(os.path.join(blockresults,"Telematics_results_Forest_Run3_block_" + str(i)+ ".csv"),'rU')
            telematics_csv = csv.reader(telematics_input)
            input_found = 1
         except:
            input_found = 0
            if (i < 28 ):
               print("Don't have ",i)
               cnt+=1
         
         if (input_found ==1):
            header = telematics_csv.next()
         
            if (i==1 ):
               output_csv.writerow(['driver_trip','prob'])
         
            cnt1 = 0
            for row in telematics_csv:
              output_csv.writerow(row)
              cnt1 += 1
           
            if (cnt1 != 20000 and i != 28):
               print(" Not Finished ",i)
               
            #print("Finished Combining Block ",i, j)  
           
   
   print(" total not found ",cnt)
   output_file.close()
   return 
   




   
combined_file = os.path.join(MODELS,"RF_Telematics_results_Forest_featureset3.csv")
break_input_file_features(combined_file)  

print 'Combined output written to\n\t', MODELS, '\n\n'