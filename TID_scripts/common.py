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

try:
    MYROOT = os.environ['MYROOT']
except:
    MYROOT = None
mplhep.style.use(mplhep.style.CMS)

ObelixDoseRate = 9.212055 #MRad/hr from Giulio
voltages = [1.08, 1.11, 1.14, 1.20, 1.26, 1.29, 1.32]

xray_start_stop = {"chip003":[(np.datetime64('2024-07-18T20:55'),np.datetime64('2024-07-19T15:49')),(np.datetime64('2024-07-19T18:21'),np.datetime64('2024-07-21T23:27'))],
                   "chip002":[(np.datetime64('2024-07-22T19:43'),np.datetime64('2024-07-25T10:08')),],
                   "chip004":[(np.datetime64('2024-07-25T18:55'),None)],
                   "chip001":[(np.datetime64('2024-07-28T17:46'),np.datetime64('2024-07-30T09:06'))],

                   "chip003-subset":[(np.datetime64('2024-07-18T20:55'),np.datetime64('2024-07-19T15:49')),(np.datetime64('2024-07-19T18:21'),np.datetime64('2024-07-21T23:27'))],
                   "chip003-subset-sc-test":[(np.datetime64('2024-07-18T20:55'),np.datetime64('2024-07-19T15:49')),(np.datetime64('2024-07-19T18:21'),np.datetime64('2024-07-21T23:27'))],
                   "chip002-subset":[(np.datetime64('2024-07-22T19:43'),None),],
                   "chip004-subset":[(np.datetime64('2024-07-25T18:55'),None)],
                   "chip001-subset":[(np.datetime64('2024-07-28T17:46'),np.datetime64('2024-07-30T09:06'))],

                   "chip002-econd-subset":[(np.datetime64('2024-07-30T18:53'),np.datetime64('2024-07-31T17:27')),],
                   "chip002-econd":[(np.datetime64('2024-07-30T18:53'),np.datetime64('2024-07-31T17:27')),],
                   "chip005-econd-subset":[(np.datetime64('2024-07-30T12:28'),np.datetime64('2024-07-31T13:58')),],
                   "chip005-econd":[(np.datetime64('2024-07-30T12:28'),np.datetime64('2024-07-31T13:58')),],
                  
                  }

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



def datetime_to_TID(timestamp, doseRate, xray_start_stop = [(None,None)]):
    """
    Convert timestamps into TID doses
    """

    TID=[]
    xray_on = []
    for t in timestamp:
        TID.append(0)
        _xray_on = False
        if t < xray_start_stop[0][0]:
            TID[-1] = (t - xray_start_stop[0][0]).astype('timedelta64[s]').astype(int)/3600.*doseRate
        else:
            for x_start,x_stop in xray_start_stop:
                if t>x_start:
                    if (x_stop is None) or (t<x_stop):
                        _xray_on = True
                        TID[-1] += (t - x_start).astype('timedelta64[s]').astype(int)/3600.*doseRate
                    else:
                        _xray_on = False
                        TID[-1] += (x_stop - x_start).astype('timedelta64[s]').astype(int)/3600.*doseRate
        xray_on.append(_xray_on)
    return TID, xray_on

def datetime_to_TID_chip002(timestamp, doseRate, xray_start_stop = [(None,None)]):
    """
    Convert timestamps into TID doses
    """

    TID=[]
    xray_on = []

    #low_dose = [np.datetime64('2024-07-30T18:53'), np.datetime64('2024-07-30T22:23')]
    #high_dose = [np.datetime64('2024-07-30T22:23'),np.datetime64('2024-07-31T17:27')]

    time_switch = np.datetime64('2024-07-30T22:23')


    for t in timestamp:
        TID.append(0)
        _xray_on = False
        if t < xray_start_stop[0][0]:

            if t < time_switch:
                doseRate = 0.5527233
            else: 
                doseRate = 9.212055
            TID[-1] = (t - xray_start_stop[0][0]).astype('timedelta64[s]').astype(int)/3600.*doseRate
        else:
            for x_start,x_stop in xray_start_stop:
                if t>x_start:
                    if t < time_switch:
                        doseRate = 0.5527233
                    else: 
                        doseRate = 9.212055
                    if (x_stop is None) or (t<x_stop):
                        _xray_on = True
                        TID[-1] += (t - x_start).astype('timedelta64[s]').astype(int)/3600.*doseRate
                    else:
                        _xray_on = False
                        TID[-1] += (x_stop - x_start).astype('timedelta64[s]').astype(int)/3600.*doseRate
        xray_on.append(_xray_on)
    return TID, xray_on

def Timestamp2MRad(input, startTime):
    #Example
    #Timestamp2MRad(data[0]['tests'][0]['metadata']['Timestamp'])
    goodTimes = np.array([datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f") for x in input])
    delTimes = [x - startTime for x in goodTimes]
    delTimes = np.array(delTimes)
    delTimes = delTimes/timedelta(minutes=1)
    rad_dose = 9.2/60
    megarad_dose = rad_dose*delTimes # offset
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
    megarad_dose = rad_dose*delTimes
    return megarad_dose

def FNames2Time(fnames):
    goodTimes = []

    for fname in fnames:
        time1 = fname.split("_")[-2]
        time2 = fname.split("_")[-1].split(".json")[0]
        time2 = time2.replace('-',":")
        timegood = time1+" "+time2
        goodTimes.append(timegood)
        
    #goodTimes = [datetime.strptime(x, "%Y-%m-%d %H-%M-%S") for x in goodTimes]
    goodTimes = [np.datetime64(x) for x in goodTimes]
    return goodTimes




def create_plot_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


# d = datetime.date(2022, 12, 25) example date

xray_times = {'start' : [datetime(2024,7,18,20,55),datetime(2024,7,19,18,21),datetime(2024,7,25,18,55)], 
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
