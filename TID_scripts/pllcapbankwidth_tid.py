# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

def getpllCapbankWidth(data, voltage):
    PllCapbankWidth = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_TID.py::test_pll_capbank_width[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    PllCapbankWidth.append(data[i]['tests'][j]['metadata']['pll_capbank_width'])    
    
    mradDose = FNames2MRad(fnames)
    return PllCapbankWidth, mradDose

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

    plots = create_plot_path(args.path+ '/' + 'pllcapbank_vs_tid_plots-%s'%args.chip)

    PllCapbankWidth = {
    volt: {
        "PllCapbankWidth": getpllCapbankWidth(data, volt)[0],
        "mradDose": getpllCapbankWidth(data, volt)[1],
    } for volt in voltages
    }

    titles = ['08', '11', '14', '20', '26', '29', '32']
    for i, (volt) in enumerate(voltages):
        plt.scatter(PllCapbankWidth[volt]["mradDose"], PllCapbankWidth[volt]["PllCapbankWidth"])
        plt.title(f"{volt}V")
        plt.ylabel('PllCapbankWidth')
        plt.xlabel("TID (MRad)")
        plt.ylim(0,20)
        plt.savefig(f'{plots}/pll_capbank_width_results_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()

    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):
        axs[i].scatter(PllCapbankWidth[volt]["mradDose"], PllCapbankWidth[volt]["PllCapbankWidth"])
        axs[i].set_title(f"{volt}")
        axs[i].set_ylabel('PllCapbankWidth')
        axs[i].set_xlabel('TID (MRad)')
        # axs[i].set_xlim(0,660)
        axs[i].set_ylim(0,20)
        axs[i].grid(which='minor', alpha=0.2, color='b', linestyle='--', linewidth=.3)
        axs[i].grid(which='major', alpha=0.2, color='b', linestyle='--', linewidth=.6)
    for ax in axs.flat:
        ax.label_outer()   
    fig.savefig(f'{plots}/pll_capbank_width_results.png', dpi=300, facecolor="w") 
