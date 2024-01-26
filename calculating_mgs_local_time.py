#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:30:35 2021

@author: naomiweiss
"""

import spiceypy as spice
from datetime import datetime, timedelta
import glob
import os


# get list of all mgs ephemeris files 
data_folder = "/Users/naomiweiss/SSL Files/mars project files/kernels/"
pos_files = glob.glob(os.path.join(data_folder, 'mgs_pos','*'))
pos_files = sorted(pos_files)

# get path to leap second kernel and frame kernel
lsk_kern = os.path.join(data_folder, "naif0012.tls")
frame_kern = os.path.join(data_folder, "maven_v09.tf.txt")
solar_system_kern = os.path.join(data_folder, "de405.bsp")

# furnsh files
spice.furnsh(pos_files)
spice.furnsh(lsk_kern)
spice.furnsh(frame_kern)
spice.furnsh(solar_system_kern)


# get time range
start_time = datetime(2004, 6, 24)

start_time = start_time.replace(minute=0, second=0, microsecond=0)
utc_time_range = [start_time + timedelta(minutes=x) for x in range(0, 24 * 60, 5)]

# convert utc time range to et
et_times = []
for i in utc_time_range:
    et_times.append(spice.str2et(str(i)))

# setting reference frame and target/observer
reference_frame = "MAVEN_MSO"
target = "MGS"
observer = "MARS"


# getting position and longitude of spacecraft for the listed times
mgs_positions = []; lons = []
for t in et_times:
    [mgs_pos, ltime] = spice.spkpos(target, t, reference_frame,'NONE', observer)
    mgs_positions.append(mgs_pos)
    [rad, lon, lat] = spice.reclat(mgs_pos)
    lons.append(lon)
    

# getting local times based on et times and position
local_times = []
for l, t in zip(lons, et_times):
    [hours, minutes, seconds, local_time, local_ampm] = spice.et2lst(t, 499, l, 'PLANETOCENTRIC')
    local_times.append(local_ampm)
    
    
print(local_ampmasw2)   
    
    
# -------- for one time ------------
# time = str(datetime(2004, 6, 24))
# time = spice.str2et(time)

# # get MGS positions and light time between Mars and mgs
# [mgs_pos, ltime] = spice.spkpos(target, time, reference_frame,'NONE', observer)
# [rad, lon, lat] = spice.reclat(mgs_pos)

# [hours, minutes, seconds, local_time, local_ampm] = spice.et2lst(time, 499, lon, 'PLANETOCENTRIC')

    
    
    



