# -*- coding: utf-8 -*-
import numpy as np
from config import config
from os import listdir
from os.path import isfile, join
# from telematics.utils.signal_utils import smooth
# from telematics.utils.signal_utils import removeRotation
import utils.signal_utils as sigut

from modules_janto.paths import *
        
data_path = DATA    
print DATA  
#data_path = "..\\..\\..\\..\\drivers_raw\\" 


#data_path = "C:\\Users\\Scott\\Desktop\\Kaggle Competitions\\Driver_Telematics\\kaggle-driver-fingerprint\\drivers_raw\\"


import matplotlib.pyplot as plt
import math

# MIN TRAJ LENGTH
MIN_TRAJ_LENGTH = 1500
MAX_DIFF_FLYING_DIST_PCT = .25
MAX_DIFF_X_EXTREMA_POS_PCT = .35

# FOR SAMPLING TRAJ AT EXTREMA
NUM_STEPS = 31
SAMPLE_LENGTH = 50

# FOR DETECTING SIMILAR TRAJS
MAX_DIFF_X_EXTREMA_POS_PCT = .15
THRESHOLD_MAX_DIFF = 30
THRESHOLD_MEAN_DIFF = 10

# FOR THE CURV PORTIONS
CURV_TRONCON = range(7) #How much portions do we keep
CURV_TRONCON_BIGTURN = range(4) #How much portions do we keep
SPEED_DELTA_PORTION = 20 # discretization of speed into trunc of 20
SPEED_TRONCON = range(8) #How much speed portions do we keep
TIMEDELTA_AHEAD = 4
TIMEDELTA_BEFORE = 4

# COLUMNS IN THE MATRIX
AUGMENT_TRIP_DATA = True
SMOOTH_DELTA = 2 # number of seconds taken to smooth data
SMOOTH_DELTA_CURV = 6 # number of seconds taken to smooth data for computing the curv
CURV_INT_FACTOR = 1.3


