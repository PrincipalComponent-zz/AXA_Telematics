#from celery import Celery
from modules_tai.driver_model import DriverModel
from config import config
import numpy as np
# %load_ext autoreload
# %autoreload 2

#app = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

#@app.task
def add(x, y):
    return x + y


#@app.task
def load_driver_celery(driver_id):
        # min_group_length = int(config.get('algo_sim_trips', 'min_trips_in_groups'))
        # print 'min group sim trip size: %s'%min_group_length
        print 'for driver %s'%driver_id
        dm = DriverModel(driver_id)
        simtraj, npst = dm.detectSimilarTraj()
        sim_groups = dm.computeSimilarTrips()
        driver_trips_id = np.arange(200)+1 + int(driver_id)*10000
        trips_id = npst[:,0] +1
        sim_trips = np.zeros(200)
        sim_trips_group = np.zeros(200)
        for group in sim_groups:
                gl = len(group)
                for gid in group: 
                        sim_trips[gid] = 1
                        sim_trips_group[gid] = gl
        print 'num sim trips for driver %s is %s'%(driver_id, np.sum(sim_trips))
        res = np.c_[np.ones(200) * int(driver_id), driver_trips_id, trips_id, sim_trips, sim_trips_group]
        return res

#@app.task
def load_driver_aggmat_celery(driver_id):
        # min_group_length = int(config.get('algo_sim_trips', 'min_trips_in_groups'))
        # print 'min group sim trip size: %s'%min_group_length
        print 'for driver %s'%driver_id
        dm = DriverModel(driver_id)
        aggmat = dm.agg_mat
        print 'ahape aggmat %s'%aggmat.shape[1]
        
        # added = np.c_[np.ones((200,1))*int(driver_id) , np.linspace(1,200,200).reshape(200,1)]
        # print 'added aggmat %s'%added.shape[1]
        # aggmat = np.c_[added, aggmat]
        # print 'ahape aggmat %s'%aggmat.shape[1]

        return aggmat, dm.agg_headers
