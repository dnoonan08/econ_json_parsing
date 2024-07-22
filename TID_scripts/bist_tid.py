# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

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

    plots = create_plot_path(args.path+ '/' + 'bist_vs_tid_plots-%s'%args.chip)


    bist_voltages = np.arange(0.9,1.20,0.01)
    timestamps = []
    obResults = []
    ppResults = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'test_TID.py::test_bist' in data[i]['tests'][j]['nodeid']:
                if 'metadata' in data[i]['tests'][j]:
                    obResults.append(data[i]['tests'][j]['metadata']['obResults'])
                    ppResults.append(data[i]['tests'][j]['metadata']['ppResults'])
                    timestamps.append(data[i]['tests'][j]['metadata']['timestamps'])
    obResults = np.array(obResults)
    ppResults = np.array(ppResults)
    timestamps = np.array(timestamps)

    obBIST = {
    bist_voltages[i]: {
            "obResults": obResults[:,i],
            "mRadDose": Timestamp2MRad(timestamps[:,i],starttime),
            "plotDose": np.array(list(Timestamp2MRad(timestamps[:,i],starttime))+[(Timestamp2MRad(timestamps[:,i],starttime)[-1]-Timestamp2MRad(timestamps[:,i],starttime)[-2])+Timestamp2MRad(timestamps[:,i],starttime)[-1]])
        } for i in range(len(bist_voltages))
    }
    ppBIST = {
        bist_voltages[i]: {
            "ppResults": ppResults[:,i],
            "mRadDose": Timestamp2MRad(timestamps[:,i],starttime),
            "plotDose": np.array(list(Timestamp2MRad(timestamps[:,i],starttime))+[(Timestamp2MRad(timestamps[:,i],starttime)[-1]-Timestamp2MRad(timestamps[:,i],starttime)[-2])+Timestamp2MRad(timestamps[:,i],starttime)[-1]])
        } for i in range(len(bist_voltages))
    }

    pp_bist = []
    for volt in bist_voltages:
        temp1 = []
        for i in range(len(ppBIST[volt]['ppResults'])):
            temp2 = []
            for j in range(4):
                for k in range(12):
                    temp2.append((ppBIST[volt]['ppResults'][i][j]>> k) & 0b1)
            temp1.append(temp2)
        pp_bist.append(temp1)
    pp_bist = np.array(pp_bist)
    for i in range(len(pp_bist)):
        pp_bist[i] = pp_bist[i].reshape(-1,48)
        pp_bist[i] = pp_bist[i][:,[range(i,48,12) for i in range(12)]].reshape(-1,48)

    ob_bist = []
    for volt in bist_voltages:
        temp1 = []
        for i in range(len(obBIST[volt]['obResults'])):
            temp2 = []
            for j in range(4):
                for k in range(12):
                    temp2.append((obBIST[volt]['obResults'][i][j]>> k) & 0b1)
            temp1.append(temp2)
        ob_bist.append(temp1)
    ob_bist = np.array(ob_bist)
    for i in range(len(ob_bist)):
        ob_bist[i] = ob_bist[i].reshape(-1,48)
        ob_bist[i] = ob_bist[i][:,[range(i,48,12) for i in range(12)]].reshape(-1,48)

    fig,axs=plt.subplots(figsize=(45,30),ncols=6,nrows=5, layout="constrained")

    plotVolts = bist_voltages.reshape(5,6)
    for j in range(6):
        for i in range(5):
            if i == 0:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
            if i == 1:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j+5].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
            if i == 2:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j+10].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
            if i == 3:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j+15].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
            if i == 4:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j+20].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
    for ax in axs.flat:
        ax.label_outer()

    fig.savefig(f'{plots}/pp_bist.png', dpi=300, facecolor="w") 


    fig,axs=plt.subplots(figsize=(45,30),ncols=6,nrows=5, layout="constrained")
    plotVolts = bist_voltages.reshape(5,6)
    for j in range(6):
        for i in range(5):
            if i == 0:
                a,b = np.meshgrid(obBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = ob_bist[j].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(obBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('OB Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
            if i == 1:
                a,b = np.meshgrid(obBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = ob_bist[j+5].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(obBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('OB Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
            if i == 2:
                a,b = np.meshgrid(obBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = ob_bist[j+10].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(obBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('OB Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
            if i == 3:
                a,b = np.meshgrid(obBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = ob_bist[j+15].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(obBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('OB Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
            if i == 4:
                a,b = np.meshgrid(obBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = ob_bist[j+20].T.flatten()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(obBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('OB Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
    for ax in axs.flat:
        ax.label_outer()

    fig.savefig(f'{plots}/ob_bist.png', dpi=300, facecolor="w") 

    ppMin = []
    for j in range(4):
        temp3 = []
        for i in range(len(ppResults)):
            if len(bist_voltages[np.argwhere((ppResults[i,:,j] < 4095))]) != 0:
                temp3.append(bist_voltages[np.argwhere((ppResults[i,:,j] < 4095))[0][0]])
            else:
                temp3.append(0)
        ppMin.append(temp3)

    fig,axs=plt.subplots(figsize=(45,12),ncols=4,nrows=1, layout="constrained")
    for i in range(4):
        axs[i].plot(ppBIST[1.0]['mRadDose'], ppMin[i])
        axs[i].set_xlabel("TID (MRad)")
        axs[i].set_ylabel("Voltage (V)")
        axs[i].set_title(f"PP Minimum Failing Voltage Test {i+1}")
    for ax in axs.flat:
        ax.label_outer()

    fig.savefig(f'{plots}/pp_min_fail.png', dpi=300, facecolor="w")

    obMin = []
    for j in range(4):
        temp4 = []
        for i in range(len(obResults)):
            if len(bist_voltages[np.argwhere((obResults[i,:,j] < 4095))]) != 0:
                temp4.append(bist_voltages[np.argwhere((obResults[i,:,j] < 4095))[0][0]])
            else:
                temp4.append(0)
        obMin.append(temp4)

    fig,axs=plt.subplots(figsize=(45,12),ncols=4,nrows=1, layout="constrained")
    for i in range(4):
        axs[i].plot(obBIST[1.0]['mRadDose'], obMin[i])
        axs[i].set_xlabel("TID (MRad)")
        axs[i].set_ylabel("Voltage (V)")
        axs[i].set_title(f"OB Minimum Failing Voltage Test {i+1}")
    for ax in axs.flat:
        ax.label_outer()

    fig.savefig(f'{plots}/ob_min_fail.png', dpi=300, facecolor="w") 