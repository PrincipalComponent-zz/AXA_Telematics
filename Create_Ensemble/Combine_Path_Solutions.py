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


def getkey2(item):
   
   brk = string.split(item[0],'_')
   return int(brk[1])




# read the input files
def read_results_file(file_name):
    
    file_path = os.path.join(MODELS,file_name)
    
    file_open = open(file_path,'rb')
    file_csv = csv.reader(file_open)
    
    results =[]
    header = file_csv.next()
    
    for row in file_csv:
       results.append( [ row[0], float(row[1]) ] )
       
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
    


# keep the path solution if it is a 1, otherwise use the telematics solution
def combine_path_results(path_solution13,path_solution15,path_solution17,adjust_csv,path_solution7_New,path_solution8_New,  path_solution9_New, path_solution10_New, path_solution11_New, path_solution12_New, path_solution13_New, path_solution14_New, path_solution15_New, path_solution17_New, path_solution19_New, path_solution21_New, path_solution25_New, path_solution30_New, path_solution35_New,  jitter_results):


    #current_single_file = open("Current_Single_Matches.csv",'wb')
    #current_single_csv = csv.writer(current_single_file)


    combined_results = []
    found_count = 0
    found_count_high_score = 0
    found_count5 = 0
    counting=0
    counting2=0
    counting3=0
    counting4 = 0
    counting5 = 0
    counting6 = 0
    counting7 = 0
    counting8 = 0
    counting9 = 0
    counting10 = 0
    counting11 = 0
    counting12 = 0
    counting13 = 0
    counting14 = 0
    
    new_found_count = 0
    for cnt,path_value in enumerate(path_solution13):
       driver = path_value[0]
       score13 = float(path_solution13[cnt][1])
       
       score15 = float(path_solution15[cnt][1])
       score17 = float(path_solution17[cnt][1])

       score7_New = float(path_solution7_New[cnt][1])
       score8_New = float(path_solution7_New[cnt][1])
       score9_New = float(path_solution9_New[cnt][1])
       score10_New = float(path_solution10_New[cnt][1])
       score11_New = float(path_solution11_New[cnt][1])
       score12_New = float(path_solution12_New[cnt][1])
       score13_New = float(path_solution13_New[cnt][1])
       score14_New = float(path_solution14_New[cnt][1])       
       score15_New = float(path_solution15_New[cnt][1])
       score17_New = float(path_solution17_New[cnt][1])
       score19_New = float(path_solution19_New[cnt][1])
       score21_New = float(path_solution21_New[cnt][1])
       score25_New = float(path_solution25_New[cnt][1])
       score30_New = float(path_solution30_New[cnt][1])
       score35_New = float(path_solution35_New[cnt][1])
       
       #second_path_run_score = float(second_path_run[cnt][1])
       jitter_score =  float(jitter_results[cnt][1])  

       
       total_found = 0
       if (score13 > 0):
          total_found +=1
       if (score15 > 0):
          total_found +=1
       if (score17 > 0):
          total_found +=1

       new_found_num = 0

       total_found_new = 0
       #if (score7_New > 0):
       #   total_found_new +=1
       if (score9_New > 0):
          total_found_new +=1
          new_found_num = 9
       if (score10_New > 0):
          total_found_new +=1
          new_found_num = 10
       if (score11_New > 0):
          total_found_new +=1
          new_found_num = 11
       if (score12_New > 0):
          total_found_new +=1
          new_found_num = 12
       if (score13_New > 0):
          total_found_new +=1
          new_found_num = 13
       if (score14_New > 0):
          total_found_new +=1
          new_found_num = 14
       if (score15_New > 0):
          total_found_new +=1
          new_found_num = 15
       if (score17_New > 0):
          total_found_new +=1  
          new_found_num = 17
       if (score19_New > 0):
          total_found_new +=1           
          new_found_num = 19
       if (score21_New > 0):
          total_found_new +=1           
          new_found_num = 21    
       if (score25_New > 0):
          total_found_new +=1           
          new_found_num = 25            
       if (score30_New > 0):
          total_found_new +=1           
          new_found_num = 30 
       if (score35_New > 0):
          total_found_new +=1           
          new_found_num = 35           
       
       max_score = max(score13,score15,score17)
       min_score = min(score13,score15,score17)
       

       max_score_new = max(score9_New,score10_New,score11_New,score12_New,score13_New,score14_New,score15_New,score17_New,score19_New,score21_New,score25_New,score30_New,score35_New)
       min_score_new = min(score9_New,score10_New,score11_New,score12_New,score13_New,score14_New,score15_New,score17_New)

       
       #if (max_score_new >= 2 and second_path_run_score >=1):
       #   max_score_new += 2
       #if (max_score >= 2 and second_path_run_score >=1):
       #   max_score     += 2
          
       if (min_score >= 1 and max_score >=2):   # if it is a match on every trip, bump it up more
          max_score += 3
       if (min_score_new >=1 and max_score_new >=2):
          max_score_new +=3

       
       if ( max_score >=2):   # if there are two matches or a max score of at least 2, count it
          combined_results.append([driver,max_score])
          found_count_high_score +=1
       elif( max_score_new >= 2 ):   # look in the new runs for matches more than 2
          combined_results.append([driver,max_score_new])
          new_found_count +=1       
          
       #elif (min_score >=1.0 and min_score_new >=1.0  and second_path_run_score >= 1.0 ):   # if there are two matches or a max score of at least 2, count it
       #   combined_results.append([driver,1.7])
       #   found_count5 +=1


       elif (min_score >=1.0 and min_score_new >=1.0 ):   # if there are two matches or a max score of at least 2, count it
          combined_results.append([driver,1.5])
          found_count5 +=1

       #elif (max_score_new >= 1.0 and second_path_run_score >= 1.0):
       #   combined_results.append([driver,1.2])
       #   counting10 += 1.0
          
       elif (score7_New >= 4.0 or score8_New >= 3.0):
          combined_results.append([driver,1.0])
          counting13 +=1

       else:   
               

           if ( min_score_new >=1   or total_found_new >= 8 ):
               adjust_csv.writerow([driver,75,0])  # if it matched for any tolerance, move up 15 percent
               counting5 +=1    

           elif (total_found >=2 ):   # if there are two matches or a max score of at least 2, count it
               #combined_results.append([driver,1.0])
               adjust_csv.writerow([driver,40,0])  # if it matched for any tolerance, move up 15 percent
               found_count +=1

           elif ( max_score_new >=1 and total_found_new >=3):
               adjust_csv.writerow([driver,30,0])  # if it matched for any tolerance, move up 15 percent
               counting11 +=1   

           elif ( max_score_new >=1 and total_found_new >=2 ):
               adjust_csv.writerow([driver,10,0])  # if it matched for any tolerance, move up 15 percent
               counting4 +=1   


           elif ( max_score_new >=1 ):
               adjust_csv.writerow([driver,1,0])  # if it matched for any tolerance, move up 15 percent
               counting12 +=1   
               #current_single_csv.writerow([driver,1.0,new_found_num])



           #elif ( max_score >=1 ):
           #    adjust_csv.writerow([driver,40,0])  # if it matched for any tolerance, move up 15 percent
           #    counting2 +=1           
 

           elif (  (max_score_new == -11 or max_score_new == -12 or max_score_new == -13  or max_score_new == -14  or max_score_new == -15  or max_score_new == -16) and max_score <=0):
               counting3 += 1
               adjust_csv.writerow([driver,-75,0])  # these are the routes that don't match anything, move them down 25 percent


           elif ( (min_score_new == -11 or min_score_new== -12 or min_score_new== -13 or min_score_new== -14 ) and max_score <=0 and max_score_new <=0):
               adjust_csv.writerow([driver,-45,0])  # if these routes weren't a match, move them down 10 percent
               counting6+=1    

           elif ( ( min_score_new== -1 or min_score_new== -2 or min_score_new== -3 or min_score_new== -4) and max_score <=0 and max_score_new <=0):
               adjust_csv.writerow([driver,-35,0])  # if these routes weren't a match, move them down 10 percent
               counting6+=1    

           elif (min_score <= -1  and max_score <=0 and max_score_new <=0):
               adjust_csv.writerow([driver,-30,0])  # if these routes weren't a match, move them down 10 percent
               counting+=1


           elif ( (min_score_new == -15 or min_score_new== -16 or min_score_new== -17 or min_score_new== -5 or min_score_new== -6 or min_score_new== -7 ) and max_score <=0 and max_score_new <=0):
               adjust_csv.writerow([driver,-30,0])  # if these routes weren't a match, move them down 10 percent
               counting7+=1    
           elif ( (min_score_new == -18 or min_score_new== -19 or min_score_new== -8 or min_score_new== -9  ) and max_score <=0 and max_score_new <=0):
               adjust_csv.writerow([driver,-25,0])  # if these routes weren't a match, move them down 10 percent
               counting8+=1               
           elif ( (  abs(min_score_new - (-19.5)) < .001 or abs(min_score_new - (-19.7)) < .001 or abs(min_score_new - (-9.5)) < .001 or abs(min_score_new - (-9.7)) < .001 ) and max_score <=0 and max_score_new <=0):
               adjust_csv.writerow([driver,-25,0])  # if these routes weren't a match, move them down 10 percent
               counting9+=1               
           elif ( max_score_new == 0 and min_score_new ==0 and jitter_score==0 ):
               adjust_csv.writerow([driver,3,0])  # move these h
               counting14+=1   


           combined_results.append([driver,0])

    
    print ("there were ",found_count_high_score," matches found scoring 2 or more")
    print ("there were ",new_found_count," matches found from the new runs scoring 2 or more")
    print ("there were ",found_count5," matches found matching all runs")
    print ("there were ",counting10," matches found from Scott & Tai's path runs")
    print ("there were ",counting13," matches found from the short RDP rus")
    print
    print ("there were ",counting5," matches found matching all or all but 1 new runs")
    print ("there were ",found_count," matches found matching at least 2 runs and adjusted up")
    print
    print("there were ",counting2," matched for a single RDP tolerance and moved up")
    print("there were ",counting11," matched for 3 or more of the new RDP tolerances and moved up")
    print("there were ",counting4," matched for 2 new RDP tolerances and moved up")
    print("there were ",counting12," matched for 1 new RDP tolerances and moved up")
    print("there were ",counting14,"short runs moved up")
    print
    print("there were ",counting," moved down based on old runs")
    print("there were ",counting6," moved down based on new runs")
    print("there were ",counting7," moved down less amount based on new runs")
    print("there were ",counting8," moved down even less amount based on new runs")
    print("there were ",counting9," moved down even even less amount based on new runs")
    print("there were ",counting3," moved down a lot")    


    return combined_results
    
    
    


