#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 14:36:24 2021

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

# convert times to datetime objects
def convert_to_dates(times):
    dates = []
    for t in times:
        year = int(t[0:4]); month = int(t[5:7]); day = int(t[8:10]); hour = int(t[16:])
        dt = datetime(year, month, day, hour)
        dates.append(dt)
    return dates

# given two time stamps return a list of the times and count values between them
def pick_date_range(start, stop, dates, counts):
    new_dates = []; new_counts = []
    for d, c in zip(dates, counts): 
        if(datetime.date(d) > datetime.date(start) and datetime.date(d) < datetime.date(stop)):
            new_dates.append(d)
            new_counts.append(c)
    return new_dates, new_counts

# get list of all mgs ephemeris files 
data_folder = "/Users/naomiweiss/SSL Files/mars project files/kernels/"
pos_files = glob.glob(os.path.join(data_folder, 'mex_pos','*'))
pos_files = sorted(pos_files)
cr_files = glob.glob(os.path.join(data_folder, 'mex_count_rates','ima counts','*.dat'))
# cr_lbl_files = glob.glob(os.path.join(data_folder, 'mex_count_rates','*.LBL'))
cr_files = sorted(cr_files)
    
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

start_times = []; crs = []
for f in cr_files:
    for line in open(f).readlines(): 
        line_arr = line.split(' ')
        
        str_date = line_arr[0].replace('T', ' ')
        start_time = datetime.strptime(str_date,'%Y-%m-%d %H:%M:%S.%f')
        start_times.append(start_time)
        cr = line_arr[1]
        crs.append(cr)

# # pick date range if wanted
# dates, counts = pick_date_range(datetime(2004, 1, 1, 0, 0), datetime(2005, 12, 31, 0, 0), dates, counts)

# convert dates to et
et_times = []
for i in start_times:
    et_times.append(spice.str2et(str(i)))

# set reference frame and target/observer
reference_frame = "MAVEN_MSO"
target = "MEX"
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
    
# make file called mex_ima_2004-2006.csv and write time, altitude, and count data into it
with open('mex_ima_2004-2006.csv','w',newline='') as f:
    writer=csv.writer(f)
    header="Start Time","Altitude","Counts"
    writer.writerow(header)
    for s,a,c in zip(start_times, altitudes, crs):
        writer.writerow([s]+[a]+[c])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
