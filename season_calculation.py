#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 11:30:09 2022

@author: naomiweiss
"""

import math as m
import pandas as pd
import spiceypy as spice

# get list of all mgs ephemeris files 
df = pd.read_csv("/Users/naomiweiss/SSL Files/mgs sep event files/mgs_info recent (without sep events).csv")

times = df['Start Time']

et_times = []
for i in times:
    et_times.append(spice.str2et(str(i)))

# set reference frame and target/observer
reference_frame = "MAVEN_MSO"
target = "MGS"
observer = "MARS"

# get position and longitude of spacecraft for the listed times
solar_lon = []
for t in et_times:
    l = spice.lspcn(observer, t, 'LT')
    l = m.degrees(l)
    solar_lon.append(l)


df["Season"] = solar_lon
df.to_csv('/Users/naomiweiss/SSL Files/mgs sep event files/mgs_info recent (without sep events).csv', index=False)

