import numpy as np
from random import sample
import os
import sys
import time
import csv

from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestClassifier

from modules_janto.paths import *

print "\n\nTraining model on feature set 2...\n\n"
blockresults = os.path.join(FEATURES,"blocks","results")
blockfeatures = os.path.join(FEATURES,"blocks","features")

def import_features(feature_file):


   feature_input = open(feature_file,'rb')
   feature_csv = csv.reader(feature_input)
   
   #header = feature_csv.next()

   features = []
   for row in feature_csv:
   
      features.append(row)
     
   features = np.array(features, dtype = np.float32)   # make a numpy array from teh feature list
   
   
   feature_input.close()


   return features
   


def Gradient_Regression(training_data,  training_labels, test_data):

   #regression1 = RandomForestClassifier(n_estimators=550, max_depth=15)
   regression1 = RandomForestClassifier(n_estimators=500, max_depth=11)
   
   
   #regression1 = GradientBoostingRegressor(n_estimators=100, max_depth=4)
   regression1.fit(training_data, training_labels)
   results = regression1.predict_proba(test_data)
   
   return results
   
   


def make_training_set(feature_file, driver_id):


   feature_input = open(feature_file,'rb')
   feature_csv = csv.reader(feature_input)
   
   header = feature_csv.next()

   training_set = []
   for row in feature_csv:
      if (driver_id ==0):   # if it is the generate training set, import routes number 5 and 110 for each driver
         
         #if( int(float(row[1])) < 1000):
            #if( int(float(row[2])) == 5 or int(float(row[2])) == 110  or int(float(row[2])) == 115  or int(float(row[2])) == 120 or int(float(row[2])) == 125 or int(float(row[2])) == 130):
            if( int(float(row[1])) == 5 or int(float(row[1])) == 110  or int(float(row[1])) == 151 ):              
               training_set.append(row)
         #else:
         #   break
      
      
      elif (driver_id > 0):
         if( int(float(row[0])) == driver_id):  # if it is the test set, import all for that driver
            training_set.append(row)
            
   #training_file = open('Tai_and_Janto_Training_features.csv','wb')            
   #training_csv = csv.writer(training_file)
   #for row in training_set:
   #   training_csv.writerow(row)
      
   #sys.exit()
     
   training_set = np.array(training_set, dtype = np.float32)   # make a numpy array from teh feature list

   feature_input.close()

   return training_set







def Main_Regression():


   print ("making the set of drivers that don't match")
   
   feature_file = "featurematrix2.csv"   
   training_set = make_training_set(feature_file, 0)  
   
   
   
   
   print ("finished the set of drivers that don't match")
   print (" total ",len(training_set)," routes")
   
   
   

   
   data_blocks = [1,2,3,4,5,6,7,8,9,10,11,12,23,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28]
   
   subset_range = [1,2,3,4,5,6,7,8,9,10]
   
   #data_blocks = [1]
   #subset_range=[1]
   
   
   for data_block in data_blocks:   # loop through this many blocks of drivers
   
   
   
      print "Making test set for data block ",data_block, "\n\n"  
         
      feature_file = os.path.join(blockfeatures,"Scott_features_block_" + str(data_block) + ".csv")
      features = import_features(feature_file)  
      
      print "-- Finished making test set for data block ",data_block
      
      
      
      drivers = features[:,0]       # drivers in the file
      drivers = np.unique(drivers)
      print "\nThere are ",len(drivers)," different drivers\n"
      
      
      
      for cnt, driver in enumerate(drivers):

         if (cnt%10 == 0):
            if (cnt!= 0):
               try: 
                  telematics_file.close()
               except:
                  pass
               
            
            subset1 = int(cnt/10) + 1
            
            
            if (subset1 in subset_range):
               telematics_file = open(os.path.join(blockresults,"Telematics_results_Scott_features_Run1_block_"+str(data_block)+ "_subset_"+str(subset1)+".csv"),'wb')
               telematics_csv = csv.writer(telematics_file)
               telematics_csv.writerow(['driver','trip_prob'])     

         if (subset1 in subset_range):
            for i in range(1,9):
               start_time = time.time()
            
               print "Starting Forest for driver ",driver
               
            
               start_num = (i-1)*25
               end_num = i*25
            
               test_block =  features[  np.where(features[:,0] == driver)[0], 2:]  # these are all the features
               
               test_data = test_block[start_num:end_num,:]
               
               if(i==1):
                  test_data2 = test_block[end_num+1 :, :]
               elif(i==10):
                  test_data2 = test_block[ : start_num, :]
               else:   
                  test_data3 = test_block[ : start_num, :]
                  test_data4 = test_block[end_num+1 :, :]
                  test_data2 = np.concatenate((test_data3,test_data4), axis=0) 
               
               
               driver_id = driver
               
               #print (len(training_set), len(np.where(training_set[:,1] != driver)[0]) )
               training_data = training_set[ np.where(training_set[:,0] != driver)[0],2:]
               
               #print(test_data.shape, training_data.shape )
               joined_training_data = np.concatenate((test_data2,training_data), axis=0)   
               #print( joined_training_data.shape )
               #sys.exit(0)
               
               
               training_labels = np.zeros(len(joined_training_data), dtype = np.float32 )
               for x in range(0,175):
                  training_labels[x] = 1.0
               
               
               results = Gradient_Regression(joined_training_data,  training_labels, test_data)
               
               for cnt2, result in enumerate(results):
                  telematics_csv.writerow([str(int(driver)) + "_" + str(cnt2+start_num + 1), result[1]])
               #print results
               
               end_time = time.time()
               print "\telapsed time ",end_time - start_time
               print
               
               telematics_file.flush()
            
      telematics_file.close()
      print"\n******************Finished block ***************\n",data_block
      

Main_Regression()      