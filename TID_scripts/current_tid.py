# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt



def getCurrentValues(data, voltage,starttime):
    currents = []
    hasL1As = []
    Timestamps = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_TID.py::test_streamCompareLoop[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    currents.append(data[i]['tests'][j]['metadata']['Current'])
                    hasL1As.append(data[i]['tests'][j]['metadata']['HasL1A'])
                    Timestamps.append(data[i]['tests'][j]['metadata']['Timestamp'])
    current = np.array([x for xs in currents for x in xs])
    hasL1A = np.array([x for xs in hasL1As for x in xs])
    Timestamp = np.array([x for xs in Timestamps for x in xs])
    mradDose = Timestamp2MRad(Timestamp,starttime)
    return current, hasL1A, mradDose


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

    currents = {
        volt: {
        "current": getCurrentValues(data, volt,starttime)[0],
        "hasL1A": getCurrentValues(data, volt,starttime)[1],
        "mradDose": getCurrentValues(data, volt,starttime)[2],
        }    for volt in voltages
    }

    # Plotting

    plots = create_plot_path('current_vs_tid')

    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):
        axs[i].scatter(currents[volt]["mradDose"][currents[volt]["hasL1A"]==0], currents[volt]["current"][currents[volt]["hasL1A"]==0])
        axs[i].scatter(currents[volt]["mradDose"][currents[volt]["hasL1A"]==7], currents[volt]["current"][currents[volt]["hasL1A"]==7])
        axs[i].scatter(currents[volt]["mradDose"][currents[volt]["hasL1A"]==67], currents[volt]["current"][currents[volt]["hasL1A"]==67])

        axs[i].set_title(f"{volt}")
        axs[i].set_ylabel('Current (A)')
        axs[i].set_xlabel('TID (MRad)')
        #set these limits later
        # axs[i].set_ylim(0.15,0.31)
        # axs[i].set_xlim(0,660) 
    for ax in axs.flat:
        ax.label_outer()   
    fig.savefig(f'{plots}/current_vs_tid_results.png', dpi=300, facecolor="w") 

    titles = ['08', '11', '14', '20', '26', '29', '32']
    for i, (volt) in enumerate(voltages):
        plt.scatter(currents[volt]["mradDose"][currents[volt]["hasL1A"]==0], currents[volt]["current"][currents[volt]["hasL1A"]==0], label = 'No L1As')
        plt.scatter(currents[volt]["mradDose"][currents[volt]["hasL1A"]==7], currents[volt]["current"][currents[volt]["hasL1A"]==7], label = '7 L1As per Orbit')
        plt.scatter(currents[volt]["mradDose"][currents[volt]["hasL1A"]==67], currents[volt]["current"][currents[volt]["hasL1A"]==67], label = '67 L1As per Orbit')
        plt.title(f"{volt}V")
        plt.ylabel("Current (A)")
        plt.xlabel("TID (MRad)")
        plt.ylim(0.15,0.41)
        plt.legend()
        plt.savefig(f'{plots}/current_measurement_results_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()






