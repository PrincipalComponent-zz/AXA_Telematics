import csv
import os
import sys
import time
import string

import numpy as np
import matplotlib.pyplot as plt
from file_paths import *


def getkey(item):
   brk = string.split(item[0],'_')
   return brk[0]

def getkey_route(item):
   brk = string.split(item[0],'_')
   return int(brk[1])


def secondvalue(item):
   return item[1]

def thirdvalue(item):
   return item[2]



# read the input files
def read_results_file(file_name):

    file_path = os.path.join(MODELS,file_name)
    
    file_open = open(file_path,'rb')

    file_csv = csv.reader(file_open)
    
    results =[]
    header = file_csv.next()
    
    for row in file_csv:
       if (len(row) ==2):
          results.append( [ row[0], float(row[1]), 0.0 ] )
       else:
          results.append( [ row[0], float(row[1]), float(row[2]) ] )
          
    file_open.close()
    
    return header,results
    
    
    
    
    
    
# write the result file
def write_results_file(header,results,output_file_name):
    file_open = open(output_file_name,'wb')
    file_csv = csv.writer(file_open)
    

    file_csv.writerow(header)
    
    for row in results:
       file_csv.writerow(row)
       
    file_open.close()
    return
    








# call this re-sort and renormalize every so often so we don't run into numeric problems with 
# trying to interpolate between numbers that are too close
def sort_telematics_values( telematics_only_results):

    # sort the telematics results on their score
    telematics_only_results   = sorted(telematics_only_results , key=secondvalue)  # sort by telematics score

    sorted_score = 0.
    increment = 1
    for cnt in range(0,len(telematics_only_results)):
        telematics_only_results[cnt][1] = sorted_score  # enumerate on the telematics scores
        sorted_score += increment   

    return  telematics_only_results













print("Doing Adjust telematics solution & combine with path solution")

    
    
header,telematics_Run1 = read_results_file('RF_Telematics_results_Forest_featureset3.csv')
header,telematics_Run2 = read_results_file('ensembleLRRF.csv')
header,telematics_Run3 = read_results_file('Telematics_results_GBM_featureset3.csv')
header,telematics_Run4 = read_results_file('Telematics_results_Tai_and_Janto_Run2_combined.csv')
header,telematics_andrei = read_results_file('R_Probabilities.csv')
header,telematics_scott = read_results_file('Telematics_results_Scott_features_Run1_combined.csv')



#  sort the values by score
telematics_Run1   = sort_telematics_values(telematics_Run1)
telematics_Run2   = sort_telematics_values(telematics_Run2)
telematics_Run3   = sort_telematics_values(telematics_Run3)
telematics_Run4   = sort_telematics_values(telematics_Run4)
telematics_andrei   = sort_telematics_values(telematics_andrei)
telematics_scott   = sort_telematics_values(telematics_scott)


# now sort back by driver and route
telematics_Run1   = sorted(telematics_Run1, key=getkey_route)
telematics_Run2   = sorted(telematics_Run2, key=getkey_route)
telematics_Run3   = sorted(telematics_Run3, key=getkey_route)
telematics_Run4   = sorted(telematics_Run4, key=getkey_route)
telematics_andrei   = sorted(telematics_andrei, key=getkey_route)
telematics_scott   = sorted(telematics_scott, key=getkey_route)

telematics_Run1   = sorted(telematics_Run1, key=getkey)
telematics_Run2   = sorted(telematics_Run2, key=getkey)
telematics_Run3   = sorted(telematics_Run3, key=getkey)
telematics_Run4   = sorted(telematics_Run4, key=getkey)
telematics_andrei   = sorted(telematics_andrei, key=getkey)
telematics_scott   = sorted(telematics_scott, key=getkey)


# average the score
combined_score = []
for cnt, score in enumerate(telematics_Run1):
   driver = telematics_Run1[cnt][0]
   average_score = telematics_Run3[cnt][1] * .42 + telematics_Run1[cnt][1] * .27 + telematics_Run2[cnt][1] * .16 + telematics_Run4[cnt][1] * .2 + telematics_andrei[cnt][1] * .20  +  telematics_scott[cnt][1] * .16  
   combined_score.append([driver, average_score])


combined_score   = sort_telematics_values(combined_score)      # sort and normalize the score
combined_score   = sorted(combined_score, key=getkey_route)  # sort on the route id
combined_score   = sorted(combined_score, key=getkey)        # sort on the driver



write_results_file(header,combined_score,'Telematics_Results_combined.csv')


print("Finish Adjust telematics solution & combine with path solution")