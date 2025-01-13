# Script to plot current versus TID

from common import create_plot_path, get_fnames, datetime_to_TID, xray_start_stop, ObelixDoseRate
import numpy as np

import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt
import json

mpl.use('Agg')

def getBistData(flist):
    pp = []
    ob = []
    goodinit = []
    timestamps = []
    voltages = None
    i=0
    counter = 0

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
        except:
            print(f'issue in file {f}')
        i += 1
    print(counter)
    pp = np.array(pp)
    ob = np.array(ob)
    #print(goodinit)
    goodinit = np.array(goodinit)

    timestamps = np.array(timestamps)

    return timestamps, voltages, pp.T, ob.T, goodinit

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


def plot_bist(timestamps, bist_result, ax, y_range=(None,None),xlabel = 'Time', ylabel = 'Voltage', title=None, xrotation=60):
    out = ax.plot(timestamps,bist_result)
    ax.scatter(timestamps,bist_result)
    ax.set_xticklabels(ax.get_xticklabels(), rotation = xrotation)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(y_range[0],y_range[1])
    ax.set_title(title)
    return out


def plot_bist2d(timestamps, sample, ax,xlabel='Time', ylabel='Bist Test',title=None,xrotation=60):
    timestamp_bins = np.concatenate([timestamps,np.array([timestamps[-1] + (timestamps[-1] - timestamps[-2])])])
    if type(timestamps[0]) is float:
        timestamp_bins -= 0.001
    a,b = np.meshgrid(timestamps,np.arange(0,12,(12/48)))
    ax.hist2d(a.flatten(),b.flatten(),weights=sample,bins=(timestamp_bins,np.arange(0,12,(12/48))-0.001),cmap='bwr_r',vmin=0,vmax=1);
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
    parser.add_argument('--chip', default = 'chip003') # repo name on github json repo
    args = parser.parse_args()

    # Path to JSONs
    path = args.path + '/' + args.chip + '/'
    print(f"Running on {path}")

    # Fetch JSON name
    fnames = get_fnames(path)

    # Plotting

    plots = create_plot_path(args.path+ '/' + 'bist_vs_tid_plots-%s'%args.chip)

    timestamps, voltages, pp, ob, goodinit = getBistData(fnames)
    tid, xray_on = datetime_to_TID(timestamps, ObelixDoseRate, xray_start_stop[args.chip])
    tid = np.array(tid)
    xray_on = np.array(xray_on)

    v_pp_lowpass, v_pp_highfail = getBistFailureVoltages(pp,voltages)
    v_ob_lowpass, v_ob_highfail = getBistFailureVoltages(ob,voltages)

    #pp bist vs tid
    fig,axs=plt.subplots(figsize=(45,30),ncols=6,nrows=5, layout="constrained")
    for i_v in range(30):
        sample = np.swapaxes(pp[:,i_v],0,1).reshape(48,-1)[:,xray_on].flatten()
        plot_bist2d(tid[xray_on], sample,axs.flatten()[i_v], title=f'V={voltages[i_v]:0.2f}', xlabel='TID (MRad)');
    for ax in axs.flat:
        ax.label_outer()
    fig.savefig(f'{plots}/pp_bist.png', dpi=300, facecolor="w")
    plt.close(fig)

    #pp bist vs time
    fig,axs=plt.subplots(figsize=(45,30),ncols=6,nrows=5, layout="constrained")
    for i_v in range(30):
        sample = np.swapaxes(pp[:,i_v],0,1).reshape(48,-1).flatten()
        plot_bist2d(timestamps, sample,axs.flatten()[i_v], title=f'V={voltages[i_v]:0.2f}');
    for ax in axs.flat:
        ax.label_outer()
    fig.savefig(f'{plots}/pp_bist_vs_time.png', dpi=300, facecolor="w")
    plt.close(fig)

    #ob bist vs tid
    fig,axs=plt.subplots(figsize=(45,30),ncols=6,nrows=5, layout="constrained")
    for i_v in range(30):
        sample = np.swapaxes(ob[:,i_v],0,1).reshape(48,-1)[:,xray_on].flatten()
        plot_bist2d(tid[xray_on], sample,axs.flatten()[i_v], title=f'V={voltages[i_v]:0.2f}', xlabel='TID (MRad)');
    for ax in axs.flat:
        ax.label_outer()
    fig.savefig(f'{plots}/ob_bist.png', dpi=300, facecolor="w")
    plt.close(fig)

    #ob bist vs time
    fig,axs=plt.subplots(figsize=(45,30),ncols=6,nrows=5, layout="constrained")
    for i_v in range(30):
        sample = np.swapaxes(ob[:,i_v],0,1).reshape(48,-1).flatten()
        plot_bist2d(timestamps, sample,axs.flatten()[i_v], title=f'V={voltages[i_v]:0.2f}');
    for ax in axs.flat:
        ax.label_outer()
    fig.savefig(f'{plots}/ob_bist_vs_time.png', dpi=300, facecolor="w")
    plt.close(fig)

    for i_test in range(4):
        #pp test vs tid
        fig,ax = plt.subplots(1,1)
        plot_bist(tid[xray_on],
                  v_pp_lowpass[i_test,xray_on].max(axis=-1),
                  ax=ax,
                  xlabel='TID (MRad)',
                  y_range=(None,None),
                  title=f'PingPing BIST test {i_test+1} lowest voltage')
        fig.savefig(f'{plots}/pp_test{i_test+1}_voltage_bist.png', dpi=300, facecolor="w")
        plt.close(fig)

        fig,ax = plt.subplots(1,1)
        plot_bist(timestamps,
                  v_pp_lowpass[i_test].max(axis=-1),
                  ax=ax,
                  y_range=(None,None),
                  title=f'PingPing BIST test {i_test+1} lowest voltage')

        fig.savefig(f'{plots}/pp_test{i_test+1}_voltage_bist_vs_time.png', dpi=300, facecolor="w")
        plt.close(fig)

        fig,ax = plt.subplots(1,1)
        plot_bist(tid[xray_on],
                  v_ob_lowpass[i_test,xray_on].max(axis=-1),
                  ax=ax,
                  xlabel='TID (MRad)',
                  y_range=(None,None),
                  title=f'OutputBuffer BIST test {i_test+1} lowest voltage')

        fig.savefig(f'{plots}/ob_test{i_test+1}_voltage_bist.png', dpi=300, facecolor="w")
        plt.close(fig)

        fig,ax = plt.subplots(1,1)
        plot_bist(timestamps,
                  v_ob_lowpass[i_test].max(axis=-1),
                  ax=ax,
                  y_range=(None,None),
                  title=f'OutputBuffer BIST test {i_test+1} lowest voltage')

        fig.savefig(f'{plots}/ob_test{i_test+1}_voltage_bist_vs_time.png', dpi=300, facecolor="w")
        plt.close(fig)

        fig,ax = plt.subplots(4,3,figsize=(30,40))
        for i_sram in range(12):
            plot_bist(tid[xray_on],
                      v_pp_lowpass[i_test,xray_on,i_sram],
                      ax=ax.flatten()[i_sram],
                      xlabel='TID (MRad)',
                      y_range=(0.89,1.2),
                      title=f'PingPing BIST test {i_test+1} SRAM {i_sram}')
        fig.savefig(f'{plots}/pp_test{i_test+1}_voltage_bist_by_sram.png', dpi=300, facecolor="w")
        plt.close(fig)

        fig,ax = plt.subplots(4,3,figsize=(30,40))
        for i_sram in range(12):
            plot_bist(timestamps,
                      v_pp_lowpass[i_test,:,i_sram],
                      ax=ax.flatten()[i_sram],
                      y_range=(0.89,1.2),
                      title=f'PingPing BIST test {i_test+1} SRAM {i_sram}')
        fig.savefig(f'{plots}/pp_test{i_test+1}_voltage_bist_by_sram_vs_time.png', dpi=300, facecolor="w")
        plt.close(fig)

        fig,ax = plt.subplots(4,3,figsize=(30,40))
        for i_sram in range(12):
            plot_bist(tid[xray_on],
                      v_ob_lowpass[i_test,xray_on,i_sram],
                      ax=ax.flatten()[i_sram],
                      xlabel='TID (MRad)',
                      y_range=(0.89,1.2),
                      title=f'OutputBuffer BIST test {i_test+1} SRAM {i_sram}')
        fig.savefig(f'{plots}/ob_test{i_test+1}_voltage_bist_by_sram.png', dpi=300, facecolor="w")
        plt.close(fig)

        fig,ax = plt.subplots(4,3,figsize=(30,40))
        for i_sram in range(12):
            plot_bist(timestamps,
                      v_ob_lowpass[i_test,:,i_sram],
                      ax=ax.flatten()[i_sram],
                      y_range=(0.89,1.2),
                      title=f'OutputBuffer BIST test {i_test+1} SRAM {i_sram}')
        fig.savefig(f'{plots}/ob_test{i_test+1}_voltage_bist_by_sram_vs_time.png', dpi=300, facecolor="w")
        plt.close(fig)

