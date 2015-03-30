# -*- coding: utf-8 -*-
"""
(c) 2015

@author:        Janto Oellrich
email:          joellrich@uos.de

CONTENT

    Functions to compute the probabilities using a given model
"""
from modules import *


def score(model,trips,reference):
    """
    Returns for each trip the probability that it belongs to that driver.
    
    INPUT:
        model:         sklearn model, e.g. LogisticRegression(C=100)
        trips:         feature matrix of all drivers
        reference:     contrast driver set  
    OUTPUT:
        SCORES:        [547200-by-1] array of predicted probabilities
    """
    
    #####
    
    driverFolder = DATA
    # driver IDs
    drivers = sorted([int(folderName) for folderName in os.listdir(driverFolder)])
    ######
        
    # INITIALIZE
    SCORES = np.zeros(shape=(547200,1))  
    
    start = 0
    
    for k,driver in enumerate(drivers):
        
        # get trips of current driver
        current_driver = trips[start:start+200,:]        
               
        train_driver = current_driver
                        
        # labels for logistic regression
        labels = np.concatenate((np.ones(shape=(train_driver.shape[0],1)),np.zeros(shape=(reference.shape[0],1))),axis=0)
        
        # combine with driver+outliers with reference
        data = np.concatenate((current_driver,reference),axis=0)
        
        train_data = np.concatenate((train_driver,reference),axis=0)  
                
        #### MODEL TO SEPARATE OUTLIERS ####
        model = model        
        model.fit(train_data,labels[:,0])
        SCORES[start:start+200,0] = model.predict_proba(data[0:200,:])[:,1] # probabiliy of belonging to class 1 (=driver)
        
        # update start
        start += 200
        
        # prompt status
        if (k+1)%250==0:
            print '{0} drivers done.'.format(k+1)        

    # check if out vector matches number of drivers
    if SCORES.shape[0]!=547200:
        print 'Incorrect number of scores!'      
    
    return SCORES