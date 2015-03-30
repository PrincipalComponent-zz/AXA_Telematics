# AXA Driver Telematics Analysis
## 2nd prize winning solution

Team:                    **Driving It**

Team members:            Scott H, TheKeymaker, Dr. Gigabit

This repository contains our 2nd prize winning solution to [**AXA Driver Telematics Analysis competition**](https://www.kaggle.com/c/axa-driver-telematics-analysis) 
hosted on kaggle.com.

The goal of this challenge was to infer from unlabeled GPS data whether a trip was driven by a given driver or not.
The dataset provided by AXA comprised around half a million trips by roughly 2700 drivers.

***

# Summary

We tackled the problem by combining the results of a trip matching algorithm and driver signature models. The objective was to identify frequently taken trips as they are likely to be trips from the respective driver and apply supervised models to telematic features extracted from GPS data to produce probabilistic output. We built ensembles of different models in both streams and one factor that was probably responsible for our success was the extensive combination of these solutions.

Trip matching was based on an ensemble of runs of the Douglas-Peucker algorithm applied at different sensitivities.
  Our final telematics model consisted of an ensemble of 6 different models. We mainly used Random Forests, in combination with Gradient Boosting and Logistic Regression. We trained models on different feature sets and combinations of those feature sets. For each feature set we selected the algorithm (out of our candidates) that yielded the best result on the LB as we expected the LB to be quite informative in this competition. The weights for the ensemble we choose arbitrarily informed by the performance of the individual models.

These are the models we used for the winning solution:

1.  Gradient Boosting Machine (feature set 3)
1.  Random Forest (feature set 3)
1.  An ensemble of Random Forest and Logistic Regression (feature set 1)
1.  Random Forest  (feature sets 1 and 3 combined)
1.  GBM in R (feature set 3)
1.  Random Forest (feature set 2)

The final telematics model did pretty well and scored 0.91375 (Private score). In combination with our trip matching we increased the final AUC score of 0.97398 which ensured us 2nd place.

![](https://cloud.githubusercontent.com/assets/8686177/6716565/4ceac948-cd9e-11e4-9eb7-12fe8158a100.png)

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

The 6 individual models are written to the `Models` folder and are in a submittable format. The file
`train_GBM_R.R` has to be run independently (change the marked path inside the file before running).



## Trip Matching

To run our trip matching routine `cd` to the `RDP_Trip_Matching` folder and execute

    Run_Trip_Matching
    
Detailed instructions can be found in the folder's README.md

## Ensemble final solution

To ensemble the trip matching results and the telematics models `cd` to the `Create_Ensemble` folder and execute

    generate_Solution
