# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

def getAutoCapbank(data, voltage,fnames):
    AutomaticCapbanks = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_TID.py::test_streamCompareLoop[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    AutomaticCapbanks.append(data[i]['tests'][j]['metadata']['automatic_capbank_setting'])    
    
    allowed_cap_bank_vals=np.array([  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,
                                    13,  14,  15,  24,  25,  26,  27,  28,  29,  30,  31,  56,  57,
                                    58,  59,  60,  61,  62,  63, 120, 121, 122, 123, 124, 125, 126,
                                    127, 248, 249, 250, 251, 252, 253, 254, 255, 504, 505, 506,       507,
                                    508, 509, 510, 511])
    for i in range (len(AutomaticCapbanks)):
            for j in range(56):
                if AutomaticCapbanks[i] == allowed_cap_bank_vals[j]:
                    AutomaticCapbanks[i] = j
    mradDose = FNames2MRad(fnames)
    return AutomaticCapbanks, mradDose


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

    AutomaticCapbank = {
        volt: {
            "AutomaticCapbank": getAutoCapbank(data, volt,fnames)[0],
            "mradDose": getAutoCapbank(data, volt,fnames)[1],
        } for volt in voltages
    }


    # Plotting

    plots = create_plot_path(args.path+ '/' + 'autocapbank_vs_tid_plots-%s'%args.chip)

    titles = ['08', '11', '14', '20', '26', '29', '32']
    for i, (volt) in enumerate(voltages):
        plt.scatter(AutomaticCapbank[volt]["mradDose"], AutomaticCapbank[volt]["AutomaticCapbank"])
        plt.title(f"{volt}V")
        plt.ylabel('Automatic Capbank Selection')
        plt.xlabel("TID (MRad)")
        plt.ylim(20,30)
        plt.savefig(f'{plots}/automatic_capbank_selection_results_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()

    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):
        axs[i].scatter(AutomaticCapbank[volt]["mradDose"], AutomaticCapbank[volt]["AutomaticCapbank"])
        axs[i].set_title(f"{volt}")
        axs[i].set_ylabel('Automatic Capbank Selection')
        axs[i].set_xlabel('TID (MRad)')
        # axs[i].set_xlim(0,660)
        axs[i].set_ylim(20,30)
        axs[i].grid(which='minor', alpha=0.2, color='b', linestyle='--', linewidth=.3)
        axs[i].grid(which='major', alpha=0.2, color='b', linestyle='--', linewidth=.6)
    for ax in axs.flat:
        ax.label_outer()   
    fig.savefig(f'{plots}/automatic_capbank_selection_results.png', dpi=300, facecolor="w") 
