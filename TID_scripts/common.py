# Tools to get setup for TID in July 19th 2024 
# Common tools to parse / load json files

import numpy as np
import glob
import json

from datetime import datetime
from datetime import timedelta
import mplhep
import matplotlib.colors as mcolors
import matplotlib.scale
import matplotlib as mpl
import matplotlib.pyplot as plt

import os

MYROOT = os.environ['MYROOT']

mplhep.style.use(mplhep.style.CMS)

voltages = [1.08, 1.11, 1.14, 1.20, 1.26, 1.29, 1.32]

def jsonload(fname):
    with open(fname) as jsonfile:
        try:
            return json.load(jsonfile)
        except Exception:
            print(fname)

def get_timestamp0(fnames):
    time1 = fnames[0].split("_")[-2]
    time2 = fnames[0].split("_")[-1].split(".json")[0]
    timegood = time1+" "+time2
    startTime = datetime.strptime(timegood, "%Y-%m-%d %H-%M-%S")
    return startTime

def get_data(path_to_json):
    fnames = list(np.sort(glob.glob(f"{path_to_json}/report*.json")))
    startTime = get_timestamp0(fnames)
    data = [jsonload(fname) for fname in fnames]
    return data, startTime

def get_fnames(path_to_json):
    return list(np.sort(glob.glob(f"{path_to_json}/report*.json")))



def Timestamp2MRad(input, startTime):
    #Example
    #Timestamp2MRad(data[0]['tests'][0]['metadata']['Timestamp'])
    goodTimes = np.array([datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f") for x in input])
    delTimes = [x - startTime for x in goodTimes]
    delTimes = np.array(delTimes)
    delTimes = delTimes/timedelta(minutes=1)
    rad_dose = 9.2/60
    megarad_dose = rad_dose*delTimes - 60 # offset
    return megarad_dose

def Timestamp2XrayBool(input):
    #Example
    #Timestamp2MRad(data[0]['tests'][0]['metadata']['Timestamp'])
    goodTimes = np.array([datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f") for x in input])

    xrays = []
    for el in goodTimes:
        xrays.append(get_xray_bool(el))
    return np.array(xrays)


def FNames2MRad(fnames):
    goodTimes = []

    for fname in fnames:
        time1 = fname.split("_")[-2]
        time2 = fname.split("_")[-1].split(".json")[0]
        timegood = time1+" "+time2
        goodTimes.append(timegood)
        
    goodTimes = [datetime.strptime(x, "%Y-%m-%d %H-%M-%S") for x in goodTimes]
    delTimes = [x - goodTimes[0] for x in goodTimes]
    delTimes = np.array(delTimes)
    delTimes = delTimes/timedelta(minutes=1)
    rad_dose = 9.2/60
    megarad_dose = rad_dose*delTimes - 60
    return megarad_dose


def create_plot_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


# d = datetime.date(2022, 12, 25) example date

xray_times = {'start' : [datetime(2024,7,18,20,55),datetime(2024,7,19,18,21)], 
              'end' : [datetime(2024,7,19,15,49),datetime(2024,7,21,23,27) ], 
}

# function to get if run is during x-ray or not

def get_xray_bool(timestamp):
    xray_bool = False
    start_times = xray_times['start']
    end_times = xray_times['end']

    for i in range(len(end_times)):
        start = start_times[i]
        end = end_times[i]
        if (timestamp > start)&(timestamp < end): xray_bool = True

    if len(start_times) == len(end_times) + 1: # should always be the same or 1 more
        start = start_times[-1]
        if timestamp > start: xray_bool = True

    return xray_bool
