# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt


def getPhaseScanData(data, voltage):
    errCounts = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f'test_ePortRXPRBS[{voltage}]' in data[i]['tests'][j]['nodeid']:
                    errCounts.append(data[i]['tests'][j]['metadata']['eRX_errcounts'])
    errCounts = np.array(errCounts)
    mradDose = FNames2MRad(fnames)
    dosePlots = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
    return errCounts, dosePlots, mradDose

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

    plots = create_plot_path(args.path+ '/' + 'phasescan_vs_tid_plots-%s'%args.chip)

    phaseScan = {
    volt: {
        'errCounts': getPhaseScanData(data, volt)[0],
        'plotDose': getPhaseScanData(data, volt)[1],
        'mradDose': getPhaseScanData(data, volt)[2],
    } for volt in voltages
    }

    titles = ['08', '11', '14', '20', '26', '29', '32']

    for j in range(12):
        for i, (volt) in enumerate(voltages):
            fig,ax=plt.subplots()
            a, b = np.meshgrid(phaseScan[volt]['mradDose'],np.arange(15))
            weights = phaseScan[volt]['errCounts'][:,:,j].T.flatten()
            h = plt.hist2d(a.flatten(), b.flatten(), weights=weights, bins = (phaseScan[volt]['plotDose'], np.arange(16)), cmap='RdYlBu_r', alpha=weights>0)
            cb=fig.colorbar(h[3])
            cb.set_label(label='Data transmission errors in PRBS',size=32)
            cb.ax.set_yscale('linear')
            plt.yticks(np.arange(15))
            plt.ylabel('Phase Select Setting')
            plt.xlabel('TID (MRad)')
            plt.title(f"eRx {j} at {volt}V")
            plt.savefig(f'{plots}/phase_scan_volt_1p{titles[i]}V_eRx{j}.png', dpi=300, facecolor="w")
            plt.clf()
            plt.close()
    
    for j in range(12):

        fig,axs=plt.subplots(figsize=(55,12),ncols=7,nrows=1, layout="constrained")
        
        for i, (volt) in enumerate(voltages):
            a, b = np.meshgrid(phaseScan[volt]['mradDose'],np.arange(15))
            weights = phaseScan[volt]['errCounts'][:,:,j].T.flatten()
            norm = mcolors.TwoSlopeNorm(vmin=0, vmax = 255, vcenter=.9)
            h = axs[i].hist2d(a.flatten(), b.flatten(), weights=weights, bins = (phaseScan[volt]['plotDose'], np.arange(16)), cmap='RdYlBu_r', alpha=weights>0)
            cb=fig.colorbar(h[3], ax = axs[i])
            cb.set_label(label='Data transmission errors in PRBS')
            axs[i].set_title(f"eRx {j} at {volt}V")
            axs[i].set_ylabel('Phase select setting')
            axs[i].set_xlabel('TID (MRad)')
        for ax in axs.flat:
            ax.label_outer()

        fig.savefig(f'{plots}/PRBS_scan_eRx_{j}.png', dpi=300, facecolor="w") 


