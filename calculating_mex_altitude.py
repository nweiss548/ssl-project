#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 11:24:00 2021

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


def get_count_rate_vs_time_all_lines(f):
    countRateArr = []; timeArr = []
    for l in f:
        lineArr = l.split(" ")
        if (lineArr[0] != "#" and len(lineArr) > 1):
            timeArr.append(lineArr[0])
            countRateArr.append(float(lineArr[3]))
    arr = [timeArr, countRateArr]
    return arr

# def convert_to_dates(times):
#     dates = []
#     for t in times:
#         year = int(t[0:4]); month = int(t[5:7]); day = int(t[8:10]); hour = int(t[16:])
#         dt = datetime(year, month, day, hour)
#         dates.append(dt)
#     return dates

def pick_date_range(start, stop, dates, counts):
    new_dates = []; new_counts = []
    for d, c in zip(dates, counts): 
        if(datetime.date(d) > datetime.date(start) and datetime.date(d) < datetime.date(stop)):
            new_dates.append(d)
            new_counts.append(c)
    return new_dates, new_counts

def combine_lists(l1, l2):
    l = []
    for i in l1:
        l.append(i)
    for i in l2:
        l.append(i)
    return l

# get list of all mgs ephemeris files 
data_folder = "/Users/naomiweiss/SSL Files/mars project files/kernels/"
pos_files = glob.glob(os.path.join(data_folder, 'mex_pos','*'))
pos_files = sorted(pos_files)
cr_files = glob.glob(os.path.join(data_folder, 'mex_count_rates','in_use','*.CSV'))
cr_lbl_files = glob.glob(os.path.join(data_folder, 'mex_count_rates','*.LBL'))
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

long_start_times = []; long_end_times = []; long_crs = []
for f in cr_files:
    for line in open(f).readlines(): 
        line_arr = line.split(',')
        if (len(line_arr) > 6):
            start_time = datetime.strptime(line_arr[0],'%Y-%jT%H:%M:%S.%f')
            long_start_times.append(start_time)
            cr = line_arr[-1].rstrip()
            long_crs.append(cr)

start_times = []; crs = []
for i in range(0, len(long_start_times)-16, 16):
    start_times.append(long_start_times[i])
    avg = 0; to_divide = 0
    for j in range(16):
        if(long_crs[i+j] != ''):
            avg += float(long_crs[i+j])
            to_divide +=1
    crs.append(avg/to_divide)
    

# # pick date range
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
altitudes = []
for t in et_times:
    [mgs_pos, ltime] = spice.spkpos(target, t, reference_frame,'NONE', observer)
    [rad, lon, lat] = spice.reclat(mgs_pos)
    altitudes.append(rad-3389)
    
    
with open('mex_info_through_2019.csv','w',newline='') as f:
    writer=csv.writer(f)
    header="Start Time","Altitude","Counts"
    writer.writerow(header)
    for s,a,c in zip(start_times, altitudes, crs):
        writer.writerow([s]+[a]+[c])
    
    
    
    
    
    
    
    
    
    
    
    
    
    