#  process the jitter results to make the adjustment file
def process_jitter_results(jitter_results,adjust_csv):    

    for jitter in jitter_results:
        jitter_count = jitter[1]
        write_result = 0


        if (jitter_count >= 25):
           write_result = 1
           percentile = 99.0    # this is what percentile to put this jitter result        
        if (jitter_count >= 12):
           write_result = 1
           percentile = 95.0000   # this is what percentile to put this jitter result        
        if (jitter_count >= 10):
           write_result = 1
           percentile = 90.0000   # this is what percentile to put this jitter result        
        elif (jitter_count >= 6):
           write_result = 1
           percentile = 82.0   # this is what percentile to put this jitter result
        elif (jitter_count >= 3):
           write_result = 1
           percentile = 60.0000   # this is what percentile to put this jitter result
        elif (jitter_count >= 1):
           write_result = 1
           percentile = 50.0000   # this is what percentile to put this jitter result        
        
        if (write_result ==1):
           adjust_csv.writerow([jitter[0],0,percentile])

    
    return
    
    




#  process the hyperspace results to make the adjustment file
def process_hyperspace_results(hyperspace_results,adjust_csv):    

    hyper_count = 0

    for hyperspace in hyperspace_results:
        hyperspace_count = hyperspace[1]
        write_result = 0

        if (hyperspace_count >= 15):
           write_result = 1
           percentile = 15.0   # move up this percent  
           hyper_count +=1
      
        
        if (write_result ==1):
           adjust_csv.writerow([hyperspace[0],percentile,0])


    print("there were ",hyper_count," adjustments made for hyperspace jumps, less however many are already included in the PATH solution")
    
    return
    
    
    





    
    

