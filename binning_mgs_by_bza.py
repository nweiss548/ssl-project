#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 10:05:41 2023

@author: naomiweiss
"""

import math as m
import pandas as pd
import spiceypy as spice
import csv

# open csv with count rate, season, heliocentric distance, 
# and bza columns and save each col into a list
df = pd.read_csv("/Users/naomiweiss/SSL Files/mgs sep event files/finding season and sun dist correlation for mgs/low_ssn split/low_ssn.csv")

cr = df['Sky Blockage Adjusted CR']
ls = df["Season"]
sd = df["Heliocentric Distance"]
bza = df["BZA"]

sd_new = []
for i in sd:
    new = i / (1.496*(10**8))
    sd_new.append(new)

cr_60 = []; cr_120 = []; cr_180 = []
ls_60 = []; ls_120 = []; ls_180 = []
sd_60 = []; sd_120 = []; sd_180 = []

# iterate through count rates and depending on the bza value write into appropriate list
# eg if bza < 60 save cr, ls, and sun dist into those lists for the bza range
for i in range(1, len(cr)):
    if bza[i] < 60:
        cr_60.append(cr[i])
        ls_60.append(ls[i])
        sd_60.append(sd_new[i]) 
    elif bza[i] < 120:
        cr_120.append(cr[i])
        ls_120.append(ls[i])
        sd_120.append(sd_new[i]) 
    else:
        cr_180.append(cr[i])
        ls_180.append(ls[i])
        sd_180.append(sd_new[i]) 

# write each set of bza ranges to their own file
with open('low_ssn_60.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     
     writer.writerow(["Sky Blockage Adjusted CR	","Season","Heliocentric Distance"])
     for i in range(len(cr_60)):
         writer.writerow([cr_60[i], ls_60[i], sd_60[i]])
       
         
with open('low_ssn_120.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     
     writer.writerow(["Sky Blockage Adjusted CR	","Season","Heliocentric Distance"])
     for i in range(len(cr_120)):
         writer.writerow([cr_120[i], ls_120[i], sd_120[i]])



with open('low_ssn_180.csv', 'w', newline='') as file:
     writer = csv.writer(file)
     
     writer.writerow(["Sky Blockage Adjusted CR	","Season","Heliocentric Distance"])
     for i in range(len(cr_180)):
         writer.writerow([cr_180[i], ls_180[i], sd_180[i]])

         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
         
