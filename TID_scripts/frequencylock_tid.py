# Script to plot current versus TID 

from common import *
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
import matplotlib as mpl
import matplotlib.pyplot as plt

def getLockingFreqs(data, voltage, starttime):
    auto_locks = []
    timestamp = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_pllautolock[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    auto_locks.append(data[i]['tests'][j]['metadata']['auto_locks'])
                    timestamp.append(data[i]['tests'][j]['metadata']['timestamp'])
    auto_locks = np.array(auto_locks)
    times = np.array([np.datetime64(x) for x in timestamp])
    #mradDose = Timestamp2MRad(timestamp, starttime)
    #hasXrays = Timestamp2XrayBool(timestamp)

    mradDose, hasXrays = datetime_to_TID(times, ObelixDoseRate, xray_start_stop[args.chip])
    mradDose = np.array(mradDose)
    hasXrays = np.array(hasXrays)
    results = {
        'auto_locks': auto_locks,
        'mradDose': mradDose,
        'dosePlots': np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]]),
        'timestamp' : times,
        'timePlots': np.array(list(times)+[(times[-1]-times[-2])+times[-1]]),
        'hasXrays' : hasXrays,
        'hasXraysPlots' : np.array(list(hasXrays)+ [False]),
    }
    return results

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

    plots = create_plot_path(args.path+ '/' + 'frequencylock_vs_tid_plots-%s'%args.chip)

    autoLocks = {
    volt: getLockingFreqs(data, volt, starttime) for volt in voltages
    }

    titles = ['08', '11', '14', '20', '26', '29', '32']
    for i, (volt) in enumerate(voltages):
        b,a =np.meshgrid(np.arange(35, 50+(1/8), (1/8)),np.array(autoLocks[volt]['mradDose'][autoLocks[volt]['hasXrays']==1]))

        d = autoLocks[volt]['auto_locks'][autoLocks[volt]['hasXrays']].flatten()

        print(autoLocks[volt]['mradDose'].shape)
        print(d.shape)
        print(autoLocks[volt]['dosePlots'][autoLocks[volt]['hasXraysPlots']].shape)
        binary_cmap = ListedColormap(['white', '#08306b'])
        plt.hist2d(a.flatten(),b.flatten(),weights=d,bins=(np.array(autoLocks[volt]['dosePlots']),np.arange(35, 51+(1/8), (1/8))),cmap=binary_cmap)
        plt.title(f"{volt}V")
        plt.ylabel("Frequency (MHz)")
        plt.xlabel("TID (MRad)")
        handles, labels = plt.gca().get_legend_handles_labels()
        patch = mpatches.Patch(color='#08306b', label='PLL Locked')
        handles.append(patch)
        plt.legend(handles=handles, loc='upper right')
        plt.savefig(f'{plots}/lockingFreq_1p{titles[i]}V_ECONT.png', dpi=300, facecolor="w")
        plt.clf()

    for i, (volt) in enumerate(voltages):
        b,a =np.meshgrid(np.arange(35, 50+(1/8), (1/8)),np.array(autoLocks[volt]['timestamp']))
        d = autoLocks[volt]['auto_locks'].flatten()
        binary_cmap = ListedColormap(['white', '#08306b'])
        plt.hist2d(a.flatten(),b.flatten(),weights=d,bins=(np.array(autoLocks[volt]['timePlots']),np.arange(35, 51+(1/8), (1/8))),cmap=binary_cmap)
        plt.title(f"{volt}V")
        plt.ylabel("Frequency (MHz)")
        #plt.xlabel("TID (MRad)")
        handles, labels = plt.gca().get_legend_handles_labels()
        patch = mpatches.Patch(color='#08306b', label='PLL Locked')
        handles.append(patch)
        plt.legend(handles=handles, loc='upper right')
        plt.savefig(f'{plots}/lockingFreq_1p{titles[i]}V_ECONT_time.png', dpi=300, facecolor="w")
        plt.clf()



    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):
        b,a =np.meshgrid(np.arange(35, 50+(1/8), (1/8)),np.array(autoLocks[volt]['mradDose'][autoLocks[volt]['hasXrays']==1]))
        d = autoLocks[volt]['auto_locks'][autoLocks[volt]['hasXrays']==1].flatten()
        binary_cmap = ListedColormap(['white', '#08306b'])
        axs[i].hist2d(a.flatten(),b.flatten(),weights=d,bins=(np.array(autoLocks[volt]['dosePlots']),np.arange(35, 51+(1/8), (1/8))),cmap=binary_cmap)
        axs[i].set_ylabel("Frequency (MHz)")
        axs[i].set_xlabel("TID (MRad)")
        axs[i].set_title(f"{volt}V")
        handles, labels = plt.gca().get_legend_handles_labels()
        patch = mpatches.Patch(color='#08306b', label='PLL Locked')
        handles.append(patch)
        axs[i].legend(handles=handles, loc='upper right')
    for ax in axs.flat:
        ax.label_outer()
        
    fig.savefig(f'{plots}/summary_locking_freq.png', dpi=300, facecolor="w")


    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):
        b,a =np.meshgrid(np.arange(35, 50+(1/8), (1/8)),np.array(autoLocks[volt]['timestamp']))
        d = autoLocks[volt]['auto_locks'].flatten()
        binary_cmap = ListedColormap(['white', '#08306b'])
        axs[i].hist2d(a.flatten(),b.flatten(),weights=d,bins=(np.array(autoLocks[volt]['timePlots']),np.arange(35, 51+(1/8), (1/8))),cmap=binary_cmap)
        axs[i].set_ylabel("Frequency (MHz)")
        #axs[i].set_xlabel("TID (MRad)")
        axs[i].set_title(f"{volt}V")
        handles, labels = plt.gca().get_legend_handles_labels()
        patch = mpatches.Patch(color='#08306b', label='PLL Locked')
        handles.append(patch)
        axs[i].legend(handles=handles, loc='upper right')
    for ax in axs.flat:
        ax.label_outer()
        
    fig.savefig(f'{plots}/summary_locking_freq_time.png', dpi=300, facecolor="w")
