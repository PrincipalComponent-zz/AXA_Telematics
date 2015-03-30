# -*- coding: utf-8 -*-
"""
(c) 2015

@author:    Janto Oellrich
email:      joellrich@uos.de

CONTENT:
    Contains PREPROCESSING funtions  (smoothing and geometric transformations,
    such as flipping, rotating or normalizing north) for the 
    AXA telematics competition.      
     
    FUNCTION LIST:
    
    movingaverage:  smoothes GPS data by movingaverage 
    
    rotate:         rotates trip by a given angle
    flip:           flips trip along x-axis
    point_north:    transforms trip to point start-end vector north
    normalize:      puts all fo them together to normalize trips  
    rounddown:      convert GPS to cells (i.e. local binning)
    stops:          get indices of stops (smoothed speed<0.5)
"""
#from math import cos, sin
from modules import *

### 1. SMOOTHING###

# moving average smoothin filter
def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    
    smoothed = np.convolve(values, weigths, 'valid')
    return smoothed 
    
### 2. GEOMETRIC NORMALIZATION ###

def rotate(vector,angle, origin=(0, 0)):
    cos_theta, sin_theta = cos(angle), sin(angle)
    x0, y0 = origin

    vector = np.array(vector) -np.array(origin) 
    
    rotation_mat = np.array([[cos_theta,-sin_theta],[sin_theta,cos_theta]])
    #print rotation_mat
    
    vector_rotated =  np.dot(rotation_mat,vector)
    
    return vector_rotated
    
def flip(trip,horizontal=True,vertical=False):
    """
    Flips GPS coordinates of a trip along specified axis
    (horizontal or vertical).
    """
    
    if horizontal:
        trip[:,0]= -trip[:,0]
     
    return trip

def point_north(trip):
    """
    Rotates all GPS such that trip (vector of end point) points north.
    """
    
    # 1. determine angle between start-end vector and north pointing vector
    #north = [1,0]
    end = trip[-1,:] # "mean vector"
    
    angle = np.arctan2(end[0],end[1]) #angle_between(end,north) # in radians
    
    # 2. rotate all points
    rotated_trip = np.zeros(shape=(len(trip),2))
    
    for i in range(len(trip)):
        rotated_trip[i,:] = rotate(trip[i,:],angle)
        
    return(rotated_trip)

def normalize(trip):
        
    normed = point_north(trip)
    
    if normed[:,0].mean()<0:
        normed = flip(normed) 
    
        
    return(normed)
    
def rounddown(x,cellsize=10):
    ten =  np.floor(x / 10) * 10
    return np.trunc(ten/cellsize)
    
def stops(bits):   

  # make sure all runs of ones are well-bounded
  bounded = np.hstack(([1], bits, [1]))

  log = (bounded<0+0.5)*1
    
  # get 1 at run starts and -1 at run ends
  diffs = np.diff(log)    
  
  # get indices if starts and ends
  run_starts = np.where(diffs > 0)[0]
  run_ends = np.where(diffs < 0)[0]
  
  return np.array([run_starts,run_ends,run_ends-run_starts]).T
