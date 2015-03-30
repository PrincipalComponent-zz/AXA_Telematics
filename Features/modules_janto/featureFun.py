# -*- coding: utf-8 -*-
"""
(c) 2015

@author:    Janto Oellrich
email:      joellrich@uos.de

CONTENT:
    Contains FEATURE EXTRACTION funtions for 
    the AXA telematics competition.  
    
    FUNCTION LIST:
    
    features:       creates feature vector for one trip    
    
    driverFrame:    creates feature matrix containing features 
                    of all trips  of one driver

    createFeatmat:  create feature matrix for all drivers               
    
    
    
"""
from load import *
from modules import *
from paths import *


def features(trip,plotting=False):
    """
    Extracts features of a trip dataframe.
    OUTPUT:
        np.array including features
        list of angles between points in deg
    """
    
    # 1. duration
    duration = len(trip)    
    
    # 2. speed: euclidean distance between adjacent points
    speed = np.sum(np.diff(trip,axis=0)**2,axis=1)**0.5
    
    ### 2.1. smooth GPS data (by convolution) ####    
    smooth_speed =  movingaverage(speed,10) 
    #smooth_speed[np.where(smooth_speed>65)[0]] = smooth_speed[np.where(smooth_speed>65)[0]-1]
    
    # head changes
    head = np.diff(trip,axis=0)
    head_x,head_y = head[:,0],head[:,1]
    
    head_quantiles_x = ss.mstats.mquantiles(head_x,np.linspace(0.02,0.99,10))
    head_quantiles_y = ss.mstats.mquantiles(head_y,np.linspace(0.02,0.99,10))
    
    # compute speed statistics    
    mean_speed = smooth_speed.mean()
    max_speed = max(smooth_speed)
    std_speed = speed.std()
    # 3. acceleration
    smooth_accel = np.diff(smooth_speed)    
    
    # 3.1 get all negative acceleration values
    accel_s = np.array(smooth_accel)    
    neg_accel = accel_s[accel_s<0]
    pos_accel = accel_s[accel_s>0]

    # 3.3 average breaking strength
    mean_breaking = neg_accel.mean()
    mean_acceleration = pos_accel.mean() 
    
    # summary statistics
    std_breaking = neg_accel.std()
    std_acceleration = pos_accel.std()
    
    # 4. total distance traveled    
    total_dist = np.sum(smooth_speed,axis=0)               
    
    # 5. relative standzeit (last 5% are discarded due standing)
    last = round(len(trip)*0.05)
    eps = 1 # threshold for determining standing
    
    # relative standzeit
    speed_red = np.array(speed)[:last]
    standzeit = len(speed_red[speed_red<0+eps])/float(duration) 
    
    #### DRIVING STYLE REALTED FEATURES ####
    # 1. acceleration from stop
    
    # 1.1 get end of stops: where is speed near zero
    end_stops = stops(smooth_speed)        
    n_stops = len(end_stops) # how many stops
    
    # 1.2 how does the driver accelerate from stop?
    
    end_stops = end_stops.astype(int)[:-1,1]
    
    # following interval
    interval = 7 # 7 seconds following end of stop
    
    # only those which dont exceed indices of trip
    end_stops = end_stops[end_stops+interval<len(smooth_speed)-1]    
    n_stops = len(end_stops) 
    
    if n_stops>1:
        anfahren = np.zeros(shape=(1,n_stops)) # initialize array
        
        for i in range(n_stops):
            
            # slope at acceleration    
            start = end_stops[i]
            
            anfahren[0,i] =  np.diff([smooth_speed[start],smooth_speed[start+interval]])
           
    else:
        anfahren = np.array([0])
    # compute statistics
    mean_anfahren = anfahren.mean()
    max_anfahren = anfahren.max()
    std_anfahren = anfahren.std()
    
    # end cell
    last_cell = rounddown(normalize(trip[-2:,:]),30)[-1]
    
    # determine trip is a back-home trip
    if last_cell[0]==0 and last_cell[1]==0:
        hometrip=1
    else:
        hometrip=0
    
    # speed quantiles
    speed_quantiles = ss.mstats.mquantiles(smooth_speed,np.linspace(0.02,0.99,25)) 
    # acceleration quantiles
    accel_quantiles = ss.mstats.mquantiles(smooth_accel,np.linspace(0.02,0.99,25))
    
    ################# PLOTS #################
    if plotting:
        figure()        
        x = range(1,len(trip)) # x values for plotting
        #plot(x,total_dist,label='velocity') #speed 
        hold('on')
        #plot(x,accel,color='red',alpha=0.6,label='acceleration') #acceleration 
        grid('on')
        xlabel('time')
        
        # plot smoothed speed data
        plot(smooth_speed,color='k',label='Spline Interpol')
        # plot smoothed accelerationd data
        plot(smooth_accel,'red',label='Acceleration')
        legend(loc='best')
        
        
    #legend()
    ######################################
    
    return np.concatenate((speed_quantiles,accel_quantiles,head_quantiles_x,head_quantiles_y,np.array([duration,total_dist,standzeit,std_speed,std_breaking,std_acceleration,std_anfahren,mean_anfahren,max_anfahren,n_stops,hometrip])))


def driverFrame(driver,n_features=10):
        
    # initialize dataframe
    trips = np.zeros(shape=(200,n_features))    
    
    # load all trips at once
    all_trips = loadDriver(driver)
    
    counter = 0
    
    for trip in all_trips:   
    
        trips[counter,:] = features(trip,False)  
    
        counter += 1
    return trips
    
def createFeatmat():
    """
    Computes the features of all trips and stores them in a matrix.
    """
    driverFolder = DATA
    # driver IDs
    drivers = sorted([int(folderName) for folderName in os.listdir(driverFolder)])
        
    print 'Creating feature matrix...'        
        
    n_feat = 81 
    
    for i,driver in enumerate(drivers):
        
        if i == 0:
            featmat = driverFrame(driver,n_feat)
        else:
            featmat = np.vstack((featmat,driverFrame(driver,n_feat)))
    
    print '\t\t{0} trips, {1} features'.format(featmat.shape[0],featmat.shape[1])
    
    # write to file
    np.save(os.path.join(FEATURES,'featurematrix1.npy'))    
    
    return featmat
        
