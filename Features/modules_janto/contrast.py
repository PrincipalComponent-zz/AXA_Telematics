# -*- coding: utf-8 -*-
"""
(c) 2015

@author:        Janto Oellrich
email:          joellrich@uos.de

CONTENT
        Function for contrast driver sampling
"""
from modules import *

def sampleContrast(trips,n_ref=1000):
    """
    Given the featmatrix samples n_ref contrast trips.
    """
    print 'Sampling contrast trips...'    
    
    # random sampling of trips from different drivers
    ref_trips = np.random.choice(trips.shape[0],size=(n_ref,1),replace=False)
    
    ref = trips[ref_trips[:,0],:]
    
    print '\t\t{0} contrast trips, {1} features'.format(ref.shape[0],ref.shape[1])
    
    return ref
    