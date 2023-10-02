#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 15:39:43 2021

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
                
# common_keys = []
# for k in mgs_dict.keys():
#     if k in mex_dict:
#         common_keys.append(k)

et_times = []
for i in mex_dict.keys():
    et_times.append(spice.str2et(str(i)))

reference_frame = "Maven_MSO"
observer = "MARS"

print(len(et_times))
mex_mso_positions = []
mex_positions = []
for t in et_times:
    [mex_pos, ltime] = spice.spkpos('MEX', t, reference_frame,'NONE', observer)
    # [mex_pos, ltime] = spice.spkpos('MEX', t, reference_frame,'NONE', observer)
    mex_mso_positions.append(mex_pos)
    # mex_positions.append(mex_pos)
    # print(len(mex_positions))

# reference_frame = "J2000"
# mex_j_positions = []
# for t in et_times:
#     [mex_pos, ltime] = spice.spkpos('MEX', t, reference_frame,'NONE', observer)
#     # [mex_pos, ltime] = spice.spkpos('MEX', t, reference_frame,'NONE', observer)
#     mex_j_positions.append(mex_pos)
#     # mex_positions.append(mex_pos)
#     # print(len(mex_positions))


with open('mex_positions.csv','w',newline='') as f:
    writer=csv.writer(f)
    header="Date","MSO Pos"
    writer.writerow(header)
    for d, m in zip(mex_dict.keys(), mex_mso_positions):
        writer.writerow([d]+[m])






              
                
                
                
                
                
                
                