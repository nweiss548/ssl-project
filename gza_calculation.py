#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 12:56:03 2021

@author: naomiweiss
"""

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
import numpy as np
import pandas as pd
import math

NOSE = [-0.2578341605, -0.9622501869, 0.0871557427]

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

# get list of all mex ephemeris files 
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
    date = []; local_time = []; 
    altitude = []; count_rate = []
    for row in csv_reader:
        date.append(row[0])
    del date[0]

et_times = []
for d in date:
    t = spice.str2et(d)
    et_times.append(t)
    
# setting reference frame and target/observer
rf = 'J2000'
targ = 'MEX'
obs = 'MARS'


gza = []
for i in range(len(et_times)):
    [mex_pos, ltime] = spice.spkpos(targ, et_times[i], rf,'NONE', obs)
    gza.append((angle(mex_pos, NOSE)*180)/math.pi)

    
df = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv")
df["GZA"] = gza
df.to_csv("/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv", index=False)
 


# with open('mex_info (without sep events) gza.csv','w',newline='') as f:
#     writer=csv.writer(f)
#     header='DATE', 'GZA'
#     writer.writerow(header)
#     for d, g in zip(date, gza):
#         writer.writerow([d] + [g])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
 