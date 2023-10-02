#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  3 22:10:12 2022

@author: naomiweiss
"""

import spiceypy as spice
import numpy as np
import csv
import os
import glob
import astropy.coordinates
import math as m


# gets angle between two vectors
def get_angle (vector_1, vector_2):
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)
    dot_product = np.dot(unit_vector_1, unit_vector_2)
    angle = np.arccos(dot_product)
    return angle


# rotates a vector by a matrix
def rotation (rotate, v1):    # parameters are the rotation matrix and unit vector
    result = []             # defines the array to be returned

    for r in range(len(rotate)):  # iterates through the rows of the rotation matrix
        sum = 0     
        
        for i in range(len(rotate[0])):   # iterates through a row of the rotation matrix
            sum += rotate[r][i] * v1[i]   # multiplies every value in that row with
                                          # with every value in the vector and sums them
                                          
        result.append(sum)   # adds the previously calculated component of the vector to an array
                                 
    return result        # returns the newly rotated vector as cartesian coords in a 1d array


# converts a vector from cartesian to spherical coords
def cart2sph(x, y, z):
    r = m.sqrt((x*x) + (y*y) + (z*z))           # r
    theta = m.acos(z/r)                          # theta
    if (y < 0):                                 # phi
        phi = (2*m.pi - m.acos(x / m.sqrt((x*x) + (y*y))))
    else:
        phi = m.acos(x/m.sqrt((x*x) + (y*y)))
    return theta, phi

# load spice kernels
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# # get list of all mgs ephemeris files 
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

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


# open mgs file with count rate information and make lists of the date,
# sza, and count rate
file = '/Users/naomiweiss/SSL Files/mgs sep event files/mgs_info recent (without sep events).csv'
with open(file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    date = []; count_rate = []; sza = []
    for row in csv_reader:
        date.append(row[0])
        count_rate.append(row[5])
        sza.append(row[6])
    del date[0]; del sza[0]; del count_rate[0]


# convert times to et times
et_times = []
for d in date:
    t = spice.str2et(d)
    et_times.append(t)
    
    
# setting reference frame and target/observer
rf_l = 'MGS_LEFT_SOLAR_ARRAY'
rf_r = 'MGS_RIGHT_SOLAR_ARRAY'
rf_sc = 'MGS_SPACECRAFT'


# define new lists 
transform_l = []
new_crs = []
new_sza = []
new_date = []
l_theta = []
l_phi = []

# unit vector used in solar array frame that is then rotated to spacecraft frame
unit_vector = [0,0,1]


# iterate through lists and get the matrix for transforming vectors between
# MGS and the left solar array, then transform the unit vector and erase all 
# dates thatthrow an error by updating the lists
for i in range(len(date)):
   
    try:
        rotate_l = spice.pxform(rf_r, rf_sc, et_times[i])
        transform_l.append(rotation(rotate_l, unit_vector))
        
        new_crs.append(count_rate[i])
        new_date.append(date[i])
        new_sza.append(sza[i])
        
    except Exception:
        pass


# change the transformed unit vectors from cartesian to spherical coords
for i in transform_l:
    [theta, phi] = cart2sph(i[0],i[1],i[2])
    l_theta.append((theta*180)/m.pi)
    l_phi.append((phi*180)/m.pi)
    



# write data to files
with open('/Users/naomiweiss/SSL Files/spyder scripts/mgs_vector(0,0,1)_from_right_sa_to_sc.csv','w') as f:
    writer=csv.writer(f)
    header='Date', 'Count Rate', 'SZA','Left Theta', "Left Phi", "Cartesian Vector"
    writer.writerow(header)
    for d, cr, sza, lt, lp, c in zip(new_date, new_crs, new_sza, l_theta, l_phi, transform_l):
        writer.writerow([d] + [cr] + [sza] + [lt] + [lp] + [c]) 
   
    
   
        
    
    
    
    
    


