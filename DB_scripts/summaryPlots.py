import numpy as np
import matplotlib.pyplot as plt
from dbClass import Database
import argparse
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import os
import pandas as pd
parser = argparse.ArgumentParser()
parser.add_argument("--dbaddress", help="db address from local tunnel", default = 27017)
parser.add_argument("--odir", help="output directory", default = './plots')
args = parser.parse_args()
odir = args.odir + '/summary'
if not os.path.isdir(odir):
    os.makedirs(odir)

def summaryPlot(results,econType,odir):
    hist = np.array(results)

    fig, axs = plt.subplots(1, 1, sharey=True, tight_layout=True)

    axs.hist(hist, bins=10)
    axs.set_xlabel('# passed tests / total')
    axs.set_ylabel('Number of chips')
    #axs.set_xlim(0,1)
    axs.axvline(np.percentile(hist, 25), color='red', linestyle='dashed', linewidth=2, label='25th Percentile')
    axs.axvline(np.percentile(hist, 50), color='green', linestyle='dashed', linewidth=2, label='50th Percentile (Median)')
    axs.axvline(np.percentile(hist, 75), color='blue', linestyle='dashed', linewidth=2, label='75th Percentile')
    axs.legend()

    #plt.show()

    fig.savefig(f'{odir}/summary_{econType}.png')
    plt.clf()
def summaryTestPlot(df, econType, odir):
    cmap = colors.ListedColormap(['green','red','yellow','blue'])
    ax = df.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
    ax.set_yticklabels(df.index, fontsize=5)
    plt.tight_layout()
    ax.invert_yaxis()

    plt.savefig(f'{odir}/summary_tests_{econType}.png')

    plt.clf()

    df_non_zero_failed = df[df['failed'] != 0]
    ax = df_non_zero_failed.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
    ax.set_yticklabels(df_non_zero_failed.index, fontsize=5)
    plt.tight_layout()
    ax.invert_yaxis()
    plt.savefig(f'{odir}/summary_tests_failed_{econType}.png')

    plt.clf()

    df_non_zero_passed = df[df['passed'] != 0]
    ax = df_non_zero_passed.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
    ax.set_yticklabels(df_non_zero_passed.index, fontsize=5)
    plt.tight_layout()
    ax.invert_yaxis()
    plt.savefig(f'{odir}/summary_tests_passed_{econType}.png')

    plt.clf()

    df_non_zero_other= df[df['error'] != 0]
    ax = df_non_zero_other.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
    ax.set_yticklabels(df_non_zero_other.index, fontsize=5)
    plt.tight_layout()
    ax.invert_yaxis()
    plt.savefig(f'{odir}/summary_tests_error_{econType}.png')
    plt.clf()
mongo = Database(args.dbaddress)

econtFracPassed = mongo.getFractionOfTestsPassed('ECONT')
econdFracPassed = mongo.getFractionOfTestsPassed()

summaryPlot(econtFracPassed, econType='ECONT', odir=odir)
summaryPlot(econdFracPassed, econType='ECOND', odir=odir)

econtDF = mongo.getTestingSummaries('ECONT')
econdDF = mongo.getTestingSummaries()

summaryTestPlot(econtDF, 'ECONT', odir=odir)
summaryTestPlot(econdDF, 'ECOND', odir=odir)
