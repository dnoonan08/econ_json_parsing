# Script to plot current versus TID

from common import create_plot_path, get_fnames, datetime_to_TID, xray_start_stop, ObelixDoseRate,datetime_to_TID_chip002
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt
import json

import pandas as pd

mpl.use('Agg')

def getBistData(flist):
    pp = []
    ob = []
    goodinit = []
    timestamps = []
    temperatures = []
    voltages = None
    i=0
    for f in flist:
        try:
            with open(f) as _file:
                data = json.load(_file)
                bist_result = data['tests'][-1]['metadata']
                this_voltages= np.array(bist_result['voltages'])
                if voltages is None:
                    voltages = this_voltages[:]
                assert (voltages==this_voltages).all(), "bad voltage values"
                this_pp= np.array(bist_result['ppResults'])
                this_ob= np.array(bist_result['obResults'])
                initbist = np.array(bist_result['initBistVal'])
                

                if len((initbist==0).all(axis=1)) > 30: raise Exception
                goodinit.append((initbist==0).all(axis=1))
                pp.append(np.array([((this_pp>>i)&1) & (this_pp>0) for i in range(12)]))
                ob.append(np.array([((this_ob>>i)&1) & (this_ob>0) for i in range(12)]))
                timestamps.append(np.datetime64(bist_result['timestamps'][0]))
                if 'Temperature' in data['tests'][-1]['metadata'].keys():
                    temperatures.append(data['tests'][-1]['metadata']['Temperature'])
                else:
                    for j in range(len(data['tests'])):
                        if f"test_streamCompareLoop[1.2]" in data['tests'][j]['nodeid']:
                            temperatures.append(data['tests'][j]['metadata']['Temperature'][0])
                            
                
        except:
            print(f'issue in file {f}')
        i += 1
    pp = np.array(pp)
    ob = np.array(ob)
    timestamps = np.array(timestamps)
    temperatures = np.array(temperatures) 

    return timestamps, voltages, pp.T, ob.T, goodinit, temperatures

def getBistFailureVoltages(bist_result,voltages):
    v_lowpass = []
    v_highfail = []
    for i_test in range(4):
        v_lowpass.append([])
        v_highfail.append([])
        for i_file in range(bist_result.shape[-1]):
            v_lowpass[-1].append([])
            v_highfail[-1].append([])
            for i_bit in range(12):
                if (bist_result[i_test,:,i_bit,i_file]==1).any():
                    v_lowpass[-1][-1].append(voltages[bist_result[i_test,:,i_bit,i_file]==1].min())
                else:
                    v_lowpass[-1][-1].append(voltages.max()+0.01)
                if (bist_result[i_test,:,i_bit,i_file]==0).any():
                    v_highfail[-1][-1].append(voltages[bist_result[i_test,:,i_bit,i_file]==0].max())
                else:
                    v_highfail[-1][-1].append(voltages.min()-0.01)
    return np.array(v_lowpass), np.array(v_highfail)


def plot_bist(timestamps, bist_result, ax, y_range=(None,None),xlabel = 'Time', ylabel = 'Voltage', title=None, xrotation=60, label = 'chip',x_range=(None,None)):

    out = ax.plot(timestamps,bist_result)
    ax.scatter(timestamps,bist_result,label = label)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = xrotation)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(y_range[0],y_range[1])
    #ax.set_xlim(x_range[0],x_range[1])
    ax.set_title(title)
    return out


def plot_bist2d(timestamps, sample, ax,xlabel='Time', ylabel='Bist Test',title=None,xrotation=60, label = 'chip003'):
    timestamp_bins = np.concatenate([timestamps,np.array([timestamps[-1] + (timestamps[-1] - timestamps[-2])])])
    if type(timestamps[0]) is float:
        timestamp_bins -= 0.001
    a,b = np.meshgrid(timestamps,np.arange(0,12,(12/48)))
    ax.hist2d(a.flatten(),b.flatten(),weights=sample,bins=(timestamp_bins,np.arange(0,12,(12/48))-0.001),cmap='bwr_r',vmin=0,vmax=1, label = label);
    if xlabel=='Time':
        ax.set_xticklabels(ax.get_xticklabels(), rotation = 60)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(xlabel)
    ax.set_title(title)

if __name__ == '__main__':
    # argument parser
    import argparse
    parser = argparse.ArgumentParser(description='Args')
    parser.add_argument('--path', default = '../..', type = str) # repo name on github json repo
    parser.add_argument('--chip', default = 'chip001-subset') # repo name on github 


    args = parser.parse_args()

    # Path to JSONs
    path = args.path + '/' + args.chip + '/'
    print(f"Running on {path}")

    # Fetch JSON name
    fnames = get_fnames(path)


    timestamps, voltages, pp, ob, goodinit,temperatures = getBistData(fnames)
    if 'chip002-econd' in args.chip:
        tid, xray_on = datetime_to_TID_chip002(timestamps, ObelixDoseRate, xray_start_stop[args.chip])
    else:
        tid, xray_on = datetime_to_TID(timestamps, ObelixDoseRate, xray_start_stop[args.chip])
    tid = np.array(tid)
    xray_on = np.array(xray_on)

    v_pp_lowpass, v_pp_highfail = getBistFailureVoltages(pp,voltages)
    v_ob_lowpass, v_ob_highfail = getBistFailureVoltages(ob,voltages)

    for i in range(v_pp_lowpass.shape[0]):
        df = pd.DataFrame(v_pp_lowpass[i], columns=[f'SRAM {j+1}' for j in range(v_pp_lowpass.shape[2])])
        
        print(len(tid))
        df['TID'] = tid
        df['XRAYON'] = xray_on
        df['TIMESTAMPS'] = timestamps
        df['TEMPERATURE'] = temperatures

        df.to_csv('bist-csv/%s_pp_test%d.csv'%(args.chip,i+1),index=False)
    
    for i in range(v_ob_lowpass.shape[0]):
        df = pd.DataFrame(v_ob_lowpass[i], columns=[f'SRAM {j+1}' for j in range(v_ob_lowpass.shape[2])])
        
        print(len(tid))
        df['TID'] = tid
        df['XRAYON'] = xray_on
        df['TIMESTAMPS'] = timestamps
        df['TEMPERATURE'] = temperatures

        df.to_csv('../../bist-study-averages/bist-csv/%s_ob_test%d.csv'%(args.chip,i+1),index=False)

   