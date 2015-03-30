# Feature extraction

To extract the 3 feature sets we used, simply run

     extract_features
     
This will create `featurematrix1.csv`,`featurematrix2.csv` and `featurematrix3.csv`. 
You can also create the individual files by executing `python generate_featureSet1.py` (e.g. for featureset 1).

You can create `featurematrix2.csv` and `featurematrix3.csv` right away. `featurematrix1.csv` relies on the the GPS
data in .npy format, so run `python csvToNpy.py` before you create it 
(if you run extract_features this step is included).

# Modelling

To train the models individually execute one or more of the following blocks

    // feature set 2
    python breakup_inputFile.py
    python train_featureSet2.py
    python combine_outputFiles.py

    // feature set 1 (training and evaluation on all trips)
    python train_featureSet1.py

    // feature set 1 and 3
    python combine_featureset1and3.py
    python breakup_inputFile_1and3.py
    python train_featureSet1and3.py
    python combine_outputFiles_1and3.py

    // feature set 3
    python breakup_inputFile_3.py (only needs to be called once for GBM and Forest)

    // feature set 3: Random Forest
    python train_Forest_featureSet3.py
    python combine_output_files_Forest.py

    // feature set 3: GBM
    python train_GBM_featureSet3.py
    combine_output_files_GBM.py
