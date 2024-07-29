# Script to check validity of reports (or if they were stopped in the middle)

# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

import os

def checkReports(data, voltage):
    fails = []
    for i in range(len(data)):
        counter = 0
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_TID.py::test_pll_capbank_width[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    counter+=1
            if 'crash' in data[i]['tests'][j]['setup']:
                if 'OSError: [Errno 5] Input/output error' in data[i]['tests'][j]['setup']['crash']['message']:
                    fails.append(fnames[i])
        if counter != 1:
            fails.append(fnames[i])
                    
    fails = np.unique(np.array(fails))
    return list(set(fails))

if __name__ == '__main__':
    # argument parser
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--path', type = str) # repo name on github json repo
    parser.add_argument('--chip', default = 'chip003') # repo name on github json repo
    parser.add_argument('--remove', action = 'store_true') # repo name on github json repo
    args = parser.parse_args()

    # Path to JSONs
    path = args.path + '/' + args.chip + '/'
    print(f"Running on {path}")

    # Fetch JSON data and startime of first JSON
    data, starttime = get_data(path)
    fnames = get_fnames(path)



    Checks = {
    volt: {
        "Fails": checkReports(data, volt),
    } for volt in voltages
    }

    for key, value in Checks.items():
        print(key)
        print(value)

        if args.remove:
            for el in value['Fails']:
                cmd = 'rm %s'%el
                print(cmd)
                os.system(cmd)

    
