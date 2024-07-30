# Script to plot SC errror versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, get_fnames, datetime_to_TID, xray_start_stop, ObelixDoseRate
import numpy as np
import glob

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

def getSCErrorsECOND(data, voltage, chip):
    word_err_cnt = []
    hasL1As = []
    Timestamps = []
    error_rates = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_streamCompareLoop[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    info = np.array(data[i]['tests'][j]['metadata']['word_err_count'])
                    hasL1As = np.array(data[i]['tests'][j]['metadata']['HasL1A'])
                    errs = []
                    times = []
                    for val in np.unique(hasL1As):
                        counts = info[:, 1:].astype(int)[np.array(hasL1As)==val]
                        print(voltage)
                        print(val)
                        print(counts)
                        rollovers = (counts[1:] < counts[:-1]).sum(axis=0)
                        print(rollovers)
                        totalWords, totalErrors = rollovers * 2**32 + counts[-1]
                        print(totalWords,totalErrors)
                        errorRate = totalErrors/totalWords
                        errs.append(errorRate)
                        times.append(np.datetime64(info[:,0][hasL1As==val][-1]))
                    Timestamps.append(times)
                    error_rates.append(errs)
    err_rates3 = []
    Timestamps3 = []
    err_rates67 = []
    Timestamps67  = []
    for i in range(len(Timestamps)):
        if len(Timestamps[i]) == 3:
            err_rates3.append(error_rates[i])
            Timestamps3.append(Timestamps[i])
        if len(Timestamps[i]) == 1:
            err_rates67.append(error_rates[i])
            Timestamps67.append(Timestamps[i])

    err_rates3 = np.array(err_rates3)
    Timestamps3 = np.array(Timestamps3)
    err_rates67 = np.array(err_rates67).flatten()
    Timestamps67 = np.array(Timestamps67).flatten()
    dim1, dim2 = Timestamps3.shape
    Timestamps3 = Timestamps3.flatten()
    tid3, xray_on3 = datetime_to_TID(Timestamps3, ObelixDoseRate, xray_start_stop[f'{chip}'])
    Timestamps3 = Timestamps3.reshape(dim1, dim2)
    tid3 = np.array(tid3)
    xray_on3 = np.array(xray_on3)
    tid3 = tid3.reshape(dim1, dim2)
    xray_on3 = xray_on3.reshape(dim1,dim2)
    tid67, xray_on67 = datetime_to_TID(Timestamps67, ObelixDoseRate, xray_start_stop[f'{chip}'])
    tid67 = np.array(tid67)
    xray_on67 = np.array(xray_on67)
    hasL1As = np.array([0,7,67])
    results = {
        f"{val}-L1As":{
            f"ErrRate": np.array(err_rates3)[:,i] if i != 2 else np.array(list(np.array(err_rates3)[:,i]) + list(err_rates67)),
            f"tid": tid3[:,i] if i!= 2 else np.array(list(tid3[:,i]) + list(tid67)),
            "xray_on": xray_on3[:,i] if i!= 2 else np.array(list(xray_on3[:,i]) + list(xray_on67)),
            'Timestamps': Timestamps3[:,i] if i!= 2 else np.array(list(Timestamps3[:,i]) + list(Timestamps67)),
        } for i, (val) in enumerate(np.unique(hasL1As))
    }
    return results




def makeECONDSCPlots(scErrors,plots,timestamps = False):
    titles = ['08', '11', '14', '20', '26', '29', '32']

    for i, (volt) in enumerate(voltages):
        for key in scErrors[volt].keys():
            if timestamps:
                plt.scatter(scErrors[volt][key]['Timestamps'], scErrors[volt][key]['ErrRate'], label=f'{key}')
                plt.xticks(rotation = 45)
            else:
                plt.scatter(scErrors[volt][key]['tid'][scErrors[volt][key]['xray_on']==True], scErrors[volt][key]['ErrRate'][scErrors[volt][key]['xray_on']==True], label=f'{key}')
                plt.xlabel("TID (MRad)")
        plt.yscale("log")
        plt.ylim(10**-11, 1.0)
        plt.legend()
        plt.ylabel("Error Rate")
        plt.title(f"{volt}V")
        if timestamps:
            plt.savefig(f'{plots}/err_rate_results_TIMESTAMPS_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        else:
            plt.savefig(f'{plots}/err_rate_results_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()
        plt.close()

    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):
        for key in scErrors[volt].keys():
            if timestamps:
                axs[i].scatter(scErrors[volt][key]['Timestamps'], scErrors[volt][key]['ErrRate'], label=f'{key}')
                axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation = 45)
            else:
                axs[i].scatter(scErrors[volt][key]['tid'][scErrors[volt][key]['xray_on']==True], scErrors[volt][key]['ErrRate'][scErrors[volt][key]['xray_on']==True], label=f'{key}')
                axs[i].set_xlabel("TID (MRad)")
        axs[i].set_yscale("log")
        axs[i].set_ylim(10**-11, 1.0)
        axs[i].legend()
        axs[i].set_ylabel("Error Rate")
        axs[i].set_title(f"{volt}V")
    for ax in axs.flat:
        ax.label_outer()
    if timestamps:
        fig.savefig(f'{plots}/summary_word_err_err_rate_results_TIMESTAMPS.png', dpi=300, facecolor="w")
    else:
        fig.savefig(f'{plots}/summary_word_err_err_rate_results.png', dpi=300, facecolor="w")


def getSCErrorsECONT(data,voltage, chip):
    errRate = []
    Timestamps = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_streamCompareLoop[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    info = np.array(data[i]['tests'][j]['metadata']['word_err_count'])
                    counts = info[:, 1:].astype(int)
                    rollovers = (counts[1:] < counts[:-1]).sum(axis=0)
                    totalWords, totalErrors = rollovers * 2**32 + counts[-1]
                    errorRate = totalErrors/totalWords
                    errRate.append(errorRate)
                    Timestamps.append(np.datetime64(info[:,0][-1]))
    Timestamps = np.array(Timestamps)
    errRate = np.array(errRate)
    tid, xray_on = datetime_to_TID(Timestamps, ObelixDoseRate, xray_start_stop[f'{chip}'])
    tid = np.array(tid)
    xray_on = np.array(xray_on)
    result = {
        'ErrRate': errRate,
        "tid": tid,
        'xray_on':xray_on,
        'Timestamps': Timestamps,
    }
    return result


def makeECONTSCPlots(scErrors, plots, timestamps = False):
    titles = ['08', '11', '14', '20', '26', '29', '32']
    for i, (volt) in enumerate(voltages):
        if timestamps:
            plt.scatter(scErrors[volt]['Timestamps'], scErrors[volt]['ErrRate'])
            plt.xticks(rotation = 45)
        else:
            plt.scatter(scErrors[volt]['tid'][scErrors[volt]['xray_on']==True], scErrors[volt]['ErrRate'][scErrors[volt]['xray_on']==True])
            plt.xlabel("TID (MRad)")
        ## note: MARKO WE WILL NEED TO UNCOMMENT THE YSCALE ONCE WE START TO GET ERRORS                                                                                       
        #plt.yscale("log")                                                                                                                                                    
        plt.ylim(10**-11, 1.0)
        plt.ylabel("Error Rate")
        plt.title(f"{volt}V")
        if timestamps:
            plt.savefig(f'{plots}/err_rate_results_TIMESTAMPS_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        else:
            plt.savefig(f'{plots}/err_rate_results_TID_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()
        plt.close()
    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):
        if timestamps:
            axs[i].scatter(scErrors[volt]['Timestamps'], scErrors[volt]['ErrRate'])
            axs[i].set_xticklabels(axs[i].get_xticklabels(), rotation = 45)
        else:
            axs[i].scatter(scErrors[volt]['tid'][scErrors[volt]['xray_on']==True], scErrors[volt]['ErrRate'][scErrors[volt]['xray_on']==True])
            axs[i].set_xlabel("TID (MRad)")
        #axs[i].set_yscale("log")
        

        axs[i].set_ylim(10**-11, 1.0)
        axs[i].set_ylabel("Error Rate")
        axs[i].set_title(f"{volt}V")
    for ax in axs.flat:
        ax.label_outer()
    if timestamps:
        fig.savefig(f'{plots}/summary_word_err_err_rate_results_TIMESTAMPS.png', dpi=300, facecolor="w")
    else:
        fig.savefig(f'{plots}/summary_word_err_err_rate_results_TID.png', dpi=300, facecolor="w")
    plt.clf()
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
    fnames = list(np.sort(glob.glob(f"{path}/report*.json")))
    # Fetch JSON data and startime of first JSON
    data, starttime = get_data(path)
    fnames = get_fnames(path)

    ECOND = True
    if 'ECONT' in fnames[0]: ECOND = False

    scErrors = {
    volt: getSCErrorsECOND(data, volt, args.chip) if 'ECOND' in fnames[0] else getSCErrorsECONT(data, volt, args.chip) for volt in voltages
    }
    # Plotting

    plots = create_plot_path(args.path+ '/' + 'sc_error_vs_tid_plots-%s'%args.chip)

    if 'ECOND' in fnames[0]:
        makeECONDSCPlots(scErrors, plots, timestamps = True)
        makeECONDSCPlots(scErrors, plots)
    else:
        makeECONTSCPlots(scErrors, plots, timestamps = True)
        makeECONTSCPlots(scErrors, plots)


        
    

