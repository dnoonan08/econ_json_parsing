# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames, datetime_to_TID, xray_start_stop, ObelixDoseRate
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt


def getPhaseScanData(data, voltage, chip):
    errCounts = []
    timestamps = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f'test_ePortRXPRBS[{voltage}]' in data[i]['tests'][j]['nodeid']:
                    if 'timestamp' in data[i]['tests'][j]['metadata']:
                        errCounts.append(data[i]['tests'][j]['metadata']['eRX_errcounts'])
                        timestamps.append(np.datetime64(data[i]['tests'][j]['metadata']['timestamp']))
    errCounts = np.array(errCounts)
    timestamps = np.array(timestamps)
    tid, xray_on = datetime_to_TID(timestamps, ObelixDoseRate, xray_start_stop[f'chip00{chip}'])
    tid = np.array(tid)
    xray_on = np.array(xray_on)
    tidPlots = np.array(list(tid)+[(tid[-1]-tid[-2])+tid[-1]])
    timestampPlots = np.array(list(timestamps)+[(timestamps[-1]-timestamps[-2])+timestamps[-1]])
    xrayBoolPlots = list(xray_on) + [True]

    result = {
        'errCounts': errCounts,
        'tid' : tid,
        'xray_on': xray_on,
        'tidPlots': tidPlots,
        'timestampPlots': timestampPlots,
        'xrayBoolPlots': np.array(xrayBoolPlots),
        'timestamps': timestamps,
    }
    return result

def makePhaseScanPlot(phaseScan, path, timestamp = False):
    titles = ['08', '11', '14', '20', '26', '29', '32']
    voltages = [1.08, 1.11, 1.14, 1.20, 1.26, 1.29, 1.32]
    for j in range(12):
        for i, (volt) in enumerate(voltages):
            fig,ax=plt.subplots()
            if timestamp:
                a, b = np.meshgrid(phaseScan[volt]['timestamps'],np.arange(15))
                weights = phaseScan[volt]['errCounts'][:,:,j].T.flatten()
                h = plt.hist2d(a.flatten(), b.flatten(), weights=weights, bins = (phaseScan[volt]['timestampPlots'], np.arange(16)), cmap='RdYlBu_r', alpha=weights>0)
                plt.xticks(rotation = 45)
            else:
                a, b = np.meshgrid(phaseScan[volt]['tid'][phaseScan[volt]['xray_on']==1],np.arange(15))
                weights = phaseScan[volt]['errCounts'][:,:,j][phaseScan[volt]['xray_on']==1].T.flatten()
                h = plt.hist2d(a.flatten(), b.flatten(), weights=weights, bins = (phaseScan[volt]['tidPlots'][phaseScan[volt]['xrayBoolPlots']==1], np.arange(16)), cmap='RdYlBu_r', alpha=weights>0)
                plt.xlabel('TID (Mrad)')
            cb=fig.colorbar(h[3])
            cb.set_label(label='Data transmission errors in PRBS',size=32)
            cb.ax.set_yscale('linear')
            plt.yticks(np.arange(15))
            plt.ylabel('Phase Select Setting')
            plt.title(f"eRx {j} at {volt}V")
            if timestamp:
                plt.savefig(f'{path}/phase_scan_volt_TIMESTAMP_1p{titles[i]}V_eRx{j}.png', dpi=300, facecolor="w")
            else:
                plt.savefig(f'{path}/phase_scan_volt_TID_1p{titles[i]}V_eRx{j}.png', dpi=300, facecolor="w")
            plt.clf()
            plt.close()
    for j in range(12):

        fig,axs=plt.subplots(figsize=(55,12),ncols=7,nrows=1, layout="constrained")
        
        for i, (volt) in enumerate(voltages):
            if timestamp:
                a, b = np.meshgrid(phaseScan[volt]['timestamps'],np.arange(15))
                weights = phaseScan[volt]['errCounts'][:,:,j].T.flatten()
                h = axs[i].hist2d(a.flatten(), b.flatten(), weights=weights, bins = (phaseScan[volt]['timestampPlots'], np.arange(16)), cmap='RdYlBu_r', alpha=weights>0)
                axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation = 45)
            else:
                a, b = np.meshgrid(phaseScan[volt]['tid'][phaseScan[volt]['xray_on']==1],np.arange(15))
                weights = phaseScan[volt]['errCounts'][:,:,j][phaseScan[volt]['xray_on']==1].T.flatten()
                h = axs[i].hist2d(a.flatten(), b.flatten(), weights=weights, bins = (phaseScan[volt]['tidPlots'][phaseScan[volt]['xrayBoolPlots']==1], np.arange(16)), cmap='RdYlBu_r', alpha=weights>0)
                axs[i].set_xlabel('TID (MRad)')
            
            cb=fig.colorbar(h[3], ax = axs[i])
            cb.set_label(label='Data transmission errors in PRBS')
            axs[i].set_title(f"eRx {j} at {volt}V")
            axs[i].set_ylabel('Phase select setting')
            
        for ax in axs.flat:
            ax.label_outer()
        if timestamp:
            fig.savefig(f'{path}/PRBS_scan_eRx_TIMESTAMP_{j}.png', dpi=300, facecolor="w")
        else:
            fig.savefig(f'{path}/PRBS_scan_eRx_TID_{j}.png', dpi=300, facecolor="w")        
        plt.close()

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

    phaseScan = {volt: getPhaseScanData(data, volt, args.chip) for volt in voltages}
    print('Finished grabbing data')
    makePhaseScanPlot(phaseScan, plots, timestamp=True)
    print('Finished making plots with Timestamps')
    makePhaseScanPlot(phaseScan, plots, timestamp=False)
    print('Finished making plots with TID')

