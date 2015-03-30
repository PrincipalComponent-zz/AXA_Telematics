# -*- coding: utf-8 -*-
"""
(c) 2015

@author:    Janto Oellrich
email:      joellrich@uos.de

CONTENT

    Computes the probabilities for each trip using 
    Logistic Regression and Random Forest.
    
    A random sample of 1000 drivers are created as contrast set, 
    assigned a class label. 
    The classifiers are trained on each driver's trips and the contrast set.
"""
#import numpy as np
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.linear_model import LogisticRegression

# import custom made modules
from modules_janto.modules import * 
from modules_janto.paths import *

###################################################

# set random number generator seed
np.random.seed=666

# 1. create Featmat
featmat = np.load(os.path.join(FEATURES,'featurematrix1.npy'))# debugging
featmat = featmat[:,2:]

# 2. sample contrast drivers
ref_RandForest = sampleContrast(featmat,200)
ref_LogReg = sampleContrast(featmat,1000)

# 3. run the model(s)
RandForest = RandomForestClassifier(n_estimators=250,random_state=0)
LogReg = LogisticRegression(C=10,random_state=0)

print '\n\nRUNNING MODELS...\n\n'

# 1. Random Forest
print 'Running Random Forest.\n'
results_RF = score(RandForest,featmat,ref_RandForest)

# Logistic Regression
print '\n\nRunning Logistic Regression.\n'
results_LR = score(LogReg,featmat,ref_LogReg)

### ENSEMBLE THE MODELS ###
weightLR = 0.1
weightRF = 0.9

final = results_RF*0.9+results_LR*0.1

# 4. write results to file
submit(final,os.path.join(MODELS,'ensembleLRRF.csv'))
#submit(results_RF,'RandomForest_janto.csv')