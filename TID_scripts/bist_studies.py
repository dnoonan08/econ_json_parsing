# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames
import numpy as np

from temperature_tid import getTemperatureValues

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

    plots = create_plot_path(args.path+ '/' + 'bist_temp_vs_tid_plots-tests-%s'%args.chip)


    bist_voltages = np.arange(0.9,0.91,0.01)
    timestamps = []
    obResults = []
    ppResults = []
    for i in range(1):#range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'test_TID.py::test_bist' in data[i]['tests'][j]['nodeid']:
                if 'metadata' in data[i]['tests'][j]:
                    obResults.append(data[i]['tests'][j]['metadata']['obResults'])
                    ppResults.append(data[i]['tests'][j]['metadata']['ppResults'])
                    timestamps.append(data[i]['tests'][j]['metadata']['timestamps'])
    obResults = np.array(obResults)
    ppResults = np.array(ppResults)
    timestamps = np.array(timestamps)

    ppBIST = {
        bist_voltages[i]: {
            "ppResults": ppResults[:,i],
            "mRadDose": Timestamp2MRad(timestamps[:,i],starttime),
            "plotDose": np.array(list(Timestamp2MRad(timestamps[:,i],starttime))+[(Timestamp2MRad(timestamps[:,i],starttime)[-1]-Timestamp2MRad(timestamps[:,i],starttime)[-2])+Timestamp2MRad(timestamps[:,i],starttime)[-1]])
        } for i in range(len(bist_voltages))
    }

    temperatures = {
    volt: {
        "temperature": getTemperatureValues(data, volt,starttime)[0],
        "hasL1A": getTemperatureValues(data, volt,starttime)[1],
        "mradDose": getTemperatureValues(data, volt,starttime)[2],
        "hasXrays": getTemperatureValues(data, volt,starttime)[3],
        } for volt in voltages
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

    

    fig,axs=plt.subplots(figsize=(45,30),ncols=6,nrows=5, layout="constrained")


    plotVolts = bist_voltages.reshape(5,6)
    for j in range(6):
        for i in range(5):
            if i == 0:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j].T.flatten()
                axs2 = axs[i,j].twinx()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')

                axs2.plot(temperatures[1.2]["mradDose"][temperatures[1.2]["hasXrays"]==1], temperatures[1.2]["temperature"][temperatures[1.2]["hasXrays"]==1], color ='orange', label='1.2 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')

                axs2.plot(temperatures[1.08]["mradDose"][temperatures[1.08]["hasXrays"]==1], temperatures[1.08]["temperature"][temperatures[1.08]["hasXrays"]==1], color ='green', label='1.08 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')



            if i == 1:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j+5].T.flatten()
                axs2 = axs[i,j].twinx()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')


                axs2.plot(temperatures[1.2]["mradDose"][temperatures[1.2]["hasXrays"]==1], temperatures[1.2]["temperature"][temperatures[1.2]["hasXrays"]==1], color ='orange', label='1.2 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')

                axs2.plot(temperatures[1.08]["mradDose"][temperatures[1.08]["hasXrays"]==1], temperatures[1.08]["temperature"][temperatures[1.08]["hasXrays"]==1], color ='green', label='1.08 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')
            if i == 2:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j+10].T.flatten()
                axs2 = axs[i,j].twinx()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')

                axs2.plot(temperatures[1.2]["mradDose"][temperatures[1.2]["hasXrays"]==1], temperatures[1.2]["temperature"][temperatures[1.2]["hasXrays"]==1], color ='orange', label='1.2 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')

                axs2.plot(temperatures[1.08]["mradDose"][temperatures[1.08]["hasXrays"]==1], temperatures[1.08]["temperature"][temperatures[1.08]["hasXrays"]==1], color ='green', label='1.08 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')
            if i == 3:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j+15].T.flatten()
                axs2 = axs[i,j].twinx()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')

                axs2.plot(temperatures[1.2]["mradDose"][temperatures[1.2]["hasXrays"]==1], temperatures[1.2]["temperature"][temperatures[1.2]["hasXrays"]==1], color ='orange', label='1.2 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')

                axs2.plot(temperatures[1.08]["mradDose"][temperatures[1.08]["hasXrays"]==1], temperatures[1.08]["temperature"][temperatures[1.08]["hasXrays"]==1], color ='green', label='1.08 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')
            if i == 4:
                a,b = np.meshgrid(ppBIST[plotVolts[i][j]]["mRadDose"],np.arange(0,12,(12/48)))
                sample = pp_bist[j+20].T.flatten()
                axs2 = axs[i,j].twinx()
                axs[i,j].hist2d(a.flatten(),b.flatten(),weights=sample,bins=(ppBIST[plotVolts[i][j]]['plotDose'],np.arange(0,13,(12/48))),cmap='bwr_r')
                axs[i,j].set_ylim(0,12)
                axs[i,j].set_title(f"{round(plotVolts[i][j],3)}V")
                axs[i,j].set_ylabel('Ping Pong Bist Result')
                axs[i,j].set_xlabel('TID (MRad)')
                axs2.plot(temperatures[1.2]["mradDose"][temperatures[1.2]["hasXrays"]==1], temperatures[1.2]["temperature"][temperatures[1.2]["hasXrays"]==1], color ='orange', label='1.2 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')

                axs2.plot(temperatures[1.08]["mradDose"][temperatures[1.08]["hasXrays"]==1], temperatures[1.08]["temperature"][temperatures[1.08]["hasXrays"]==1], color ='green', label='1.08 volt', alpha=1.0)
                axs2.set_ylabel("Temperature")
                #axs2.patch.set_facecolor('red')
                axs2.patch.set_alpha(0.1)
                axs2.set_ylim(-15,-10)
                axs2.set_xlabel('TID (MRad)')
                plt.legend()


    for ax in axs.flat:
        ax.label_outer()

    fig.savefig(f'{plots}/pp_bist.png', dpi=300, facecolor="w") 


    