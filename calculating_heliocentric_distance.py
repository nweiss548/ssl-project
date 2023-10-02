#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 09:36:26 2022

@author: naomiweiss
"""


import csv
from scipy.io import readsav
import datatable as dt
import spiceypy as spice
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import glob
import os


def convert_list_of_utc_times_to_dates(t):
    times = np.empty(len(t), dtype = object)
    for i in range(len(times)):
        times[i] = datetime.utcfromtimestamp(int(t[i]))
    return times

# get list of all mgs ephemeris files 
df = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/mgs_info.csv")

times = df['Start Time']

et_times = []
for i in times:
    et_times.append(spice.str2et(str(i)))

# set reference frame and target/observer
reference_frame = "MAVEN_MSO"
target = "MGS"
observer = "MARS"

# get position and longitude of spacecraft for the listed times
lons = []; sun_dist = []
for t in et_times:
    [mgs_pos, ltime] = spice.spkpos(target, t, reference_frame,'NONE', observer)
    [rad, lon, lat] = spice.reclat(mgs_pos)
    print(mgs_pos)
    sun_dist.append(int(rad))

  
# df = pd.read_csv('/Users/naomiweiss/SSL Files/spyder scripts/mgs_info.csv')
# df["Heliocentric Distance"] = sun_dist
# df.to_csv('/Users/naomiweiss/SSL Files/spyder scripts/mgs_info.csv', index=False)

















 
    
    