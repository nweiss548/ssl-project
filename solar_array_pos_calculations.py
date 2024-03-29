#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 10:21:58 2022

@author: naomiweiss
"""

##----------------------------------------
## Not sure what this code/file does
##----------------------------------------

import spiceypy as spice
import numpy as np
import csv
import os
import glob

def get_angle (vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    return angle

# get list of all mgs ephemeris files 
data_folder = "/Users/naomiweiss/SSL Files/mars project files/kernels/"
pos_files = glob.glob(os.path.join(data_folder, 'mgs_pos','*'))
pos_files = sorted(pos_files)

# get list of all mgs ephemeris files 
ck_files = glob.glob(os.path.join(data_folder, 'mgs_ck_files','*'))
ck_files = sorted(ck_files)


mgs_sclk_files = glob.glob(os.path.join(data_folder, 'mgs_sclk_files','*'))
mgs_sclk_files = sorted(mgs_sclk_files)

# get path to leap second kernel and frame kernel
lsk_kern = os.path.join(data_folder, "naif0012.tls")
frame_kern1 = os.path.join(data_folder, "maven_v09.tf.txt")
frame_kern2 = os.path.join(data_folder, 'mgs_v10.tf.txt')
frame_kern3 = os.path.join(data_folder, 'mgs_hga_v10.tf')
solar_system_kern = os.path.join(data_folder, "de405.bsp")
pck_kern = os.path.join(data_folder, "PCK00010.TPC.txt")

# furnsh files
spice.furnsh(pos_files)
spice.furnsh(ck_files)
spice.furnsh(mgs_sclk_files)

spice.furnsh(pck_kern)
spice.furnsh(lsk_kern)
spice.furnsh(frame_kern1)
spice.furnsh(frame_kern2)
spice.furnsh(frame_kern3)
spice.furnsh(solar_system_kern)


with open('/Users/naomiweiss/SSL Files/spyder scripts/mgs_info.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    date = []; local_time = []; altitude = []; count_rate = []
    for row in csv_reader:
        date.append(row[0])
        local_time.append(row[2])
        altitude.append(row[3])
        count_rate.append(row[5])
    del date[0]; del local_time[0]; del altitude[0]; del count_rate[0]

et_times = []
for d in date:
    t = spice.str2et(d)
    et_times.append(t)
    
# setting reference frame and target/observer
rf = 'MAVEN_MSO'
targ = -94000
sun = 10

obsl = -94001
pos_y = -94901

obsr = -94002
neg_y = -94902


distr = []; distl = []; dist_negy = []; dist_posy = []; mgs_to_sun = []; crs = []

for i in range(len(count_rate)):
    try:
        [pos, ltime] = spice.spkgps(targ, et_times[i], rf, obsl)
        # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        distl.append(pos)
        
        [pos, ltime] = spice.spkgps(targ, et_times[i], rf, pos_y)
        # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        dist_posy.append(pos)
        
        [pos, ltime] = spice.spkgps(targ, et_times[i], rf, obsr)
        # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        distr.append(pos)
        
        [pos, ltime] = spice.spkgps(targ, et_times[i], rf, neg_y)
        # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        dist_negy.append(pos)
        
        [pos, ltime] = spice.spkgps(targ, et_times[i], rf, sun)
        # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        mgs_to_sun.append(pos)
        crs.append(count_rate[i])
        
    except Exception:
        pass
   
    

with open('/Users/naomiweiss/SSL Files/spyder scripts/test_sa_pos.csv','w') as f:
    writer=csv.writer(f)
    header='DATE', 'COUNT RATE' ,'SPACECRAFT TO SUN', 'RIGHT SA POSITION', 'MGS -Y SA POSITION', 'LEFT SA POSITION', 'MGS +Y SA POSITION'
    writer.writerow(header)
    for d, cr, s, r, y_neg, l, y_pos in zip(date, crs, mgs_to_sun, distr, dist_negy, distl, dist_posy):
        writer.writerow([d] + [cr] + [s] + [r] + [y_neg] + [l] + [y_pos])
        
        
        
        
