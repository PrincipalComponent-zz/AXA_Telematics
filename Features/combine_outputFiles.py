import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from random import sample
import os
import sys
import time
import csv

from modules_janto.paths import *

print "\n\nCombining outputs of model trained on feature set 2...\n\n"
blockresults = os.path.join(FEATURES,"blocks","results")


def break_input_file_features(combined_file):


   output_file = open(combined_file, 'wb')
   output_csv = csv.writer(output_file)

   cnt=0

   for i in range(1,29):
   
      for j in range(1,11):

         input_found = 0
         try:
            telematics_input = open(os.path.join(blockresults,"Telematics_results_Scott_features_Run1_block_" + str(i) +"_subset_"+str(j)+".csv"),'rU')
            telematics_csv = csv.reader(telematics_input)
            input_found = 1
         except:
            input_found = 0
            if (i < 28 or j <=4):
               #print("Don't have ",i,j)
               cnt+=1
         
         if (input_found ==1):
            header = telematics_csv.next()
         
            if (i==1 and j==1):
               output_csv.writerow(['driver_trip','prob'])
         
            cnt1 = 0
            for row in telematics_csv:
              output_csv.writerow(row)
              cnt1 += 1
           
            if (cnt1 != 2000 and i!=28):
               print(" Not Finished ",i,j)
               
            #print("Finished Combining Block ",i, j)  
           
   
   print " Total outputs not found ",cnt
   print "Model output has been written to \n\t\t", MODELS
   output_file.close()
   return 
   




   
combined_file = os.path.join(MODELS,"Telematics_results_Scott_features_Run1_combined.csv")
break_input_file_features(combined_file)  
