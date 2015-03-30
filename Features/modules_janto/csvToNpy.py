"""
(c) 2015

@author:    Janto Oellrich
email:      joellrich@uos.de

CONTENT:
  Converts GPS data files to .npy files and stores them in same driverfolders.    
"""

from modules import *
from paths import *

driverFolder = DATA

print '\nConverting raw .csv files to numpy files...\n'

drivers = sorted([int(folderName) for folderName in os.listdir(driverFolder)])
# Check that we unzipped the archive properly and have all the drivers
try:
    if len(drivers) != 2736:
        raise
except:
    print "Error: {} drivers found instead of 2736".format(len(drivers))
    sys.exit(0)

trips = range(1, 201)

#drivers = drivers[0:4]

# Main loop
for driver in drivers:
    tripsData = []
    for trip in trips:
        tripsData.append(np.loadtxt(os.path.join(driverFolder,"{}\{}.csv".format(driver, trip)), delimiter=',', skiprows=1))

    np.save(os.path.join(driverFolder,str(driver),"trips.npy"), tripsData)
    print "Driver {} done".format(driver)

print "Conversion completed."
