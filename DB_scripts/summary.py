# Script to create database from scratch

import pymongo
import json
from pymongo import MongoClient, InsertOne
import os, glob

import matplotlib.pyplot as plt
import numpy as np

from matplotlib import colors
from matplotlib.ticker import PercentFormatter

import pandas as pd


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--path", help="Path to JSON files", default = './data')
parser.add_argument("--dbname", help="DB name", default = 'jsonDB')
parser.add_argument("--target", help="ECOND or ECONT", default = 'ECOND')
args = parser.parse_args()

# utility scripts

from json_uploader import jsonFileUploader


client = pymongo.MongoClient("mongodb://127.0.0.1:27017") # Connect to local database

# Load DB 

mydatabase = client[args.dbname] # create new database
mycol = mydatabase[args.target] # dict of type {'unique_id' : json_full_report}

results = []

for obj in mycol.find():
    #print(obj['summary'])
    frac = float(obj['summary']['passed']) / obj['summary']['total']
    results.append(frac)

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

fig.savefig('plots/summary.png')


maps = ['passed', 'failed','other',]

counters = {}
total = 0

for obj in mycol.find():
    for key, value in obj['individual_test_outcomes'].items():
        if value == 1:
            if key in counters.keys():
                counters[key][0]+=1
            else:
                counters[key] = [1,0,0]
        elif value == 0:
            if key in counters.keys():
                counters[key][1]+=1
            else:
                counters[key] = [0,1,0]
        elif value == -1:
            if key in counters.keys():
                counters[key][2] += 1
            else:
                counters[key] = [0,0,1]

    total += 1


df = pd.DataFrame(counters, index=maps)
df = df.T
df = df/total

# plot 

cmap = colors.ListedColormap(['green','red','yellow'])
ax = df.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
ax.set_yticklabels(df.index, fontsize=5)
plt.tight_layout()
ax.invert_yaxis()

plt.savefig('plots/summary_tests.png')

plt.clf()

df_non_zero_failed = df[df['failed'] != 0]
ax = df_non_zero_failed.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
ax.set_yticklabels(df_non_zero_failed.index, fontsize=5)
plt.tight_layout()
ax.invert_yaxis()
plt.savefig('plots/summary_tests_failed.png')

plt.clf()

df_non_zero_passed = df[df['passed'] != 0]
ax = df_non_zero_passed.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
ax.set_yticklabels(df_non_zero_passed.index, fontsize=5)
plt.tight_layout()
ax.invert_yaxis()
plt.savefig('plots/summary_tests_passed.png')

plt.clf()

df_non_zero_other= df[df['other'] != 0]
ax = df_non_zero_other.plot.barh(stacked=True, cmap=cmap, figsize=(10, 6))
ax.set_yticklabels(df_non_zero_other.index, fontsize=5)
plt.tight_layout()
ax.invert_yaxis()
plt.savefig('plots/summary_tests_other.png')

