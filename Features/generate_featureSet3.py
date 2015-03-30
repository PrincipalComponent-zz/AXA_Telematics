# from call_celery import compute_all_drivers

from modules_tai.driver_model import DriverModel
from celery_tasks import load_driver_celery
from celery_tasks import load_driver_aggmat_celery
from config import config
from os import listdir
from os.path import isfile, join
import numpy as np
import time
import csv

from modules_janto.paths import *
     
# path to GPS data         
data_path = DATA       
#data_path = "..\\..\\..\\..\\drivers_raw\\" 

print '\nExtracting feature set 3...\n\n'


NUM_DATA_AGGREGATED = 100
DEBUG = True

def compute_aggmat_drivers():
        drivers = [ f for f in listdir(data_path) if not isfile(join(data_path,f)) ]
        task_ids = []
        if DEBUG: drivers = drivers[0:2] #UNCOMMENT TO TEST IF IT WORKS ONLY FOR THE 2 FIRST DRIVERS
        numtrips = len(drivers) * 200

        dm = DriverModel(1)
        sizemat = len(dm.agg_headers)

        for i in drivers: 
                res = load_driver_aggmat_celery(i)
                task_ids.append(res)

        print "celery tasks created with ids = %s"%task_ids

        res = np.zeros((numtrips, sizemat), dtype='float')
        finished = False
        all_res = {}
        counter = 0
        while not finished:
                found_one = False
                for i,task_id in enumerate(task_ids):
                        result = load_driver_celery(task_id)

                print '%s - counter !'%(counter)
                res[np.arange(counter*200,(counter+1)*200),:] = result.result

                counter += 1
                #del task_ids[i]
                finished = True
                found_one = True
                #break

                #if not found_one : time.sleep(2)

        # RE ORDER
        ss = res[:,0].argsort()
        res = res[ss,:]
        
        if not DEBUG: 
                np.save('res_aggmat.npy', res)
                hhh = ','.join(dm.agg_headers)
                np.savetxt('res_aggmat.csv', res, header = hhh, delimiter = ',', fmt='%8.3f')

        return res


def compute_all_drivers():
        drivers = [ f for f in listdir(data_path) if not isfile(join(data_path,f)) ]
        task_ids = []
        # drivers = drivers[0:2]
        numtrips = len(drivers) * 200

        for i in drivers: 
                res = load_driver_celery.delay(i)
                task_ids.append(res.task_id)

        print "celery tasks created with ids = %s"%task_ids

        res = np.zeros((numtrips, 5), dtype='float')

        finished = False
        all_res = {}
        counter = 0
        while not finished:
                found_one = False
                for i,task_id in enumerate(task_ids):
                        result = load_driver_celery(task_id)
                                
                print '%s - counter !'%(counter)
                res[np.arange(counter*200,(counter+1)*200),:] = result.result

                counter += 1
                #del task_ids[i]
                finished = True
                found_one = True
                #break
                                
                #if not found_one : time.sleep(2)

        # RE ORDER
        import pdb
        pdb.set_trace()
        ss = res[:,1].argsort()
        res = res[ss,:]
        np.save('sim_trajs3.npy', res)
        np.savetxt('sim_trajs3.csv', res)

        return res






output_file = open('featurematrix3.csv','wb')
output_csv = csv.writer(output_file)

for driver in range(1,3613):

   driver_exists = 0
   try:
      file_name = os.path.join(data_path,str(driver) + "\\1.csv")
      test_file = open(file_name,'rb')
      test_file.close()
      driver_exists = 1
   except:
      driver_exists = 0

   if (driver_exists):
      print("doing driver ",driver)
      start_time = time.time()
      results, headers = load_driver_aggmat_celery(driver)
      if (driver ==1):
         output_csv.writerow(headers)
      
      for cnt10, result in enumerate(results):
         for cnt11, feature1 in enumerate(result):
            
            if ('nan' in str(feature1) ):
              #feature1 = 0.
              results[cnt10][cnt11] = 0.
            #print (str(feature1))
         #sys.exit()
      
      #for result1 in results:
      #  for cnt3, item in enumerate(result1):
      #     if ( 'nan' in result1[cnt3] ):
      #        result1[cnt3] = 0.
      #     else:
      #        result1[cnt3] = round( result1[cnt3], 3)
      #  output_csv.writerow(result1)
      
      np.savetxt(output_file, results,   delimiter = ',', fmt='%8.3f')
   
      end_time = time.time()
      print "\tTime elapsed ",end_time - start_time