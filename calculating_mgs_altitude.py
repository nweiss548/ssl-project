#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 15:03:37 2021

@author: naomiweiss
"""
# import python packages
import csv
import scipy.io as sio
from scipy.io import readsav
import datatable as dt
import spiceypy as spice
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import os

# convert utc times to datetime objects
def convert_list_of_utc_times_to_dates(t):
    times = np.empty(len(t), dtype = object)
    for i in range(len(times)):
        times[i] = datetime.utcfromtimestamp(int(t[i]))
    return times

# given two time stamps return a list of the times and count values between them
def choose_timeframe(start, stop, times, counts):
    t = []; c = []
    for i in range(len(times)):
        if (times[i] > start and times[i] < stop):
            t.append(times[i])
            c.append(counts[i][2])
    return t, c

# get list of all mgs ephemeris files 
data_folder = "/Users/naomiweiss/SSL Files/mars project files/kernels/"
pos_files = glob.glob(os.path.join(data_folder, 'mgs_pos','*'))
pos_files = sorted(pos_files)

# get count rate data
s = readsav(data_folder+ 'mgs_count_rates'+'/ERBackgrounds_5min.sav')
    
# get path to leap second kernel and frame kernel
lsk_kern = os.path.join(data_folder, "naif0012.tls")
frame_kern = os.path.join(data_folder, "maven_v09.tf.txt")
solar_system_kern = os.path.join(data_folder, "de405.bsp")
pck_kern = os.path.join(data_folder, 'PCK00010.TPC.txt')

# furnsh files
spice.furnsh(pos_files)
spice.furnsh(lsk_kern)
spice.furnsh(frame_kern)
spice.furnsh(pck_kern)
spice.furnsh(solar_system_kern)

print("furnished!")

# put time column and count rate column into python lists
times = s['time']
crs = s['rate']

# convert all utc times to dates and isolate a range of the data 
dates = convert_list_of_utc_times_to_dates(times)
dates, crs = choose_timeframe(datetime(2001, 3, 1), datetime(2001, 6, 30), dates, crs)
    
# convert datetime objects to et
et_times = []
for i in dates:
    et_times.append(spice.str2et(str(i)))

# set reference frame and target/observer
reference_frame = "MAVEN_MSO"
target = "MGS"
observer = "MARS"

# get position and longitude of spacecraft for the listed times
lons = []; altitudes = []
for t in et_times:
    [mgs_pos, ltime] = spice.spkpos(target, t, reference_frame,'NONE', observer)
    [rad, lon, lat] = spice.reclat(mgs_pos)
    lons.append(lon)
    altitudes.append(rad-3389)

# calculate local times and save in local_times
local_times = []
for l, t in zip(lons, et_times):
    [hour, minute, second, local_time, local_ampm] = spice.et2lst(t, 499, l, 'PLANETOCENTRIC')
    local_times.append(local_time)
    
# make file called mgs_2001_info.csv and write data into it
with open('mgs_2001_info.csv','w',newline='') as f:
    writer=csv.writer(f)
    header="Start Time","Local Time","Altitude","Counts"
    writer.writerow(header)
    for d, lt,a,c in zip(dates, local_times, altitudes, crs):
        writer.writerow([d]+[lt]+[a]+[c])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
