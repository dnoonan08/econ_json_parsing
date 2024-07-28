# Script to plot temperature as function of TID

from common import get_data, Timestamp2MRad, FNames2MRad, voltages, MYROOT, create_plot_path, Timestamp2XrayBool, datetime_to_TID, xray_start_stop, ObelixDoseRate
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt


def getTemperatureValues(data, voltage,starttime):
    temperatures = []
    hasL1As = []
    Timestamps = []
    hasXrays = []
    for i in range(len(data)):
        for j in range(len(data[i]['tests'])):
            if 'metadata' in data[i]['tests'][j]:
                if f"test_streamCompareLoop[{voltage}]" in data[i]['tests'][j]['nodeid']:
                    temperatures.append(data[i]['tests'][j]['metadata']['Temperature'])
                    hasL1As.append(data[i]['tests'][j]['metadata']['HasL1A'])
                    Timestamps.append(data[i]['tests'][j]['metadata']['Timestamp'])



    temperature = np.array([x for xs in temperatures for x in xs])
    hasL1A = np.array([x for xs in hasL1As for x in xs])
    Timestamp = np.array([x for xs in Timestamps for x in xs])
    #mradDose = Timestamp2MRad(Timestamp,starttime)
    #hasXrays = Timestamp2XrayBool(Timestamp)
    timestamps = np.array([np.datetime64(xs) for xs in Timestamp ])
        
    mradDose, hasXrays = datetime_to_TID(timestamps, ObelixDoseRate, xray_start_stop[args.chip])

    mradDose = np.array(mradDose)
    hasXrays = np.array(hasXrays)

    return temperature, hasL1A, mradDose, hasXrays, timestamps


def plot_temp(timestamps, temp_result, ax, y_range=(None,None),xlabel = 'Time', ylabel = 'Temperature', title=None, xrotation=60):
    out = ax.plot(timestamps,temp_result)
    ax.scatter(timestamps,temp_result)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = xrotation)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(y_range[0],y_range[1])
    ax.set_title(title)
    return out    



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


    temperatures = {
    volt: {
        "temperature": getTemperatureValues(data, volt,starttime)[0],
        "hasL1A": getTemperatureValues(data, volt,starttime)[1],
        "mradDose": getTemperatureValues(data, volt,starttime)[2],
        "hasXrays": getTemperatureValues(data, volt,starttime)[3],
        "timestamps": getTemperatureValues(data, volt,starttime)[4],
        } for volt in voltages
    }

    plots = create_plot_path(args.path+ '/' + 'temperature_vs_tid_plots-%s'%args.chip)


    titles = ['08', '11', '14', '20', '26', '29', '32']
    for i, (volt) in enumerate(voltages):
        #plt.scatter(temperatures[volt]["mradDose"], temperatures[volt]["temperature"])

        #plt.scatter(temperatures[volt]["mradDose"][temperatures[volt]["hasXrays"]==0], temperatures[volt]["temperature"][temperatures[volt]["hasXrays"]==0], label = 'No x-ray')

        #plt.scatter(temperatures[volt]["mradDose"][temperatures[volt]["hasXrays"]==1], temperatures[volt]["temperature"][temperatures[volt]["hasXrays"]==1], label = 'X-ray on')

        #plt.title(f"{volt}V")
        #plt.ylabel('Temperature (C)')
        #plt.xlabel("TID (MRad)")
        #plt.ylim(-20,35)
        #plt.legend()

        fig,ax = plt.subplots(1,1)
        plot_temp(temperatures[volt]["timestamps"], temperatures[volt]["temperature"], ax ,y_range=(-20,35), title = f"{volt}")
        fig.savefig(f'{plots}/temperature_vs_time_results_volt_1p{titles[i]}V_time.png', dpi=300, facecolor="w")
        plt.clf()

        fig,ax = plt.subplots(1,1)
        plot_temp(temperatures[volt]["mradDose"][temperatures[volt]["hasXrays"]==1], temperatures[volt]["temperature"][temperatures[volt]["hasXrays"]==1], ax ,y_range=(-20,35), title = f"{volt}", xlabel = 'TID (MRad)')
        fig.savefig(f'{plots}/temperature_vs_tid_results_volt_1p{titles[i]}V.png', dpi=300, facecolor="w")
        plt.clf()

    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):

        # Temperature versus timestamp 

        plot_temp(temperatures[volt]["timestamps"], temperatures[volt]["temperature"], axs[i],y_range=(-20,35), title = f"{volt}")

        #axs[i].scatter(temperatures[volt]["mradDose"], temperatures[volt]["temperature"])
        #axs[i].set_title(f"{volt}")
        #axs[i].set_ylabel('Temperature (C)')
        #axs[i].set_xlabel('TID (MRad)')
        # set these limits later
        #axs[i].set_ylim(-20,35)
        # axs[i].set_xlim(0,660)
    for ax in axs.flat:
        ax.label_outer()   
    fig.savefig(f'{plots}/summary_temperature_vs_time_results.png', dpi=300, facecolor="w")

    fig,axs=plt.subplots(figsize=(70,12),ncols=7,nrows=1, layout="constrained")
    for i, (volt) in enumerate(voltages):

        # Temperature versus TID 

        plot_temp(temperatures[volt]["mradDose"][temperatures[volt]["hasXrays"]==1], temperatures[volt]["temperature"][temperatures[volt]["hasXrays"]==1], axs[i],y_range=(-20,35), title = f"{volt}", xlabel = 'TID (MRad)')
    for ax in axs.flat:
        ax.label_outer()   
    fig.savefig(f'{plots}/summary_temperature_vs_tid_results.png', dpi=300, facecolor="w")

    print("Done producing temperature vs TID plots!")
