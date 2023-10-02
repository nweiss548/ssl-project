#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 21:22:37 2021

@author: naomiweiss
"""

import pandas as pd
import math
import csv

mex = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/mex_info.csv")

cr = mex["Sky Blockage Adjusted CR"]
sza = mex["SZA in degrees"]
sunspot = mex["Sunspot Number"]

converted = 0
converts = []
for i in range(len(cr)):
    if sunspot[i] < 35:
        if sza[i] < 45:
            converted = cr[i]*13.743496429
        if sza[i] >= 45 and sza[i] < 90:
            converted = cr[i]*14.195834635
        if sza[i] >= 90 and sza[i] < 135:
            converted = cr[i]*17.960317338
    elif sunspot[i] >= 35 and sunspot[i] < 70:
        if sza[i] < 45:
            converted = cr[i]*13.910525314
        if sza[i] >= 45 and sza[i] < 90:
            converted = cr[i]*13.640286165
        if sza[i] >= 90 and sza[i] < 135:
            converted = cr[i]*17.210690553
    elif sunspot[i] >= 70 and sunspot[i] < 105:
        if sza[i] < 45:
            converted = cr[i]*17.019916911
        if sza[i] >= 45 and sza[i] < 90:
            converted = cr[i]*13.720160301
        if sza[i] >= 90 and sza[i] < 135:
            converted = cr[i]*17.45359272
    elif sunspot[i] >= 105 and sunspot[i] < 140:
        if sza[i] < 45:
            converted = cr[i]*2.7400340401
        if sza[i] >= 45 and sza[i] < 90:
            converted = cr[i]*11.031935236
        if sza[i] >= 90 and sza[i] < 135:
            converted = cr[i]*14.556359073
    elif sunspot[i] >= 140:
        if sza[i] >= 45 and sza[i] < 90:
            converted = cr[i]*12.061232636
        if sza[i] >= 90 and sza[i] < 135:
            converted = cr[i]*14.817575948
    converts.append(converted)
    converted = 0
    
    
with open('converts.csv','w',newline='') as f:
    writer=csv.writer(f)
    header="Date","Converted Count Rate"
    writer.writerow(header)
    for d, c in zip(mex["Start Time"], converts):
        writer.writerow([d]+[c])
    
    
    
    
    
    
    
    
    