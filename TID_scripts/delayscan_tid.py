# Script to plot current versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames, datetime_to_TID, xray_start_stop, ObelixDoseRate
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

def getDelayScanData(data, voltage, chip):
    bitCounts = []
    errCounts = []
    timestamps = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f'test_eTX_delayscan[{voltage}]' in data[i]['tests'][j]['nodeid']:
                    if 'timestamp' in data[i]['tests'][j]['metadata']:
                        errCounts.append(data[i]['tests'][j]['metadata']['eTX_errcounts'])
                        bitCounts.append(data[i]['tests'][j]['metadata']['eTX_bitcounts'])
                        timestamps.append(np.datetime64(data[i]['tests'][j]['metadata']['timestamp']))
    errCounts = np.array(errCounts)
    bitCounts = np.array(bitCounts)
    errRate = errCounts/bitCounts
    timestamps = np.array(timestamps)
    # mradDose = FNames2MRad(fnames)
    # dosePlots = np.array(list(mradDose)+[(mradDose[-1]-mradDose[-2])+mradDose[-1]])
    tid, xray_on = datetime_to_TID(timestamps, ObelixDoseRate, xray_start_stop[f'chip00{chip}'])
    tid = np.array(tid)
    xray_on = np.array(xray_on)
    tidPlots = np.array(list(tid)+[(tid[-1]-tid[-2])+tid[-1]])
    timestampPlots = np.array(list(timestamps)+[(timestamps[-1]-timestamps[-2])+timestamps[-1]])
    xrayBoolPlots = list(xray_on) + [True]

    result = {
        'errRate': errRate,
        'tid' : tid,
        'xray_on': xray_on,
        'tidPlots': tidPlots,
        'timestampPlots': timestampPlots,
        'xrayBoolPlots': np.array(xrayBoolPlots),
        'timestamps': timestamps,
    }
    return result

def makeDelayScanPlot(delayScan,path, ECONT = False, timestamp = False):
    titles = ['08', '11', '14', '20', '26', '29', '32']
    voltages = [1.08, 1.11, 1.14, 1.20, 1.26, 1.29, 1.32]
    if ECONT:
        jrange = 13
    else:
        jrange = 6
    for j  in range(jrange):
        for i, (volt) in enumerate(voltages):
            fig, ax = plt.subplots()
            if timestamp:
                a, b = np.meshgrid(delayScan[volt]['timestamps'],np.arange(63))
                weights = delayScan[volt]['errRate'][:,j,:].T.flatten()
                h = plt.hist2d(a.flatten(), b.flatten(), weights=weights, bins = (delayScan[volt]['timestampPlots'], np.arange(64)), cmap='RdYlBu_r', alpha=weights>0)
                plt.xticks(rotation = 45)
            else:
                a, b = np.meshgrid(delayScan[volt]['tid'][delayScan[volt]['xray_on']==1],np.arange(63))
                weights = delayScan[volt]['errRate'][:,j,:][delayScan[volt]['xray_on']==1].T.flatten()
                h = plt.hist2d(a.flatten(), b.flatten(), weights=weights, bins = (delayScan[volt]['tidPlots'][delayScan[volt]['xrayBoolPlots']==1], np.arange(64)), cmap='RdYlBu_r', alpha=weights>0)
                plt.xlabel('TID (MRad)')
                
            cb=fig.colorbar(h[3], ax = ax)
            cb.set_label(label='Transmission errors rate')
            plt.title(f"eTx {j} at {volt}V")
            plt.ylabel('Delay select setting')
            if timestamp:
                plt.savefig(f'{path}/delay_scan_volt_TIMESTAMP_1p{titles[i]}V_eRx{j}.png', dpi=300, facecolor="w")
            else:
                plt.savefig(f'{path}/delay_scan_volt_TID_1p{titles[i]}V_eRx{j}.png', dpi=300, facecolor="w")
            plt.clf()
            plt.close()
    for j in range(jrange):

        fig,axs=plt.subplots(figsize=(55,12),ncols=7,nrows=1, layout="constrained")
        
        for i, (volt) in enumerate(voltages):
            if timestamp:
                a, b = np.meshgrid(delayScan[volt]['timestamps'],np.arange(63))
                weights = delayScan[volt]['errRate'][:,j,:].T.flatten()
                h = axs[i].hist2d(a.flatten(), b.flatten(), weights=weights, bins = (delayScan[volt]['timestampPlots'], np.arange(64)), cmap='RdYlBu_r', alpha=weights>0)
                axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation = 45)
            else:
                a, b = np.meshgrid(delayScan[volt]['tid'][delayScan[volt]['xray_on']==1],np.arange(63))
                weights = delayScan[volt]['errRate'][:,j,:][delayScan[volt]['xray_on']==1].T.flatten()
                h = axs[i].hist2d(a.flatten(), b.flatten(), weights=weights, bins = (delayScan[volt]['tidPlots'][delayScan[volt]['xrayBoolPlots']==1], np.arange(64)), cmap='RdYlBu_r', alpha=weights>0)
                axs[i].set_xlabel('TID (MRad)')
            cb=fig.colorbar(h[3], ax = axs[i])
            cb.set_label(label='Transmission errors rate')
            axs[i].set_title(f"eTx {j} at {volt}V")
            axs[i].set_ylabel('Delay select setting')
            
        for ax in axs.flat:
            ax.label_outer()
        if timestamp:
            fig.savefig(f'{path}/delay_scan_TIMESTAMP_eTx_{j}.png', dpi=300, facecolor="w")
        else:
            fig.savefig(f'{path}/delay_scan_TID_eTx_{j}.png', dpi=300, facecolor="w")

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

    ECOND = True
    if 'ECONT' in fnames[0]:
        ECOND = False


    # Plotting

    plots = create_plot_path(args.path+ '/' + 'delayscan_vs_tid_plots-%s'%args.chip)

    delayScanResults = {
    volt: getDelayScanData(data, volt, args.chip) for volt in voltages
    }
    print('finished loading data')
    if ECOND == True:
        makeDelayScanPlot(delayScanResults, plots, ECONT = False, timestamp = False)
        makeDelayScanPlot(delayScanResults, plots, ECONT = False, timestamp = True)
    else:
        makeDelayScanPlot(delayScanResults, plots, ECONT = True, timestamp = False)
        makeDelayScanPlot(delayScanResults, plots, ECONT = True, timestamp = True)
            
        
