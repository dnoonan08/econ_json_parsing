# Script to plot SC errror versus TID 

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path,get_fnames,Timestamp2XrayBool
import numpy as np
import glob

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

def getSCErrorsECOND(data, voltage, starttime):
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
                        rollovers = (counts[1:] < counts[:-1]).sum(axis=0)
                        totalWords, totalErrors = rollovers * 2**32 + counts[-1]
                        errorRate = totalErrors/totalWords
                        errs.append(errorRate)
                        times.append(info[:,0][hasL1As==val][-1])
                    Timestamps.append(times)
                    error_rates.append(errs)
    dim1, dim2 = np.array(Timestamps).shape
    Timestamps = np.array(Timestamps).flatten()
    mradDose = Timestamp2MRad(Timestamps, starttime)
    hasXrays = Timestamp2XrayBool(Timestamps)
    mradDose = mradDose.reshape(dim1, dim2)
    hasXrays = hasXrays.reshape(dim1,dim2)
    results = {
        f"{val}-L1As":{
            f"ErrRate": np.array(error_rates)[:,i],
            f"mradDose": mradDose[:,i],
            f"hasXrays": hasXrays[:,i],
        } for i, (val) in enumerate(np.unique(hasL1As))
    }
    return results

def getSCErrorsECONT(data,voltage, starttime):
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
                    Timestamps.append(info[:,0][-1])
    Timestamps = np.array(Timestamps)
    errRate = np.array(errRate)
    mradDose = Timestamp2MRad(Timestamps, starttime)
    hasXrays = Timestamp2XrayBool(Timestamps)
    result = {
        'ErrRate': errRate,
        "mradDose": mradDose,
        "hasXrays": hasXrays,
    }
    return result


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
    volt: getSCErrorsECOND(data, volt, starttime) if 'ECOND' in fnames[0] else getSCErrorsECONT(data, volt, starttime) for volt in voltages
    }
    # Plotting

    plots = create_plot_path(args.path+ '/' + 'sc_error_vs_tid_plots-%s'%args.chip)


    if 'ECOND' in fnames[0]:
        titles = ['08', '11', '14', '20', '26', '29', '32']
        for i, (volt) in enumerate(voltages):
            for key in scErrors[volt].keys():
                plt.scatter(scErrors[volt][key]['mradDose'][scErrors[volt][key]['hasXrays']==1], scErrors[volt][key]['ErrRate'][scErrors[volt][key]['hasXrays']==1], label=f'{key}')
            plt.yscale("log")
            #plt.ylim(10**-11, 1.0)
            plt.legend()
            plt.ylabel("Error Rate")
            plt.xlabel("TID (MRad)")
            plt.title(f"{volt}V")
            plt.savefig(f'{plots}/err_rate_results_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
            plt.clf()


        fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
        for i, (volt) in enumerate(voltages):
            for key in scErrors[volt].keys():
                axs[i].scatter(scErrors[volt][key]['mradDose'][scErrors[volt][key]['hasXrays']==1], scErrors[volt][key]['ErrRate'][scErrors[volt][key]['hasXrays']==1], label=f'{key}')
            axs[i].set_yscale("log")
            #axs[i].set_ylim(10**-11, 1.0)
            axs[i].legend()
            axs[i].set_ylabel("Error Rate")
            axs[i].set_xlabel("TID (MRad)")
            axs[i].set_title(f"{volt}V")
        for ax in axs.flat:
            ax.label_outer()

        fig.savefig(f'{plots}/summary_word_err_err_rate_results.png', dpi=300, facecolor="w")   
    
    else:
        titles = ['08', '11', '14', '20', '26', '29', '32']
        for i, (volt) in enumerate(voltages):
            plt.scatter(scErrors[volt]['mradDose'][scErrors[volt]['hasXrays']==1], scErrors[volt]['ErrRate'][scErrors[volt]['hasXrays']==1])
            ## note: MARKO WE WILL NEED TO UNCOMMENT THE YSCALE ONCE WE START TO GET ERRORS
            #plt.yscale("log")
            #plt.ylim(10**-11, 1.0)
            plt.ylabel("Error Rate")
            plt.xlabel("TID (MRad)")
            plt.title(f"{volt}V")
            plt.savefig(f'{plots}/err_rate_results_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
            plt.clf()
        fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
        for i, (volt) in enumerate(voltages):
            axs[i].scatter(scErrors[volt]['mradDose'][scErrors[volt]['hasXrays']==1], scErrors[volt]['ErrRate'][scErrors[volt]['hasXrays']==1])
            #axs[i].set_yscale("log")
            #axs[i].set_ylim(10**-11, 1.0)
            axs[i].set_ylabel("Error Rate")
            axs[i].set_xlabel("TID (MRad)")
            axs[i].set_title(f"{volt}V")
        for ax in axs.flat:
            ax.label_outer()

        fig.savefig(f'{plots}/summary_word_err_err_rate_results.png', dpi=300, facecolor="w")   
        
    

