import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier
from random import sample
import os
import sys
import time
import csv

from modules_janto.paths import *

print '\nCombining feature set 1 and feature set 3 in one matrix...\n\n'

combined_file = open("featureset1and3_combined.csv",'wb')
combined_csv = csv.writer(combined_file)

      
tai_input_file = open(os.path.join(FEATURES,'featurematrix3.csv'),'rb')
tai_input_csv = csv.reader(tai_input_file)
header = tai_input_csv.next()

# convert featurematrix1 to .csv
featmat = np.load(os.path.join(FEATURES,'featurematrix1.npy'))
np.savetxt("featurematrix1.csv", featmat, delimiter=",")
input_file = open(os.path.join(FEATURES,"featurematrix1.csv"),'rb')
input_csv = csv.reader(input_file)

tai_routes = []
tai_features = []
for row in tai_input_csv:
   route_num = int(float(row[2]))
   driver_num = int(float(row[1]))
   
   #tai_routes.append([driver_num,route_num])
   #tai_features.append(row)

   janto_feature = input_csv.next()
   
   combined_features = row
   for cnt2 in range(2, len( janto_feature ) ):
      combined_features.append( janto_feature[cnt2] )   


   for cnt3, item in enumerate(combined_features):
     if ( 'nan' in combined_features[cnt3] ):
        combined_features[cnt3] = 0.
     else:
        combined_features[cnt3] = float(combined_features[cnt3])

   combined_csv.writerow(combined_features)

   #sys.exit()