class DriverModel(object):


        def __init__(self, driver_id):
                print "driver : %s created"%(driver_id)
                self.driver_id = driver_id
                self.driver_path = os.path.join(data_path,str(driver_id))
                # print self.driver_path
                trips = onlyfiles = [ f for f in listdir(self.driver_path) if isfile(join(self.driver_path,f)) ]
                self.nptrips = []
                self.nptripsdict = {}
                counter = 0                
                for trip in trips:
                        if trip.split('.')[1] != 'npy':
                            # print "for trip %s"%trip
                            tripnum = int(trip.split('.')[0])
                            fn = join(self.driver_path,trip)
                            data = np.genfromtxt(fn, dtype=float, delimiter=',', skip_header=1)
                            data = sigut.removeRotation(data)
                            data = self.augmentTripData(data, AUGMENT_TRIP_DATA)
                            
                            self.nptripsdict[tripnum] = data                        
                            counter += 1
                            # if counter == 20: break
                            # print counter
                            # break
                for tripnum in np.arange(1,201):
                        self.nptrips.append(self.nptripsdict[tripnum])

                self.aggregateCatData()

        def augmentTripData(self, XY, full=True):
                # GET ONE STEP AWAY ... using a kernel function on a few timestamps
                # could be better but slower this could be tested later

                XY2 = XY.copy()
                for nn in range(SMOOTH_DELTA):
                        XY2 = np.r_[XY2,[XY2[-1]]]
                        XY2 = np.delete(XY2, 0, 0)
                vxy = (XY2-XY)/SMOOTH_DELTA

                XY2 = XY.copy()
                XY1 = XY.copy()
                for nn in range(SMOOTH_DELTA_CURV):
                        if nn<(SMOOTH_DELTA_CURV/2) : 
                                XY2 = np.r_[XY2,[XY2[-1]]]
                                XY2 = np.delete(XY2, 0, 0)
                        else:
                                XY1 = np.r_[[XY1[0]],XY1]
                                XY1 = np.delete(XY1, -1, 0)

                vxy_curv = (XY2-XY1)/SMOOTH_DELTA_CURV

                # basic matrix with t and positions
                t = np.arange(XY.shape[0])
                XY = np.c_[t, XY]
                self.headers = {'t':0, 'x': 1, 'y':2}

                # adding dist and cumulated dist
                dist = np.sqrt(np.einsum('ij,ij->i', vxy, vxy))
                cc = np.cumsum(dist)
                XY = np.c_[XY, dist]
                XY = np.c_[XY, cc]
                self.headers['d'] = 3
                self.headers['cum_d'] = 4

                if not full: return XY
                #adding speed and tangential acceleration
                # Computing using kernel function
                # speed = sigut.smooth(t,cc, 5, 2, 1)*3.6
                # acc_T = sigut.smooth(t,cc, 5, 2, 2)
                # Computing using simple delta
                cc2 = np.r_[cc,[cc[-1]]]
                cc2 = np.delete(cc2, 0, 0)
                speed = cc2 - cc
                speed_int = speed*3.6/SPEED_DELTA_PORTION
                speed_int = speed_int.astype(int)
                speed_int[speed_int>(SPEED_TRONCON[-1]+1)] = (SPEED_TRONCON[-1]+1)
                speed2 = np.r_[speed,[speed[-1]]]
                speed2 = np.delete(speed2, 0, 0)
                acc_T = speed2 - speed
                XY = np.c_[XY, speed*3.6, speed_int, acc_T]
                self.headers['speed'] = 5
                self.headers['speed_int'] = 6
                self.headers['a_t'] = 7

                #adding curvature and normal acceleration http://en.wikipedia.org/wiki/Curvature
                # curvature for cartesian data is  \kappa = \frac{|x'y''-y'x''|}{(x'^2+y'^2)^{3/2}},
                curv_r, curv_int = self.computeRCurv2(vxy_curv)
                
                XY = np.c_[XY, curv_r, curv_int]
                XY = np.c_[XY, speed*speed/curv_r]
                self.headers['K'] = 8
                self.headers['K_int'] = 9
                self.headers['a_n'] = 10

                curv_int_ahead = curv_int.copy()
                for nn in range(TIMEDELTA_AHEAD):
                        curv_int_ahead = np.r_[curv_int_ahead,[curv_int_ahead[-1]]]
                        curv_int_ahead = np.delete(curv_int_ahead, 0, 0)

                curv_int_before = curv_int.copy()
                for nn in range(TIMEDELTA_BEFORE):
                        curv_int_before = np.r_[[curv_int_before[0]],curv_int_before]
                        curv_int_before = np.delete(curv_int_before, -1, 0)

                XY = np.c_[XY, curv_int_ahead, curv_int_before]
                self.headers['K_int_after'] = 11
                self.headers['K_int_before'] = 12

                return XY

        def     addAggHeaders(self, totheaders, agg_data, TRONCON, strT):
                hcol = []
                for st in TRONCON: hcol.append("%s_%s"%(strT, st))

                for key in agg_data.keys():
                        hrow = []
                        for hh in agg_data[key]: hrow.append('%s_%s'%(key, hh))

                        for hc in hcol:
                                for hr in hrow: totheaders.append("%s_%s"%(hc,hr))

         
        def aggregateCatData(self):
                # COMPUTE GLOBAL DATA ON
                #       avg-std-max speed
                #       std-max a_t
                #       std-max a_n
                #       max x (flying dist)
                #       last cum_dist (total dist)
                global_headers = ['DR', 'Driver', 'trip', 'avg_speed', 'std_speed', 'perc_99_speed',
                                        'std_a_t', 'perc_99_a_t', 'std_a_n', 'perc_99_a_n', 
                                        'flying_dist', 'total_dist', 'total_time']

                # AGGREGATE ON SPEED TRONCON 
                agg_data_speed = { 'a_t': ['count_pct', 'std', 'percentile_99'],
                                        'a_n': ['median','std','percentile_99']}
                
                # # AGGREGATE ON CURV TRONCON
                agg_data_curv = { 'speed': ['median','std','percentile_99'],
                                        'a_t': ['median','std','min','percentile_99']}
                
                # # AGGREGATE ON CURV TRONCON AFTER
                agg_data_curv_ahead = { 'speed': ['median','std','percentile_99'],
                                        'a_t': ['median','std','min','percentile_99']}

                # # AGGREGATE ON CURV TRONCON BEFORE
                agg_data_curv_before = { 'speed': ['median','std','percentile_99'],
                                        'a_t': ['median','std','min','percentile_99']}

                # COMPUTE HEADERS
                self.agg_headers = global_headers
                self.addAggHeaders(self.agg_headers, agg_data_speed, SPEED_TRONCON, 'ST')
                self.addAggHeaders(self.agg_headers, agg_data_curv, CURV_TRONCON, 'KT')
                self.addAggHeaders(self.agg_headers, agg_data_curv_before, CURV_TRONCON_BIGTURN, 'KT_BEF')
                self.addAggHeaders(self.agg_headers, agg_data_curv_ahead, CURV_TRONCON_BIGTURN, 'KT_AFT')
                
                # COMPUTE AGGREGATE MAT
                self.agg_mat =  np.zeros((len(self.nptrips),len(self.agg_headers)))     

                # ADD GLOBAL AND LOCAL VALUES
                for idx, trip in enumerate(self.nptrips):
                        agg_trip = np.zeros((1,13))
                        
                        agg_trip[0,0] = int(self.driver_id) * 10000 + idx + 1
                        agg_trip[0,1] = int(self.driver_id) 
                        agg_trip[0,2] = idx + 1
                        
                        agg_trip[0,3] = np.nanmedian(trip[:,self.headers['speed']])
                        agg_trip[0,4] = np.nanstd(trip[:,self.headers['speed']])
                        agg_trip[0,5] = np.nanpercentile(trip[:,self.headers['speed']],99)
                        
                        agg_trip[0,6] = np.nanstd(trip[:,self.headers['a_t']])
                        agg_trip[0,7] = np.nanpercentile(trip[:,self.headers['a_t']],99)
                        agg_trip[0,8] = np.nanstd(trip[:,self.headers['a_n']])
                        agg_trip[0,9] = np.nanpercentile(trip[:,self.headers['a_n']],99)

                        agg_trip[0,10] = trip[-1,self.headers['x']]
                        agg_trip[0,11] = trip[-1,self.headers['cum_d']]
                        agg_trip[0,12] = trip.shape[0]

                        for key in agg_data_speed.keys():
                                res = sigut.group_by_func(SPEED_TRONCON, trip[:,self.headers['speed_int']], 
                                        trip[:,[self.headers[key]]],agg_data_speed[key], mincount = 25)
                                rs = res.shape
                                resf = res[:,1:rs[1]].reshape((1,rs[0]*(rs[1]-1)))
                                agg_trip = np.c_[agg_trip, resf]
                        
                        for key in agg_data_curv.keys():
                                res = sigut.group_by_func(CURV_TRONCON, trip[:,self.headers['K_int']], 
                                        trip[:,[self.headers[key]]],agg_data_curv[key], mincount = 15)
                                rs = res.shape
                                resf = res[:,1:rs[1]].reshape((1,rs[0]*(rs[1]-1)))
                                agg_trip = np.c_[agg_trip, resf]

                        for key in agg_data_curv_before.keys():
                                res = sigut.group_by_func(CURV_TRONCON_BIGTURN, trip[:,self.headers['K_int_before']], 
                                        trip[:,[self.headers[key]]],agg_data_curv_before[key], mincount = 15)
                                rs = res.shape
                                resf = res[:,1:rs[1]].reshape((1,rs[0]*(rs[1]-1)))
                                agg_trip = np.c_[agg_trip, resf]

                        for key in agg_data_curv_ahead.keys():
                                res = sigut.group_by_func(CURV_TRONCON_BIGTURN, trip[:,self.headers['K_int_after']], 
                                        trip[:,[self.headers[key]]],agg_data_curv_ahead[key], mincount = 15)
                                rs = res.shape
                                resf = res[:,1:rs[1]].reshape((1,rs[0]*(rs[1]-1)))
                                agg_trip = np.c_[agg_trip, resf]

                        self.agg_mat[idx,:] = agg_trip



        def computeRCurv2(self, vxy):
                vxy2 = np.r_[vxy,[vxy[-1]]]
                vxy2 = np.delete(vxy2, 0, 0)
                axy = vxy2 - vxy

                curv = np.power(vxy[:,0]*vxy[:,0]+vxy[:,1]*vxy[:,1], 1.5) / abs(vxy[:,0]*axy[:,1] - vxy[:,1]*axy[:,0])
                curv2 = curv.copy()
                curv2 = np.r_[[curv[0]], curv]
                curv2 = np.delete(curv2, -1,0)
                curv = (curv2+curv)/2.0
                curv_int = np.log(curv)/CURV_INT_FACTOR
                curv_int = curv_int.astype(int)
                curv_int[curv_int<0] = 0
                curv_int[curv_int>CURV_TRONCON[-1]] = CURV_TRONCON[-1]

                return curv, curv_int

        def computeRCurv(self, XY):
                vx = (sigut.smooth(XY[:,0], XY[:,1], 5, 2, 1))
                # vx = abs(dxy[:,0])
                vy = (sigut.smooth(XY[:,0], XY[:,2], 5, 2, 1))
                # vy = abs(dxy[:,1])
                ax = sigut.smooth(XY[:,0], vx, 5, 2, 1)
                ay = sigut.smooth(XY[:,0], vy, 5, 2, 1)

                curv = np.power(vx*vx+vy*vy, 1.5) / abs(vx*ay - vy*ax)
                # curv = sigut.smooth(XY[:,0], curv, 7, 5, 0)
                curv_int = np.log(curv)
                curv_int = curv_int.astype(int)
                curv_int[curv_int<0] = 0
                curv_int[curv_int>CURV_TRONCON[-1]] = CURV_TRONCON[-1]

                return curv, curv_int


        def getSampledTrajAroundMax(self, trip):
                # Find min and max Y idx of both trips
                """ From Max and Min Y position in the Traj, get the X-Y position forward and backward
                        sampled in distance 

                        columnY is at idx 2
                """
                idxMax = np.argmax(trip[:,self.headers['y']])
                idxMin = np.argmin(trip[:,self.headers['y']])
                # print "xmax at %s: %s - xmin at %s: %s"%(idxMax, trip[idxMax,self.headers['y']], idxMin, trip[idxMin,self.headers['y']])

                # traj forward from index sampled every XX meters during N steps
                nmid = (NUM_STEPS-1)/2
                ss = (np.arange(NUM_STEPS) * SAMPLE_LENGTH) - (nmid*SAMPLE_LENGTH)
                res = {'max': trip[idxMax,self.headers['y']], 
                        'max_x': trip[idxMax,self.headers['x']], 
                        'min': trip[idxMin,self.headers['y']], 
                        'min_x': trip[idxMin,self.headers['x']], 
                        'flying_dist': trip[-1,self.headers['x']],
                        'total_dist': trip[-1,self.headers['cum_d']]}

                if res['total_dist'] < MIN_TRAJ_LENGTH: return res

                idtest = idxMax 
                length_trip = trip.shape[0]
                cumdist = trip[length_trip-1,self.headers['cum_d']]
                if idtest > nmid and idtest < (length_trip-nmid): #the min should not be at start or end in time
                        # the min should not be at start or end in dist
                        if trip[idtest, self.headers['cum_d']]>(nmid*SAMPLE_LENGTH) and (cumdist-trip[idtest, self.headers['cum_d']])>(nmid*SAMPLE_LENGTH):
                                res['maxar'] = self.interpAroundId(idtest, trip, NUM_STEPS, nmid, ss)
                idtest = idxMin         
                if idtest > nmid  and idtest < (length_trip-nmid):
                        if trip[idtest, self.headers['cum_d']]>(nmid*SAMPLE_LENGTH) and (cumdist-trip[idtest, self.headers['cum_d']])>(nmid*SAMPLE_LENGTH):
                                res['minar'] = self.interpAroundId(idtest, trip, NUM_STEPS, nmid, ss)
                # print dist_interp
                # res = np.concatenate((x_interp, y_interp, dist_interp), axis=0)
                return res

        def interpAroundId(     self, idtest, trip, Nsteps, nmid, samples):
                newzero = trip[idtest,:]        
                # import pdb
                # pdb.set_trace()       
                ndist = trip[:, self.headers['cum_d']] - newzero[self.headers['cum_d']]
                # print ndist[idtest]

                res = np.zeros((Nsteps, 2), dtype=np.float)
                res[:,0] = np.interp(samples,  ndist, trip[:,self.headers['x']])
                res[:,1] = np.interp(samples,  ndist, trip[:,self.headers['y']])
                # res[:,2] = np.interp(samples,  ndist, trip[:,4])
                res = sigut.removeRotation(res, removeBias=True)
                shifted = -res[:,1]
                res = np.c_[res, shifted]

                return res              

        def detectSimilarTraj(self):
                # First get all maxima dict
                self.extrema_trajs = []
                count=0
                for trip in self.nptrips:
                        self.extrema_trajs.append(self.getSampledTrajAroundMax(trip))
                        count +=1

                numtrajs = len(self.nptrips)
                self.similarTrips = []
                self.similarTripsNP = np.zeros((numtrajs,2))
                self.similarTripsNP[:,0] = np.arange(200)


                for i in range(numtrajs):
                        self.similarTrips.append([i, 0,[]])

                for i in range(numtrajs):
                        tt1 = self.extrema_trajs[i]

                        for j in range(i+1,numtrajs):
                                tt2 = self.extrema_trajs[j]
                                delta_flyingdist = abs(tt2['flying_dist'] - tt1['flying_dist'])
                                avg_flyingdist = (tt2['flying_dist'] + tt1['flying_dist'])/2
                                if  delta_flyingdist < (MAX_DIFF_FLYING_DIST_PCT * avg_flyingdist):
                                # print 'compare traj %s with traj %s'%(i,j)
                                        res = self.compareSampleTrajDist(tt1, tt2)
                                else:
                                        res = -1
                                if res>=0: 
                                        self.similarTrips[i][2].append(j)
                                        self.similarTrips[j][2].append(i)
                                        self.similarTrips[i][1] = 1
                                        self.similarTrips[j][1] = 1
                                        self.similarTripsNP[i,1] = 1
                                        self.similarTripsNP[j,1] = 1
                return self.similarTrips, self.similarTripsNP

        def computeSimilarTrips(self, log=False):
                self.sim_trip_groups = []
                alltogether = []

                if not hasattr(self, 'similarTrips'):
                        self.detectSimilarTraj()
                for traj in self.similarTrips:
                        if traj[1] == 0: continue
                        if traj[0] in alltogether: continue
                        newgroup = []+traj[2]                   
                        for elem in newgroup:
                                newgroup = newgroup + self.similarTrips[elem][2]
                        newgroup = list(set(newgroup))
                        for elem in newgroup:
                                newgroup = newgroup + self.similarTrips[elem][2]
                        newgroup = list(set(newgroup))
                        for elem in newgroup:
                                newgroup = newgroup + self.similarTrips[elem][2]
                        newgroup = list(set(newgroup))
                        alltogether = alltogether + newgroup
                        newgroup.sort()
                        self.sim_trip_groups.append(newgroup)

                if log:
                        print 'Num groups is : %s'%len(self.sim_trip_groups)
                        for i,group in enumerate(self.sim_trip_groups):
                                print 'Group %s : %s'%(i,group)

                return self.sim_trip_groups
                
        def compareSampleTrajDist(self, sample1, sample2):

                avg_flyingdist = (sample1['flying_dist'] + sample2['flying_dist'])/2
                if 'maxar' in sample1 and 'maxar' in sample2:
                        delta_extrema = abs(sample1['max'] + sample2['max'])/ avg_flyingdist
                        delta_extrema_x = abs(sample1['max_x'] - sample2['max_x']) / avg_flyingdist
                        if delta_extrema < MAX_DIFF_X_EXTREMA_POS_PCT and delta_extrema_x < MAX_DIFF_X_EXTREMA_POS_PCT:
                                diffX = sample1['maxar'][:,0] - sample2['maxar'][:,0]
                                diffY = sample1['maxar'][:,1] - sample2['maxar'][:,1]
                                diff = np.c_[diffX,diffY]

                                p = np.power(diff,2)
                                dist = np.sqrt( p[:,0]+p[:,1] )
                                mmax = np.max(dist)
                                mmean = np.sum(dist)/dist.shape[0]
                                # dist = np.sqrt(np.einsum('ij,ij->i',c,c))
                                # print 'compute max - min diff - delta = %s - %s'%(mmax, mmean)
                                if mmax < THRESHOLD_MAX_DIFF and mmean < THRESHOLD_MEAN_DIFF :
                                        return 0
                                #TODO to improve, we could rotate both traj and test the ending Y distance

                        #test if extrema are too different
                if 'maxar' in sample1 and 'minar' in sample2:
                        delta_extrema = abs(sample1['max'] + sample2['min'])/ avg_flyingdist
                        delta_extrema_x = abs(sample1['max_x'] - sample2['min_x']) / avg_flyingdist
                        if delta_extrema < MAX_DIFF_X_EXTREMA_POS_PCT and delta_extrema_x < MAX_DIFF_X_EXTREMA_POS_PCT:
                                diffX = sample1['maxar'][:,0] - sample2['minar'][:,0]
                                diffY = sample1['maxar'][:,1] - sample2['minar'][:,2]
                                diff = np.c_[diffX,diffY]

                                p = np.power(diff,2)
                                dist = np.sqrt( p[:,0]+p[:,1] )
                                mmax = np.max(dist)
                                mmean = np.sum(dist)/dist.shape[0]
                                # dist = np.sqrt(np.einsum('ij,ij->i',c,c))
                                # print 'compute max - min diff - delta = %s - %s'%(mmax, mmean)
                                if mmax < THRESHOLD_MAX_DIFF and mmean < THRESHOLD_MEAN_DIFF :
                                        return 1

                if 'minar' in sample1 and 'maxar' in sample2:
                        delta_extrema = abs(sample1['min'] + sample2['max']) / avg_flyingdist
                        delta_extrema_x = abs(sample1['min_x'] - sample2['max_x']) / avg_flyingdist
                        if delta_extrema < MAX_DIFF_X_EXTREMA_POS_PCT and delta_extrema_x < MAX_DIFF_X_EXTREMA_POS_PCT:
                                diffX = sample1['minar'][:,0] - sample2['maxar'][:,0]
                                diffY = sample1['minar'][:,2] - sample2['maxar'][:,1]
                                diff = np.c_[diffX,diffY]

                                p = np.power(diff,2)
                                dist = np.sqrt( p[:,0]+p[:,1] )
                                mmax = np.max(dist)
                                mmean = np.sum(dist)/dist.shape[0]
                                # dist = np.sqrt(np.einsum('ij,ij->i',c,c))
                                # print 'compute max - min diff - delta = %s - %s'%(mmax, mmean)
                                if mmax < THRESHOLD_MAX_DIFF and mmean < THRESHOLD_MEAN_DIFF :
                                        return 2

                if 'minar' in sample1 and 'minar' in sample2:
                        delta_extrema = abs(sample1['min'] + sample2['min'])/ avg_flyingdist
                        delta_extrema_x = abs(sample1['min_x'] - sample2['min_x']) / avg_flyingdist
                        if delta_extrema < MAX_DIFF_X_EXTREMA_POS_PCT and delta_extrema_x < MAX_DIFF_X_EXTREMA_POS_PCT:
                                diffX = sample1['minar'][:,0] - sample2['minar'][:,0]
                                diffY = sample1['minar'][:,1] - sample2['minar'][:,1]
                                diff = np.c_[diffX,diffY]

                                p = np.power(diff,2)
                                dist = np.sqrt( p[:,0]+p[:,1] )
                                mmax = np.max(dist)
                                mmean = np.sum(dist)/dist.shape[0]
                                # dist = np.sqrt(np.einsum('ij,ij->i',c,c))
                                # print 'compute max - min diff - delta = %s - %s'%(mmax, mmean)
                                if mmax < THRESHOLD_MAX_DIFF and mmean < THRESHOLD_MEAN_DIFF :
                                        return 3

                return -1

        def plotSimilarTrips(self):
                if not hasattr(self,'sim_trip_groups'):
                        self.computeSimilarTrips()

                print 'num groups is : %s'%len(self.sim_trip_groups)
                for i,group in enumerate(self.sim_trip_groups):
                        print 'Group %s : %s'%(i,group)
                        self.plotTrajectory(group)
                
                plt.show()


        # FOR PLOTTING DATA
        def plotTrajectory(self, ids, show = False):
                if isinstance(ids, int):
                        ids = [ids]

                plt.figure()
                # plt.subplot(311)
                idscsv = [x+1 for x in ids]
                plt.title('%s'%idscsv)
                for id in ids:
                        trip = self.nptrips[id]
                        plt.plot(trip[:,1], trip[:,2])
                plt.grid()

                # plt.subplot(312)
                # for id in ids:
                #       trip = self.nptrips[id]
                #       plt.plot(trip[:,0], trip[:,4], 'r')
                # plt.grid()

                # ax1 = plt.subplot(313)
                # ax2 = ax1.twinx()
                # ax1.grid()
                # for id in ids:
                #       trip = self.nptrips[id]
                #       ax1.plot(trip[:,0], trip[:,5], 'r')
                #       ax2.plot(trip[:,0], trip[:,6], 'g')
                # ax1.set_xlabel('time (s)')
                # ax1.set_ylabel('Speed', color='r')
                # for tl in ax1.get_yticklabels():
                #       tl.set_color('r')
                # ax2.grid()
                # ax2.set_ylabel('acc', color='g')
                # for tl in ax2.get_yticklabels():
                #       tl.set_color('g')


                if show: plt.show()

        def plotTrajCurv(self, ids, show = False):
                if isinstance(ids, int):
                        ids = [ids]

                colors = ['magenta', 'red', 'orange', 'yellow', 'green', 'lightblue', 'darkblue']
                # colors = ['r', 'g', 'b', 'm', 'k', '#808080', 'p']
                plt.figure()
                plt.title('%s'%ids)
                for id in ids:
                        trip = self.nptrips[id]
                        cint = trip[:, self.headers['K_int']]
                        for kp in CURV_TRONCON:
                                pp = cint==kp
                                mode = '.%s'%colors[kp]
                                print mode
                                plt.plot(trip[pp,1], trip[pp,2], '.', color=colors[kp])
                plt.grid()
                if show: plt.show()

# dd=pd.load_driver()
# dd.plotTrajectory([9, 10,16, 18])
# a1 = dd.getSampledTrajAroundMax(dd.nptrips[16])
# a2 = dd.getSampledTrajAroundMax(dd.nptrips[10])

# dd.compareSampleTrajDist(a1, a2)





