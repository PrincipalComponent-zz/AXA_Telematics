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
    file_open = open(file_name,'rb')
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
    

#  normalize the value range to go from zero to 1
def normalize_values(results):

    max_value = -1000
    min_value = 1000

    # find the max and min
    for row in results:
       value = row[1]
       max_value = max(max_value,value)
       min_value = min(min_value,value)

    # normalize to zero    
    for cnt in xrange(0,len(results)):
       results[cnt][1] = results[cnt][1] - min_value
    
    # normalize max_value to zero
    max_value = max_value - min_value   
    
    # normalize to max of 100
    for cnt in xrange(0,len(results)):
       results[cnt][1] = results[cnt][1] / max_value * 100


    return(results)
    






# keep the path solution if it is a 1, otherwise use the telematics solution
#@profile
def combine_results(path_solution, telematics_solution):

    driver_list=[]
    for driver in telematics_solution:
       driver_list.append(driver[0])



    combined_results = []
    # these are the ordered path scores
    for path_value in path_solution:
       driver = path_value[0]
       score = path_value[1]
       combined_results.append([driver,score])

    # add in the adjusted telematics scores
    for telematics_value in telematics_solution:
       driver = telematics_value[0]
       score = telematics_value[1]
       combined_results.append([driver,score])


    combined_results       = sorted(combined_results, key=getkey_route)  # sort on the route id
    combined_results       = sorted(combined_results, key=getkey)  # sort on the driver
    
    return combined_results








# keep the path solution if it is a 1, otherwise use the telematics solution
def sort_path_matches(path_solution, telematics_solution):


    sorted_path_results = []
    
    telematics_only_results = []
    driver_list=[]
    for driver in telematics_solution:
       driver_list.append(driver[0])    
    
    for cnt,path_value in enumerate(path_solution):
    
       driver = path_value[0]
       score = path_value[1]


       if (driver == driver_list[cnt]):  # if the telematics and path solution are sorted the same
           telematics_score = telematics_solution[cnt][1]
       else:  # search for the telematics score    
           index1 = driver_list.index(driver)
           telematics_score = telematics_solution[index1][1]

       if (score >=1):   # if the path score is above a 1, remember it
           sorted_path_results.append([driver,score,telematics_score])
       else:  # otherwise use the telematics results
           telematics_only_results.append([driver,telematics_score])
          

    # this sorting will make a route that matches 2 other routes higher ranked than a route that matches 1 other route
    # and a route that matches 3 higher than any of them.  However if there are two route that match 1 other route
    # for instance than their ranking will be driven by the telematics score
    sorted_path_results       = sorted(sorted_path_results , key=thirdvalue)   # first sort by the telematics score
    sorted_path_results       = sorted(sorted_path_results , key=secondvalue)  # then sort by the number of matches found
    
    sorted_score = 100.
    increment = .0001
    for cnt in range(0,len(sorted_path_results)):
        if (sorted_path_results[cnt][1] >=1):
           sorted_path_results[cnt][1] = sorted_score  # this ensures that no two path results have the same score
           sorted_score += increment              # the ones that would are instead sorted by the telematics method


    # sort the telematics results on their score
    telematics_only_results   = sorted(telematics_only_results , key=secondvalue)  # sort by telematics score

    sorted_score = 0.
    increment = .0001
    for cnt in range(0,len(telematics_only_results)):
        telematics_only_results[cnt][1] = sorted_score  # enumerate on the telematics scores
        sorted_score += increment             

    
    
    telematics_only_results = sorted(telematics_only_results , key=secondvalue)# first sort by the telematics score
    
    return sorted_path_results, telematics_only_results




# call this re-sort and renormalize every so often so we don't run into numeric problems with 
# trying to interpolate between numbers that are too close
def sort_telematics_values( telematics_only_results):

    # sort the telematics results on their score
    telematics_only_results   = sorted(telematics_only_results , key=secondvalue)  # sort by telematics score

    sorted_score = 0.
    increment = .0001
    for cnt in range(0,len(telematics_only_results)):
        telematics_only_results[cnt][1] = sorted_score  # enumerate on the telematics scores
        sorted_score += increment   

    return  telematics_only_results




