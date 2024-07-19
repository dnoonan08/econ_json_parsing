# Script to plot SC errror versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

def getSCErrors(data, voltage,starttime):
    scErrors = []
    scWordCounts = []
    Timestamps = []
    hasL1As = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_TID.py::test_streamCompareLoop[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    info = np.array(data[i]['tests'][j]['metadata']['word_err_count'])
                    scErrors.append([int(x) for x in info[:,2]])
                    scWordCounts.append([int(x) for x in info[:,1]])
                    Timestamps.append(info[:,0])
                    hasL1As.append(data[i]['tests'][j]['metadata']['HasL1A'])
    scError = np.array([x for xs in scErrors for x in xs])
    scWordCount = np.array([x for xs in scWordCounts for x in xs])
    hasL1A = np.array([x for xs in hasL1As for x in xs])
    Timestamp = np.array([x for xs in Timestamps for x in xs])
    mradDose = Timestamp2MRad(Timestamp,starttime)
    return scError, scWordCount, hasL1A, mradDose

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

    scErrors = {
    volt: {
        "scErrors": getSCErrors(data, volt,starttime)[0],
        "scWordCount": getSCErrors(data, volt,starttime)[1],
        "hasL1A": getSCErrors(data, volt,starttime)[2],
        "mradDose": getSCErrors(data, volt,starttime)[3],
    } for volt in voltages
}
    # Plotting

    plots = create_plot_path(args.path+ '/' + 'sc_error_vs_tid_plots')

    fig,axs=plt.subplots(figsize=(45,12),ncols=7,nrows=3, layout="constrained")
    for i, (volts) in enumerate(voltages):
        for j in range(3):
            if j==2:
                axs[j,i].scatter(scErrors[volts]["mradDose"][scErrors[volts]["hasL1A"]==1], (scErrors[volts]["scErrors"]/scErrors[volts]["scWordCount"])[scErrors[volts]["hasL1A"]==1], label = "errors w l1a", color = "r") 
                axs[j,i].scatter(scErrors[volts]["mradDose"][scErrors[volts]["hasL1A"]==0], (scErrors[volts]["scErrors"]/scErrors[volts]["scWordCount"])[scErrors[volts]["hasL1A"]==0], label = "errors w/o l1a",facecolors='none', edgecolors='b')
                axs[j,i].set_ylabel("Error Rate")
                axs[j,i].set_xlabel("TID (MRad)")
                axs[j,i].set_title(f"{volts} V")
                #axs[i,j].set_yscale("log")
                # axs[i,j].set_ylim((1e-8,1.1))
                # axs[i,j].set_xlim(0,660)
            if j==1:
                axs[j,i].scatter(scErrors[volts]["mradDose"][scErrors[volts]["hasL1A"]==1], (scErrors[volts]["scWordCount"])[scErrors[volts]["hasL1A"]==1], label = "errors w l1a", color = "r") 
                axs[j,i].scatter(scErrors[volts]["mradDose"][scErrors[volts]["hasL1A"]==0], (scErrors[volts]["scWordCount"])[scErrors[volts]["hasL1A"]==0], label = "errors w/o l1a",facecolors='none', edgecolors='b')
                axs[j,i].set_ylabel("Word Count")
                axs[j,i].set_xlabel("TID (MRad)")
                axs[j,i].set_title(f"{volts} V")
                #axs[i,j].set_yscale("log")
                # axs[i,j].set_ylim((1e-8,1.1))
                # axs[i,j].set_xlim(0,660)
            if j==0:
                axs[j,i].scatter(scErrors[volts]["mradDose"][scErrors[volts]["hasL1A"]==1], (scErrors[volts]["scErrors"])[scErrors[volts]["hasL1A"]==1], label = "errors w l1a", color = "r") 
                axs[j,i].scatter(scErrors[volts]["mradDose"][scErrors[volts]["hasL1A"]==0], (scErrors[volts]["scErrors"])[scErrors[volts]["hasL1A"]==0], label = "errors w/o l1a",facecolors='none', edgecolors='b')
                axs[j,i].set_ylabel("Error Count")
                axs[j,i].set_xlabel("TID (MRad)")
                axs[j,i].set_title(f"{volts} V")
                #axs[i,j].set_yscale("log")
                # axs[i,j].set_ylim((1e-8,1.1))
                # axs[i,j].set_xlim(0,660)
    for ax in axs.flat:
        ax.label_outer()
    fig.savefig(f'{plots}/summary_word_err_err_rate_results.png')