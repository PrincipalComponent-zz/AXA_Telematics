# Trip matching routine

This documents the RDP based trip matching

# How to Generate the Solution
   The trip matching was done on 7 Google Compute n1-highcpu-2 machines  (1.8 GB memory) for a total of 14 nodes, run over approximately 14 days
   Python, Numpy, and Matplotlib must be loaded onto the machine  (note matplotlib can be commented out, it is just for visualization)
   
   The code supplied is set up to run on Windows.   To run on linux the \ needs to be changed to /
   
   To run
   
      -  First compile the search_matches.f90 using f2py
           the script is contained in build_it.bat
   
   
      -  Launch  Initial_Processing.py
           this will generate RDP solutions for all 15 RDP tolerances.  It will take approximately 200 CPU days.   Different drivers
           can be run in parallel by changing this line
           
           Realistically I recommend cutting the RDP 7, 8 from the run since they added little value.  We have included it in this code
           set since it was in our final submission.
           
           for driver_id in range(1,3613):
           
           to only run a subset of drivers, and then run different subsets on different nodes.  For instance, if running on 6 nodes
           
           for driver_id in range(1,3613,6):
           for driver_id in range(2,3613,6):
           for driver_id in range(3,3613,6):
           for driver_id in range(4,3613,6):
           for driver_id in range(5,3613,6):
           for driver_id in range(6,3613,6):
           
           on the 6 different instances
           
           
           
           Note, this line
               Input_Path =   "..\\..\\..\\drivers_raw\\" 
           must be pointing at the 5 GB of raw data
           
           
           
           
         After Initial_Processing.py is run,   run  Final_Submission.py
            this will combine the results from the 15 folders of RDP results into 15 files of RDP results such as
               Final_Results_11m_New.csv
               Final_Results_12m_New.csv
               Final_Results_13m_New.csv
               
            which can be put in the ensembling
            
            (Note, in our final submission, the RDP 7m results had only run about 30% through, and RDP 11m results had been pasted in
            so that we didn't get a bunch of zeros for incomplete drivers.   However the 7m, 8, RDP results did not contribute significantly 
            to the score, so could be cut)
