# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames
import numpy as np
import glob
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
                if f"test_streamCompareLoop[{voltage}]" in data[i]['tests'][j]['nodeid']:
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
    fnames = list(np.sort(glob.glob(f"{path_to_json}/report*.json")))
    # Path to JSONs
    path = args.path + '/' + args.chip + '/'
    print(f"Running on {path}")

    # Fetch JSON data and startime of first JSON
    data, starttime = get_data(path)
    fnames = get_fnames(path)

    ECOND = True
    if 'ECONT' in fnames[0]:
        ECOND = False

    currents = {
        volt: {
        "current": getCurrentValues(data, volt,starttime)[0],
        "hasL1A": getCurrentValues(data, volt,starttime)[1],
        "mradDose": getCurrentValues(data, volt,starttime)[2],
        }    for volt in voltages
    }

    # Plotting

    plots = create_plot_path(args.path+ '/' + 'current_vs_tid_plots-%s'%args.chip)



    titles = ['08', '11', '14', '20', '26', '29', '32']
    for i, (volt) in enumerate(voltages):
        if 'ECOND' in fnames[0]:
            for val in np.unique(currents[volt]['hasL1A']):
                plt.scatter(currents[volt]["mradDose"][currents[volt]["hasL1A"]==val], currents[volt]["current"][currents[volt]["hasL1A"]==val], label = f'{val} L1As')
            plt.legend()
        else:
            plt.scatter(currents[volt]['mradDose'], currents[volt]['current'])
        plt.title(f"{volt}V")
        plt.ylabel("Current (A)")
        plt.xlabel("TID (MRad)")
        plt.ylim(0.15,0.41)
        plt.savefig(f'{plots}/current_measurement_results_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()






    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):
        if 'ECOND' in fnames[0]:
            for val in np.unique(currents[volt]['hasL1A']):
                axs[i].scatter(currents[volt]["mradDose"][currents[volt]["hasL1A"]==val], currents[volt]["current"][currents[volt]["hasL1A"]==val], label = f"{val} L1A's")
        else:
            axs[i].scatter(currents[volt]['mradDose'], currents[volt]['current'])
        axs[i].set_title(f"{volt}")
        axs[i].set_ylabel('Current (A)')
        axs[i].set_xlabel('TID (MRad)')
        #set these limits later
        axs[i].set_ylim(0.15,0.41)
        if 'ECOND' in fnames[0]:
            axs[i].legend() 
    for ax in axs.flat:
        ax.label_outer()   
    fig.savefig(f'{plots}/summary_current_vs_tid_results.png', dpi=300, facecolor="w")
        
    print("Done producing current vs TID plots!")







