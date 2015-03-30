# -*- coding: utf-8 -*-
"""
(c) 2015

@author:    Janto Oellrich
Email:      joellrich@uos.de 

CONTENT:
    Contains DATA IMPORT and NUMPY CONVERSION
    funtions for the AXA telematics competition.  
    
    FUNCTION LIST:
    
    loadDriver:     loads all trips for one driver (list of arrays)
    loadTrip:       load GPS data of in trip
"""
from modules import *
from paths import *


def loadDriver(driverNr):
    
    root = DATA
    
    # load .npy file
    return np.load(os.path.join(root,'{}\\trips.npy'.format(driverNr)))


def loadTrip(driver,trip):
    """
    Fast function to load raw GPS data of driver's trip.
    """
    
    if trip>200 or trip<=0:
        raise Exception('Invalid input: wrong trip Nr.')
    
    return loadDriver(driver)[trip-1]
