# Script to run all the chips from the bist-study

import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os


types = ['pp','ob']
chips = ['chip001','chip002-econd','chip003','chip004','chip005-econd']
tests = ['1','2','3','4']


print("Running on all the delta plots")
for t in types:
    for chip in chips:
        for test in tests:
            cmd = 'python3 delta_study.py --chip %s --test %s --type %s'%(chip,test,t)
            os.system(cmd)

print("Done!")