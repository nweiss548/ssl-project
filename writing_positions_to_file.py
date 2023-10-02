#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 11:58:23 2021

@author: naomiweiss
"""
import csv 
import spiceypy as spice
import glob
import os
import pandas as pd

data_folder = "/Users/naomiweiss/SSL Files/mars project files/kernels/"
mgs_pos_files = glob.glob(os.path.join(data_folder, 'mgs_pos','*'))
mgs_pos_files = sorted(mgs_pos_files)

data_folder = "/Users/naomiweiss/SSL Files/mars project files/kernels/"
mex_pos_files = glob.glob(os.path.join(data_folder, 'mex_pos','*'))
mex_pos_files = sorted(mex_pos_files)

lsk_kern = os.path.join(data_folder, "naif0012.tls")
frame_kern = os.path.join(data_folder, "maven_v09.tf.txt")
solar_system_kern = os.path.join(data_folder, "de405.bsp")
pck_kern = os.path.join(data_folder, 'PCK00010.TPC.txt')

spice.furnsh(lsk_kern)
spice.furnsh(frame_kern)
spice.furnsh(solar_system_kern)
spice.furnsh(pck_kern)
spice.furnsh(mgs_pos_files)
spice.furnsh(mex_pos_files)

with open('/Users/naomiweiss/SSL Files/spyder scripts/mgs_info.csv') as mgs_file:
    with open('/Users/naomiweiss/SSL Files/spyder scripts/mex_info.csv') as mex_file:
        mgs_reader = csv.reader(mgs_file, delimiter=',')
        mex_reader = csv.reader(mex_file, delimiter=',')
        
        exclude_header = 0
        
        mgs_dict = {}
        for row in mgs_reader:
            if(exclude_header == 0):
                exclude_header+=1
            else:
                mgs_dict[row[0][:16]] = row[1:]

        exclude_header = 0

        mex_dict = {}
        for row in mex_reader:
            if(exclude_header == 0):
                exclude_header+=1
            else:
                mex_dict[row[0][:16]] = row[2:]


common_keys = []
for k in mgs_dict.keys():
    if k in mex_dict:
        common_keys.append(k)

et_times = []
for i in common_keys:
    et_times.append(spice.str2et(str(i)))

reference_frame = "J2000"
observer = "MARS"

print(len(et_times))
mgs_positions = []
mex_positions = []
for t in et_times:
    # [mgs_pos, ltime] = spice.spkpos('MGS', t, reference_frame,'NONE', observer)
    [mex_pos, ltime] = spice.spkpos('MEX', t, reference_frame,'NONE', observer)
    # mgs_positions.append(mgs_pos)
    mex_positions.append(mex_pos)
    print(len(mex_positions))

df = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/positions_for_common_times(J2000).csv")
df["MEX Pos"] = mex_positions
df.to_csv("/Users/naomiweiss/SSL Files/spyder scripts/positions_for_common_times(J2000).csv", index=False)

    
    
    

    
    
    