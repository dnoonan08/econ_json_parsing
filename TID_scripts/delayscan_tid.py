# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

def getDelayScanData(data, voltage):
    bitCounts = []
    errCounts = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f'test_TID.py::test_eTX_delayscan[{voltage}]' in data[i]['tests'][j]['nodeid']:
                    errCounts.append(data[i]['tests'][j]['metadata']['eTX_errcounts'])
                    bitCounts.append(data[i]['tests'][j]['metadata']['eTX_bitcounts'])
    errCounts = np.array(errCounts)
    bitCounts = np.array(bitCounts)
    if bitCounts > 0:
        errRate = errCounts/bitCounts
    else:
        errRate = 0
    mradDose = FNames2MRad(fnames)
    dosePlots = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
    return errRate, dosePlots, mradDose

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

    plots = create_plot_path(args.path+ '/' + 'delayscan_vs_tid_plots')

    delayScan = {
        volt: {
            'errRate': getDelayScanData(data, volt)[0],
            'plotDose': getDelayScanData(data, volt)[1],
            'mradDose': getDelayScanData(data, volt)[2],
        } for volt in voltages
    }

    titles = ['08', '11', '14', '20', '26', '29', '32']

    for j  in range(6):
        for i, (volt) in enumerate(voltages):
            fig, ax = plt.subplots()
            a, b = np.meshgrid(delayScan[volt]['mradDose'],np.arange(63))
            weights = delayScan[volt]['errRate'][:,j,:].T.flatten()
            h = plt.hist2d(a.flatten(), b.flatten(), weights=weights, bins = (delayScan[volt]['plotDose'], np.arange(64)), cmap='RdYlBu_r', alpha=weights>0)
            cb=fig.colorbar(h[3])
            cb.set_label(label='Transmission errors rate')
            plt.title(f"eTx {j} at {volt}V")
            plt.ylabel('Delay select setting')
            plt.xlabel('TID (MRad)')
            plt.savefig(f'{plots}/delay_scan_volt_1p{titles[i]}V_eRx{j}.png', dpi=300, facecolor="w")
            plt.clf()
            plt.close()

    for j in range(6):

        fig,axs=plt.subplots(figsize=(55,12),ncols=7,nrows=1, layout="constrained")
        
        for i, (volt) in enumerate(voltages):
            a, b = np.meshgrid(delayScan[volt]['mradDose'],np.arange(63))
            weights = delayScan[volt]['errRate'][:,j,:].T.flatten()
            norm = mcolors.TwoSlopeNorm(vmin=0, vmax = 255, vcenter=.9)
            h = axs[i].hist2d(a.flatten(), b.flatten(), weights=weights, bins = (delayScan[volt]['plotDose'], np.arange(64)), cmap='RdYlBu_r', alpha=weights>0)
            cb=fig.colorbar(h[3], ax = axs[i])
            cb.set_label(label='Transmission errors rate')
            axs[i].set_title(f"eTx {j} at {volt}V")
            axs[i].set_ylabel('Delay select setting')
            axs[i].set_xlabel('TID (MRad)')
        for ax in axs.flat:
            ax.label_outer()

        fig.savefig(f'{plots}/delay_scan_eTx_{j}.png', dpi=300, facecolor="w") 
            
        