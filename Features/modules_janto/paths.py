# -*- coding: utf-8 -*-
"""
(c) 2015

@author:    Janto Oellrich
email:      joellrich@uos.de

CONTENT
    Imports PATH variables to major folders stored in SETTINGS.json
"""
import json
import os

# path to SETTINGS.json file (in parent directory)
file_dir = os.path.dirname(__file__) +'\\..\\..\\SETTINGS.json'

# import paths
PATHS = json.loads(open(file_dir).read())
# get parent folder
ROOT = PATHS["ROOT"]
# build path to parent folder
DATA = PATHS["DATA"]


# path to feature folder
FEATURES = os.path.join(ROOT,'Features')
# path to model outputs
MODELS = os.path.join(ROOT,'Models')

# Prompt information
print '\nImported PATH variables from SETTINGS.json\n'

print '\tThese are the major folders...\n\n'

print '\t', PATHS["ROOT"]
print '\t', PATHS["DATA"]
print '\t', MODELS
print '\t', FEATURES, '\n\n\n'