# adjust the scores in the telematics solution based on the adjust scores list
#@profile
def adjust_telematics_scores(telematics_solution, adjust_score):

    driver_list=[]
    driver_only_list = []
    driver_num =0
    for driver in telematics_solution:
       driver_list.append(driver[0])  
       driver_id =  int(string.split(driver[0],'_')[0])
       if (driver_id != driver_num):
          driver_num = driver_id
          driver_only_list.append(driver_num)
          
       

    num_telematics = len(telematics_solution)

    for cnt in range(0,len(adjust_score)):
    
       if (cnt%600 ==0):
          print("number of adjustments made ",cnt," out of ",len(adjust_score))
    
       driver= adjust_score[cnt][0]   # see if the driver is in this list and not the path solution
       driver_found = 0
       try:
          
          #driver_id =  int(string.split(driver[0],'_')[0])
          #route_id =  int(string.split(driver[0],'_')[1])
          #index0 = driver_only_list.index(driver_id)
          #index1 = driver_id * 200 + (route_id -1)
          #
          #if (driver_list[index1] != driver):  # if the matching didn't work
          
          index1 = driver_list.index(driver)      
          driver_found=1
       except:
          driver_found = 0
          pass

       if (driver_found ==1):
       
           if (adjust_score[cnt][1] > 0.0000001 or adjust_score[cnt][1] < -0.0000001):  # move up or down a percentage
              target_spot = index1 + int(num_telematics * adjust_score[cnt][1] / 100 )
           elif (adjust_score[cnt][2] > 0):  # move to a desired percentage
              target_spot = int(num_telematics * adjust_score[cnt][2] / 100 )
           else:  # otherwise don't move
              target_spot = index1
          
          
           # see if we are at the top or bottom of the list,  and also get the new score
           if (target_spot < 0):  # put it in the first spot
              target_spot = 0
              telematics_solution[index1][1] = telematics_solution[target_spot][1] - .0001
           elif (target_spot > num_telematics-1):  # put it in the last spot
              target_spot = num_telematics-1
              telematics_solution[index1][1] = telematics_solution[target_spot][1] + .0001
           else:  # take the average of the before and after spots
              telematics_solution[index1][1] = (telematics_solution[target_spot-1][1] + telematics_solution[target_spot][1]) / 2.0
              
              
           if (target_spot > index1):
              moving_spot = telematics_solution[index1]
              telematics_solution.insert(target_spot,moving_spot)  #  insert the new score into the right position
              telematics_solution.pop(index1)  # remove the old score
              
              moving_driver = driver_list[index1]
              driver_list.insert(target_spot, moving_driver)#  insert the driver into the right position
              driver_list.pop(index1)  # remove the old driver

           elif (target_spot < index1):  # do it in the other order so the list indices don't get messed up.
              moving_spot = telematics_solution[index1]
              telematics_solution.pop(index1)  # remove the old score
              telematics_solution.insert(target_spot,moving_spot)  #  insert the new score into the right position
              
              moving_driver = driver_list[index1]
              driver_list.pop(index1)  # remove the old driver           
              driver_list.insert(target_spot, moving_driver)#  insert the driver into the right position
              
          
       if (cnt%200 ==0):
          # resort every so often to make sure errors don't propagate
          telematics_solution = sort_telematics_values( telematics_solution)
          driver_list=[]
          for driver in telematics_solution:
              driver_list.append(driver[0]) 
          
          

    return telematics_solution 












print("Doing Adjust telematics solution & combine with path solution")

    
    
header,path_solution = read_results_file('Current_Best_Path_Solution.csv')
header,telematics_solution = read_results_file('Telematics_results_combined.csv')


header2,adjust_score = read_results_file('Adjust_Score.csv')



path_solution       = sorted(path_solution, key=getkey)
telematics_solution = sorted(telematics_solution, key=getkey)


adjust_score       = sorted(adjust_score, key=getkey_route)  # sort on the route id
adjust_score       = sorted(adjust_score, key=getkey)        # sort on the driver


print("here1*********")

path_solution, telematics_solution = sort_path_matches(path_solution,telematics_solution)

print("here3*********")

path_solution       = sorted(path_solution, key=getkey_route)  # sort on the route id
path_solution       = sorted(path_solution, key=getkey)  # sort on the driver



# adjust the scores in the telematics solution based on the adjust scores list
telematics_solution = adjust_telematics_scores(telematics_solution, adjust_score)



print("here4*********")

combined_results = combine_results(path_solution,telematics_solution)

print("here5*********")

#write_results_file(header,path_solution,'test_path.csv')
#write_results_file(header,telematics_solution,'test_telematics.csv')

write_results_file(header,combined_results,'combined_results.csv')


print("Finish Adjust telematics solution & combine with path solution")