import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()

odir = args.odir + '/currentThresholds'
if not os.path.isdir(odir):
    os.makedirs(odir)



mongo = Database(args.dbaddress, client = 'econdDB')

current, voltage,  current_during_hardreset, current_after_hardreset, current_during_softreset, current_after_softreset, current_runbit_set = mongo.getVoltageAndCurrent()


thresholds = {
    'current':[0.235,0.265],
    'current_during_hardreset':[0.270,0.290],
    'current_after_hardreset':[0.240, 0.260],
    'current_during_softreset':[0.250,0.270],
    'current_after_softreset':[0.240, 0.260],
    'current_runbit_set':[0.235, 0.255],                         
}

def plotCurrentAndThresholds(var, stringVar, thresholds, odir=odir):
    values, bins = np.histogram(var, bins = 100)
    lowVals = np.argwhere(bins <= thresholds[0])
    highVals = np.argwhere(bins >= thresholds[1])
    totalFail = np.sum(values[lowVals]) + np.sum(values[highVals[0][0]:])
    fracFail = np.round((totalFail/len(var)),3)
    plt.title(f'{stringVar} - 1.20V')
    plt.axvline(thresholds[0], color='k', linewidth=2)
    plt.axvline(thresholds[1], color='k', linewidth=2)
    plt.hist(var, bins = 100, label = f'N: {len(var)} \nAvg: {np.round(np.average(var),3)}A \nSt.Dev: {np.round(np.average(var),3)}A \nLow Threshold: {thresholds[0]}A \nHigh Threshold: {thresholds[1]}A \nFrac Failed: {fracFail}')
    plt.yscale('log')
    plt.legend()
    plt.ylim(0.1,3000)
    plt.xlim(0.01,0.7)
    plt.ylabel('Number of chips')
    plt.xlabel('Current (A)')
    plt.savefig(f'{odir}/{stringVar}_thresholdPlot.png', dpi=300, facecolor='w')
    plt.clf()

plotCurrentAndThresholds(var=current, stringVar='Current', thresholds = thresholds['current'])
plotCurrentAndThresholds(var=current_during_hardreset, stringVar='current_during_hardreset', thresholds = thresholds['current_during_hardreset'])
plotCurrentAndThresholds(var=current_after_hardreset, stringVar='current_after_hardreset', thresholds = thresholds['current_after_hardreset'])
plotCurrentAndThresholds(var=current_during_softreset, stringVar='current_during_softreset', thresholds = thresholds['current_during_softreset'])
plotCurrentAndThresholds(var=current_after_softreset, stringVar='current_after_softreset', thresholds = thresholds['current_after_softreset'])
plotCurrentAndThresholds(var=current_runbit_set, stringVar='current_runbit_set', thresholds = thresholds['current_runbit_set'])