tolerance_list = [13, 15, 17, 19]

print("Doing combine path solutions")

    
header,path_solution13 = read_results_file('Final_Results_13m.csv')
header,path_solution15 = read_results_file('Final_Results_15m.csv')
header,path_solution17 = read_results_file('Final_Results_17m.csv')


path_solution13       = sorted(path_solution13, key=getkey2)
path_solution15       = sorted(path_solution15, key=getkey2)
path_solution17       = sorted(path_solution17, key=getkey2)


path_solution13       = sorted(path_solution13, key=getkey)
path_solution15       = sorted(path_solution15, key=getkey)
path_solution17       = sorted(path_solution17, key=getkey)


header2,path_solution7_New = read_results_file('Final_Results_7m_New.csv')
header2,path_solution8_New = read_results_file('Final_Results_8m_New.csv')
header2,path_solution9_New = read_results_file('Final_Results_9m_New.csv')
header2,path_solution10_New = read_results_file('Final_Results_10m_New.csv')
header2,path_solution11_New = read_results_file('Final_Results_11m_New.csv')
header2,path_solution12_New = read_results_file('Final_Results_12m_New.csv')
header2,path_solution13_New = read_results_file('Final_Results_13m_New.csv')
header2,path_solution14_New = read_results_file('Final_Results_14m_New.csv')
header2,path_solution15_New = read_results_file('Final_Results_15m_New.csv')
header2,path_solution17_New = read_results_file('Final_Results_17m_New.csv')
header2,path_solution19_New = read_results_file('Final_Results_19m_New.csv')
header2,path_solution21_New = read_results_file('Final_Results_21m_New.csv')
header2,path_solution25_New = read_results_file('Final_Results_25m_New.csv')
header2,path_solution30_New = read_results_file('Final_Results_30m_New.csv')
header2,path_solution35_New = read_results_file('Final_Results_35m_New.csv')

