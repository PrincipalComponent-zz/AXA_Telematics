# Feature extraction

To extract the 3 feature sets we used, simply run

     extract_features
     
This will create `featurematrix1.csv`,`featurematrix2.csv` and `featurematrix3.csv`. 
You can also create the individual files by executing `python generate_featureSet1.py` (e.g. for featureset 1).

You can create `featurematrix2.csv` and `featurematrix3.csv` right away. `featurematrix1.csv` relies on the the GPS
data in .npy format, so run `python csvToNpy.py` before you create it 
(if you run extract_features this step is included).
