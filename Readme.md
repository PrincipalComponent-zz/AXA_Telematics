# AXA Driver Telematics Analysis
## 2nd prize winning solution

Team:                    **Driving It**

Team members:            Scott H, TheKeymaker, Dr. Gigabit

This repository contains our 2nd prize winning solution to [**AXA Driver Telematics Analysis competition**](https://www.kaggle.com/c/axa-driver-telematics-analysis) 
hosted on kaggle.com.

The goal of this challenge was to infer from unlabeled GPS data whether a trip was driven by a given driver or not.
The dataset provided by AXA comprised around half a million trips by roughly 2700 drivers.

***

# How to generate the solution

In order to replicate the winning solution, just follow the few steps below.

If you do not have the raw GPS data, get it here

[http://www.kaggle.com/c/axa-driver-telematics-analysis/data](http://www.kaggle.com/c/axa-driver-telematics-analysis/data)

Change the `"DATA"` path in the file `SETTINGS.json` to point to your data folder, and the `"ROOT"` path
to match the parent folder of the cloned repository, e.g.

     {
        "DATA": "C:/users/user/FinalSubmission/drivers",
        "ROOT": "C:/users/user/FinalSubmission/"
     }
     

## Telematics

For the telematics part, we first extracted the 3 feature sets and then trained our various models on them.

### Feature Extraction

To extract the features, go to the `Features` folder and run 

      extract_features

This will create the three feature matrices `featurematrix1.csv`,  `featurematrix2.csv `and  `featurematrix3.csv`. You can also create the matrices individually by running (e.g. for feature set 1)

      python generate_featureSet1.py

### Modelling

All our models can be run by

     train

The 6 individual models are written to the `Models` folder and are in a submittable format.



## Trip Matching

To run our trip matching routine `cd` to the `RDP_Trip_Matching` folder and execute

    Run_Trip_Matching
    
Detailed instructions can be found in the folder's README.md

## Ensemble final solution

To ensemble the trip matching results and the telematics models `cd` to the `Create_Ensemble` folder and execute

    generate_Solution
