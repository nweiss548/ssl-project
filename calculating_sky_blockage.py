#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 14:37:50 2021

@author: naomiweiss
"""

import pandas as pd 
import csv
import math

RADIUS = 3389.5

with open('/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    # date = []; local_time = []; 
    altitude = []; count_rate = []
    for row in csv_reader:
        altitude.append(row[1])
        count_rate.append(row[2])


sky_blockages = []
for a in range(1, len(altitude)):
    # get sky blockage
    alt = float(altitude[a])
    p1 = (math.sqrt((2*RADIUS*alt) + (alt*alt))) / (alt+RADIUS)
    sky_blocked = 1 - (0.5*(1+p1))
    sky_blockages.append(sky_blocked)
    
fixed_cr = []
for i in range(len(altitude)-1):
    try: 
        fixed_cr.append( (float(count_rate[i+1]) / (1-sky_blockages[i]) ))
    except:
        fixed_cr.append(' ')
        
df = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv")
df["Sky Blockage Adjusted Counts"] = fixed_cr
df.to_csv("/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv", index=False)