path_solution7_New       = sorted(path_solution7_New, key=getkey2)
path_solution8_New       = sorted(path_solution8_New, key=getkey2)
path_solution9_New       = sorted(path_solution9_New, key=getkey2)
path_solution10_New       = sorted(path_solution10_New, key=getkey2)
path_solution11_New       = sorted(path_solution11_New, key=getkey2)
path_solution12_New       = sorted(path_solution12_New, key=getkey2)
path_solution13_New       = sorted(path_solution13_New, key=getkey2)
path_solution14_New       = sorted(path_solution14_New, key=getkey2)
path_solution15_New       = sorted(path_solution15_New, key=getkey2)
path_solution17_New       = sorted(path_solution17_New, key=getkey2)
path_solution19_New       = sorted(path_solution19_New, key=getkey2)
path_solution21_New       = sorted(path_solution21_New, key=getkey2)
path_solution25_New       = sorted(path_solution25_New, key=getkey2)
path_solution30_New       = sorted(path_solution30_New, key=getkey2)
path_solution35_New       = sorted(path_solution35_New, key=getkey2)


path_solution7_New       = sorted(path_solution7_New, key=getkey)
path_solution8_New       = sorted(path_solution8_New, key=getkey)
path_solution9_New       = sorted(path_solution9_New, key=getkey)
path_solution10_New       = sorted(path_solution10_New, key=getkey)
path_solution11_New       = sorted(path_solution11_New, key=getkey)
path_solution12_New       = sorted(path_solution12_New, key=getkey)
path_solution13_New       = sorted(path_solution13_New, key=getkey)
path_solution14_New       = sorted(path_solution14_New, key=getkey)
path_solution15_New       = sorted(path_solution15_New, key=getkey)
path_solution17_New       = sorted(path_solution17_New, key=getkey)
path_solution19_New       = sorted(path_solution19_New, key=getkey)
path_solution21_New       = sorted(path_solution21_New, key=getkey)
path_solution25_New       = sorted(path_solution25_New, key=getkey)
path_solution30_New       = sorted(path_solution30_New, key=getkey)
path_solution35_New       = sorted(path_solution35_New, key=getkey)



#header2, second_path_run = read_results_file('sim_trajs_all.csv')
#second_path_run       = sorted(second_path_run, key=getkey)



# read in the jitter results
jitter_header,jitter_results = read_results_file('Final_Results_All_Jitter.csv')
jitter_results       = sorted(jitter_results, key=getkey2)
jitter_results       = sorted(jitter_results, key=getkey)


# read in the hyperspace results
#hyperspace_header,hyperspace_results = read_results_file('Final_Results_Hyperspace.csv')
#hyperspace_results       = sorted(hyperspace_results, key=getkey)


adjust_file = open("Adjust_Score.csv",'wb')
adjust_csv  = csv.writer(adjust_file)
adjust_csv.writerow(['driver_trip','Move_Up_this_percent','Move_to_this_percentile'])


combined_results = combine_path_results(path_solution13,path_solution15,path_solution17,adjust_csv, path_solution7_New, path_solution8_New, path_solution9_New, path_solution10_New, path_solution11_New, path_solution12_New, path_solution13_New, path_solution14_New, path_solution15_New, path_solution17_New, path_solution19_New, path_solution21_New,path_solution25_New, path_solution30_New, path_solution35_New,  jitter_results)
write_results_file(header,combined_results,'Current_Best_Path_Solution.csv')


#  process the jitter results to make the adjustment file
process_jitter_results(jitter_results,adjust_csv)


#  process the hyperspace results to make the adjustment file
#process_hyperspace_results(hyperspace_results,adjust_csv)



print("Finished with combine path solutions")


adjust_file.close()