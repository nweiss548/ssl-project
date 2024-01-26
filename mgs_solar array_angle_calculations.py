#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 22:54:13 2022

@author: naomiweiss
"""

##----------------------------------------
## Not sure what this file was for,
## Feel free to take a look but it may 
## not be super illuminating
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


with open('/Users/naomiweiss/SSL Files/mgs sep event files/mgs_info recent (without sep events).csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    date = []; local_time = []; altitude = []; count_rate = []; sza = []
    for row in csv_reader:
        date.append(row[0])
        local_time.append(row[2])
        altitude.append(row[3])
        count_rate.append(row[5])
        sza.append(row[6])
    del date[0]; del local_time[0]; del sza[0]; del count_rate[0]

print(len(count_rate))
print(len(date))
print(len(sza))

et_times = []
for d in date:
    t = spice.str2et(d)
    et_times.append(t)
    
# setting reference frame and target/observer
rf = 'MGS_SPACECRAFT'
targ = -94000
sun = 10

obsl = -94001
pos_y = -94901

obsr = -94002
neg_y = -94902


distr = []; distl = []; dist_negy = []; dist_posy = []; mgs_to_sun = []; crs = []
new_crs = []
new_sza = []
new_date = []
for i in range(len(date)):
    try:
        [pos, ltime] = spice.spkgps(targ, et_times[i], rf, obsl)
        # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        distl.append(pos)
        
        # [pos, ltime] = spice.spkgps(targ, et_times[i], rf, pos_y)
        # # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        # dist_posy.append(pos)
        
        [pos, ltime] = spice.spkgps(targ, et_times[i], rf, obsr)
        # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        distr.append(pos)
        
        # [pos, ltime] = spice.spkgps(targ, et_times[i], rf, neg_y)
        # # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        # dist_negy.append(pos)
        
        [pos, ltime] = spice.spkgps(targ, et_times[i], rf, sun)
        # [trgepc, srfvec, phase, incdnc, emissn] = spice.ilumin('ELLIPSOID', targ_s, et_times[i], rf, 'NONE', obs_s, pos)
        mgs_to_sun.append(pos)
        
        new_crs.append(count_rate[i])
        new_date.append(date[i])
        new_sza.append(sza[i])
    except Exception:
        pass
   

r_angle = []; l_angle = []
for i in range(len(new_date)):
    r_angle.append(get_angle(mgs_to_sun[i], distr[i]))
    l_angle.append(get_angle(mgs_to_sun[i], distl[i]))
    
print(len(mgs_to_sun))
for i in mgs_to_sun:
    print(i)


# with open('/Users/naomiweiss/SSL Files/spyder scripts/mgs_sa_angles_nonevent(spacecraft_frame).csv','w') as f:
#     writer=csv.writer(f)
#     header='Date', 'Count Rate', 'SZA', 'Right Angle', 'Left Angle'
#     writer.writerow(header)
#     for d, cr, sza, r, l in zip(new_date, new_crs, new_sza, r_angle, l_angle):
#         writer.writerow([d] + [cr] + [sza] + [r] + [l])
        
        
     
        
     
        
     
        
     
        
     
        
     
 
