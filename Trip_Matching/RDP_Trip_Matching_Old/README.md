This documents the RDP based trip matching


## Summary

# How to Generate the Solution
   This trip matching was run on windows over several days.  It could be run on a linux server.
   Python, Numpy, and Matplotlib must be loaded onto the machine  (note matplotlib can be commented out, it is just for visualization)
   
   The code supplied is set up to run on Windows .   To run on linux the fortran needs to be recompiled
   
   To run
   
      -  First compile the search_matches.f90 using f2py
           the script is contained in build_it.bat
   
   
      -  Launch  Initial_Processing.py
           this will generate RDP solutions for all 3 RDP tolerances.     Different drivers
           can be run in parallel by changing this line.   
           
           
           for driver_id in range(1,3613):
           
           to only run a subset of drivers, and then run different subsets on different nodes.  For instance, if running on 6 nodes
           
           for driver_id in range(1,3613,6):
           for driver_id in range(2,3613,6):
           for driver_id in range(3,3613,6):
           for driver_id in range(4,3613,6):
           for driver_id in range(5,3613,6):
           for driver_id in range(6,3613,6):
           
           on the 6 different instances
           
           
           
           the data is read from the settings.json file
           
           
           
           
         After Initial_Processing.py is run,   run  Final_Submission.py
            this will combine the results from the 3 folders of RDP results into 3 files of RDP results such as
               Final_Results_13m.csv
               Final_Results_15m.csv
               Final_Results_17m.csv
               
            which can be put in the ensembling.   These files will be put in the FinalSubmission/Trip_Matching Directory
            
            (Note, in our final submission, the RDP 7m results had only run about 30% through, and RDP 11m results had been pasted in
            so that we didn't get a bunch of zeros for incomplete drivers.   However the 7m, 8, RDP results did not contribute significantly 
            to the score, so could be cut)
