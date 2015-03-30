# -*- coding: utf-8 -*-
"""
(c) 2015

@author:    Janto Oellrich
email:      joellrich@uos.de

CONTENT:
    Contains SUBMISSION funtion AXA telematics competition.      
      
    submit:         takes array of predictions and creates submission
"""
import os
from modules import *

def submit(values,outfile,driverFolder=DATA):
    """
    Given a list of values constructs submission file
    for each trip in AXA challenge.

    INPUT:
        values: vector of 547200 probabilities
    OUTPUT:
        csv submission file
    """
    # 0. check if input vector matches IDs
    if len(values)!=547200:
        raise Exception('Incorrect number of values!')

    # 1. get all driver IDs
    drivers = sorted([int(folderName) for folderName in os.listdir(driverFolder)])
    start = 0
    
    # 2. write trip ID and probability value to row
    with open(outfile, "w") as fout:
        
        # insert header  
        fout.write(','.join(['driver_trip','prob'])+'\n')
        
        # go through all drivers
        for driver in drivers:

            rows = ['%s_'%driver+str(i) for i in range(1,201)]
            #print 'Driver {0}, {1} to {2},   start is {3}'.format(driver,rows[0],rows[-1],start)
            
            cur_values = values[start:start+200,0]
            # insert trip ID and submission
            if len(cur_values)==len(rows):
                for row,value in zip(rows,cur_values):
                    fout.write(','.join([row,str(value)])+'\n')

            #update start
            start += 200
            
    # 3. prompt success
    if os.path.isfile(outfile):
        print 'Submission file %s successfully created.'%outfile
    else:
        raise Exception('\nSubmission file not created.')