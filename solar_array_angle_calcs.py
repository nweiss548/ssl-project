#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 08:13:10 2022

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
import astropy.coordinates
import math

def get_angle (vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    return angle

def rotation (rotate, v1):
    result = []
    for r in range(len(rotate)):
        sum = 0
        for i in range(len(rotate[0])):
            sum += rotate[r][i] * v1[i]
        result.append(sum)
    return result

def cart2sph(x,y,z):
    XsqPlusYsq = x**2 + y**2
    r = math.sqrt(XsqPlusYsq + z**2)               # r
    elev = math.atan2(z,math.sqrt(XsqPlusYsq))     # theta
    az = math.atan2(y,x)                           # phi
    return r, elev, az

# get list of all mgs ephemeris files 
# data_folder = "/Users/naomiweiss/SSL Files/mars project files/kernels/"
# pos_files = glob.glob(os.path.join(data_folder, 'mgs_pos','*'))
# pos_files = sorted(pos_files)

# # get list of all mgs ephemeris files 
# ck_files = glob.glob(os.path.join(data_folder, 'mgs_ck_files','*'))
# ck_files = sorted(ck_files)


# mgs_sclk_files = glob.glob(os.path.join(data_folder, 'mgs_sclk_files','*'))
# mgs_sclk_files = sorted(mgs_sclk_files)

# # get path to leap second kernel and frame kernel
# lsk_kern = os.path.join(data_folder, "naif0012.tls")
# frame_kern1 = os.path.join(data_folder, "maven_v09.tf.txt")
# frame_kern2 = os.path.join(data_folder, 'mgs_v10.tf.txt')
# frame_kern3 = os.path.join(data_folder, 'mgs_hga_v10.tf')
# solar_system_kern = os.path.join(data_folder, "de405.bsp")
# pck_kern = os.path.join(data_folder, "PCK00010.TPC.txt")

# # furnsh files
# spice.furnsh(pos_files)
# spice.furnsh(ck_files)
# spice.furnsh(mgs_sclk_files)

# spice.furnsh(pck_kern)
# spice.furnsh(lsk_kern)
# spice.furnsh(frame_kern1)
# spice.furnsh(frame_kern2)
# spice.furnsh(frame_kern3)
# spice.furnsh(solar_system_kern)


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



et_times = []
for d in date:
    t = spice.str2et(d)
    et_times.append(t)
    
# setting reference frame and target/observer
rf_l = 'MGS_LEFT_SOLAR_ARRAY'
rf_r = 'MGS_RIGHT_SOLAR_ARRAY'
rf_sc = 'MGS_SPACECRAFT'



transform_r = []; transform_l = []; dist_negy = []; dist_posy = []; mgs_to_sun = []; crs = []
new_crs = []
new_sza = []
new_date = []

vector = [0,1,0]
for i in range(len(date)):
    try:
        rotate_l = spice.pxform(rf_l, rf_sc, et_times[i])
        rotate_r = spice.pxform(rf_r, rf_sc, et_times[i])
        
        transform_l.append(rotation(rotate_l, vector))
        transform_r.append(rotation(rotate_r, vector))
     
        
        new_crs.append(count_rate[i])
        new_date.append(date[i])
        new_sza.append(sza[i])
        
    except Exception:
        pass

r_theta = []; l_theta = []
r_phi = []; l_phi = []


for i in transform_r:
    [r, theta, phi] = cart2sph(i[0],i[1],i[2])
    r_theta.append((theta*180)/math.pi)
    r_phi.append((phi*180)/math.pi)

for i in transform_l:
    [l, theta, phi] = cart2sph(i[0],i[1],i[2])
    l_theta.append((theta*180)/math.pi)
    l_phi.append((phi*180)/math.pi)


with open('/Users/naomiweiss/SSL Files/spyder scripts/mgs_sa_angles(unit vector (0,1,0)).csv','w') as f:
    writer=csv.writer(f)
    header='Date', 'Count Rate', 'SZA', 'Right Theta', 'Left Theta', 'Right Phi', "Left Phi"
    writer.writerow(header)
    for d, cr, sza, rt, lt, rp, lp in zip(new_date, new_crs, new_sza, r_theta, l_theta, r_phi, l_phi):
        writer.writerow([d] + [cr] + [sza] + [rt] + [lt] + [rp] + [lp])
   
    
   
    
