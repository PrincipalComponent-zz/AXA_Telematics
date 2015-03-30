import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from random import sample
import os
import sys
import time
import csv

from modules_janto.paths import *

print '\nBreaking up feature set 1 and 3 (combined) into blocks...\n'

blockFolder = os.path.join(FEATURES,"blocks")

def break_input_file_features(feature_file):


   cnt = 0
   cnt2 = 1
   current_driver = 0
   output_file = open(os.path.join(blockFolder,'features',"Tai_and_Janto_features_block_" + str(cnt2) + ".csv"), 'wb')
   output_csv = csv.writer(output_file)
   cnt2 = 0

 


   feature_input = open(feature_file,'rb')
   feature_csv = csv.reader(feature_input)
   
   #header = feature_csv.next()

   for row in feature_csv:
     csv_driver = int(float(row[1]))
     if( csv_driver != current_driver):
        current_driver = csv_driver
        cnt += 1
        print "Processing driver...",current_driver
        
        #if (cnt == 150):
        #   sys.exit()
        
        if (cnt % 100 == 1):
           cnt2 +=1
           output_file.close()
           output_file = open(os.path.join(blockFolder,'features',"Tai_and_Janto_features_block_" + str(cnt2) + ".csv"), 'wb')
           output_csv = csv.writer(output_file) 
           #output_csv.writerow(header)

     for cnt3, item in enumerate(row):
        if ( 'nan' in row[cnt3] ):
           row[cnt3] = 0.
        else:
           row[cnt3] = float(row[cnt3])
     
     output_csv.writerow( row)
          


   output_file.close()
   return 
   




   
feature_file = "featureset1and3_combined.csv"   
break_input_file_features(feature_file)  
