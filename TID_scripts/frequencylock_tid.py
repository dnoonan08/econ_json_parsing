# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

def getMinMaxLockingFreq(data, voltage):
    minFreq = []
    maxFreq = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_TID.py::test_pllautolock[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    minFreq.append(data[i]['tests'][j]['metadata']['min_freq'])
                    maxFreq.append(data[i]['tests'][j]['metadata']['max_freq'])
    minFreq = np.array(minFreq)
    maxFreq = np.array(maxFreq)
    mradDose = FNames2MRad(fnames)
    return minFreq, maxFreq, mradDose

if __name__ == '__main__':
    # argument parser
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--path', type = str) # repo name on github json repo
    parser.add_argument('--chip', default = 'chip003') # repo name on github json repo
    args = parser.parse_args()

    # Path to JSONs
    path = args.path + '/' + args.chip + '/'
    print(f"Running on {path}")

    # Fetch JSON data and startime of first JSON
    data, starttime = get_data(path)
    fnames = get_fnames(path)


    # Plotting

    plots = create_plot_path(args.path+ '/' + 'frequencylock_vs_tid_plots')

    MinMaxLockingFreq = {
    volt: {
        'minFreq': getMinMaxLockingFreq(data, volt)[0],
        'maxFreq': getMinMaxLockingFreq(data, volt)[1],
        'mradDose': getMinMaxLockingFreq(data, volt)[2],
    } for volt in voltages
}

    titles = ['08', '11', '14', '20', '26', '29', '32']
    for i, (volt) in enumerate(voltages):
        plt.plot(MinMaxLockingFreq[volt]['mradDose'], MinMaxLockingFreq[volt]['maxFreq'])
        plt.title(f"Maximum Locking Frequency at {volt}V")
        plt.xlabel("TID (MRad)")
        plt.ylabel("Frequency (MHz)")
        #plt.ylim(43,47)
        plt.savefig(f'{plots}/max_locking_freq_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()
    
    for i, (volt) in enumerate(voltages):
        plt.plot(MinMaxLockingFreq[volt]['mradDose'], MinMaxLockingFreq[volt]['minFreq'])
        plt.title(f"Minimum Locking Frequency at {volt}V")
        plt.xlabel("TID (MRad)")
        plt.ylabel("Frequency (MHz)")
        #plt.ylim(43,47)
        plt.savefig(f'{plots}/min_locking_freq_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()

    fig,axs=plt.subplots(figsize=(55,12),ncols=7,nrows=2, layout="constrained")
    for j, (volt) in enumerate(voltages):
        for i in range(2):
            if i == 0:
                axs[i,j].plot(MinMaxLockingFreq[volt]['mradDose'], MinMaxLockingFreq[volt]['maxFreq'])
                axs[i,j].set_title(f"Maximum Locking Frequency at {volt}V")
                axs[i,j].set_xlabel("TID (MRad)")
                axs[i,j].set_ylabel("Frequency (MHz)")
                #axs[i,j].set_ylim(43,47)
            if i == 1:
                axs[i,j].plot(MinMaxLockingFreq[volt]['mradDose'], MinMaxLockingFreq[volt]['minFreq'])
                axs[i,j].set_title(f"Minimum Locking Frequency at {volt}V")
                axs[i,j].set_xlabel("TID (MRad)")
                axs[i,j].set_ylabel("Frequency (MHz)")
                #axs[i,j].set_ylim(34,38)
    for ax in axs.flat:
            ax.label_outer()

    fig.savefig(f'{plots}/min_max_locking_freq.png', dpi=300, facecolor="w") 