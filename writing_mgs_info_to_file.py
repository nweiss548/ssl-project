#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 15:03:37 2021

@author: naomiweiss
"""

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

def find_bin(val, bin_lims):
    for i in (range(len(bin_lims)-1)):
        if(val >= bin_lims[i] and val <= bin_lims[i+1]):
            return i-1
    return -1

def convert_list_of_utc_times_to_dates(t):
    times = np.empty(len(t), dtype = object)
    for i in range(len(times)):
        times[i] = datetime.utcfromtimestamp(int(t[i]))
    return times

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

times = s['time']
crs = s['rate']


dates = convert_list_of_utc_times_to_dates(times)
dates, crs = choose_timeframe(datetime(2001, 3, 1), datetime(2001, 6, 30), dates, crs)
    

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
    
local_times = []
for l, t in zip(lons, et_times):
    [hour, minute, second, local_time, local_ampm] = spice.et2lst(t, 499, l, 'PLANETOCENTRIC')
    local_times.append(local_time)
    

with open('mgs_2001_info.csv','w',newline='') as f:
    writer=csv.writer(f)
    header="Start Time","Local Time","Altitude","Counts"
    writer.writerow(header)
    for d, lt,a,c in zip(dates, local_times, altitudes, crs):
        writer.writerow([d]+[lt]+[a]+[c])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
