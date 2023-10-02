#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 10:32:15 2021

@author: naomiweiss
"""
import spiceypy as spice
import csv
import os
import glob
import pandas as pd
import math

# get list of all mgs ephemeris files 
data_folder = "/Users/naomiweiss/SSL Files/mars project files/kernels/"
pos_files = glob.glob(os.path.join(data_folder, 'mex_pos','*'))
pos_files = sorted(pos_files)

# get path to leap second kernel and frame kernel
lsk_kern = os.path.join(data_folder, "naif0012.tls")
frame_kern = os.path.join(data_folder, "maven_v09.tf.txt")
solar_system_kern = os.path.join(data_folder, "de405.bsp")
pck_kern = os.path.join(data_folder, "PCK00010.TPC.txt")

# # furnsh files
# spice.furnsh(pos_files)
# spice.furnsh(pck_kern)
# spice.furnsh(lsk_kern)
# spice.furnsh(frame_kern)
# spice.furnsh(solar_system_kern)


with open('/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    date = [];
    altitude = []; count_rate = []
    for row in csv_reader:
        date.append(row[0])
        # local_time.append(row[1])
        altitude.append(row[1])
        count_rate.append(row[2])
    del date[0]; del altitude[0]; del count_rate[0]

et_times = []
for d in date:
    t = spice.str2et(d)
    et_times.append(t)
    
# setting reference frame and target/observer
rf = 'MAVEN_MSO'
targ = 'MEX'
obs = 'MARS'

sza = []
for i in range(len(count_rate)):
    [mex_pos, ltime] = spice.spkpos(targ, et_times[i], rf,'NONE', obs)
    [trgepc, srfvec, phase, solar, emissn] = spice.ilumin('ellipsoid', obs, et_times[i], rf, 'NONE', targ, mex_pos)
    sza.append((solar*180)/math.pi)
    
df = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv")
df["SZA"] = sza
df.to_csv("/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv", index=False)
 
    
    
    
    
    
    
    
    
    
    
    
    