# Script to plot SC errror versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

def getSCErrors(data, voltage, starttime):
    scErrors = []
    scWordCounts = []
    Timestamps = []
    hasL1As = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_TID.py::test_streamCompareLoop[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    info = np.array(data[i]['tests'][j]['metadata']['word_err_count'])
                    scErrors.append(np.array([int(x) for x in info[:,2]]))
                    scWordCounts.append(np.array([int(x) for x in info[:,1]]))
                    Timestamps.append(np.array(info[:,0]))
                    hasL1As.append(np.array(data[i]['tests'][j]['metadata']['HasL1A']))
    indexesErrCnt = [[j for j in range(len(scErrors[i])-1) if scErrors[i][j] > scErrors[i][j+1]] for i in range(len(scErrors))]
    indexesWordCnt = [[j for j in range(len(scWordCounts[i])-1) if scWordCounts[i][j] > scWordCounts[i][j+1]] for i in range(len(scWordCounts))]
    for i in range(len(scWordCounts)):
        for j in range(len(scWordCounts[i])):
            if len(indexesWordCnt[i]) != 0:
                if j > indexesWordCnt[i][0]:
                    scWordCounts[i][j] = (scWordCounts[i][j] + (2**32-1))
    for i in range(len(scErrors)):
        for j in range(len(scErrors[i])):
            if len(indexesErrCnt[i]) != 0:
                if j > indexesErrCnt[i][0]:
                    scErrors[i][j] = (scErrors[i][j] + (2**32-1))
    totalWords0 = []
    totalWords7 = []
    totalWords67 = []
    for i in range(len(scWordCounts)):
        x1 = scWordCounts[i][hasL1As[i]==0]
        x2 = scWordCounts[i][hasL1As[i]==7] - scWordCounts[i][hasL1As[i]==0][-1]
        x3 = scWordCounts[i][hasL1As[i]==67] - scWordCounts[i][hasL1As[i]==7][-1]
        totalWords0.append(x1[-1])
        totalWords7.append(x2[-1])
        totalWords67.append(x3[-1])
    totalWords0 = np.array(totalWords0)
    totalWords7 = np.array(totalWords7)
    totalWords67 = np.array(totalWords67)
    totalErrs0 = []
    totalErrs7 = []
    totalErrs67 = []
    for i in range(len(scErrors)):
        x1 = scErrors[i][hasL1As[i]==0]
        x2 = scErrors[i][hasL1As[i]==7] - scErrors[i][hasL1As[i]==0][-1]
        x3 = scErrors[i][hasL1As[i]==67] - scErrors[i][hasL1As[i]==7][-1]
        totalErrs0.append(x1[-1])
        totalErrs7.append(x2[-1])
        totalErrs67.append(x3[-1])
    totalErrs0 = np.array(totalErrs0)
    totalErrs7 = np.array(totalErrs7)
    totalErrs67 = np.array(totalErrs67)
    errRate0 = totalErrs0/totalWords0
    errRate7 = totalErrs7/totalWords7
    errRate67 = totalErrs67/totalWords67
    mradDose0 = []
    mradDose7 = []
    mradDose67 = []
    for i in range(len(Timestamps)):
        x1 = Timestamp2MRad(Timestamps[i][hasL1As[i]==0],starttime)
        x2 = Timestamp2MRad(Timestamps[i][hasL1As[i]==7],starttime)
        x3 = Timestamp2MRad(Timestamps[i][hasL1As[i]==67],starttime)
        mradDose0.append(x1[-1])
        mradDose7.append(x2[-1])
        mradDose67.append(x3[-1])
    mradDose0 = np.array(mradDose0)
    mradDose7 = np.array(mradDose7)
    mradDose67 = np.array(mradDose67)
    
    return errRate0, errRate7, errRate67, mradDose0, mradDose7, mradDose67

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
        "errRate0": getSCErrors(data, volt,starttime)[0],
        "errRate7": getSCErrors(data, volt,starttime)[1],
        "errRate67": getSCErrors(data, volt, starttime)[2],
        "mradDose0": getSCErrors(data, volt, starttime)[3],
        "mradDose7": getSCErrors(data, volt, starttime)[4],
        "mradDose67": getSCErrors(data, volt, starttime)[5],
    } for volt in voltages
}
    # Plotting

    plots = create_plot_path(args.path+ '/' + 'sc_error_vs_tid_plots')

    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):
        axs[i].scatter(scErrors[volt]["mradDose0"], scErrors[volt]["errRate0"])
        axs[i].scatter(scErrors[volt]["mradDose7"], scErrors[volt]["errRate7"])
        axs[i].scatter(scErrors[volt]["mradDose67"], scErrors[volt]["errRate67"])
        axs[i].set_title(f"{volt}")
        axs[i].set_ylabel('Error Rate')
        axs[i].set_xlabel('TID (MRad)')
        axs[i].set_yscale('log')
        # set these limits later
        axs[i].set_ylim(10**-11,1)
        # axs[i].set_xlim(0,660)
    for ax in axs.flat:
        ax.label_outer()
    fig.savefig(f'{plots}/summary_word_err_err_rate_results.png')
    
    titles = ['08', '11', '14', '20', '26', '29', '32']
    for i, (volt) in enumerate(voltages):
        plt.scatter(scErrors[volt]["mradDose0"], scErrors[volt]["errRate0"])
        plt.scatter(scErrors[volt]["mradDose7"], scErrors[volt]["errRate7"])
        plt.scatter(scErrors[volt]["mradDose67"], scErrors[volt]["errRate67"])
        plt.title(f"{volt}V")
        plt.ylabel('Error Rate')
        plt.xlabel("TID (MRad)")
        plt.ylim(10**-11,1)
        plt.yscale('log')
        plt.savefig(f'{plots}/err_rate_results_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()
