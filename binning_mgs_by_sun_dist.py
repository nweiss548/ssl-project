#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 17:02:47 2023

@author: naomiweiss
"""

import pandas as pd
import csv
import matplotlib.pyplot as plt
import math
from scipy.stats import sem

# open csv with count rate, season, heliocentric distance, 
# and bza columns and save each col into a list
df = pd.read_csv("/Users/naomiweiss/SSL Files/mgs sep event files/finding season and sun dist correlation for mgs/high_ssn split/high_ssn_180.csv")

cr = df['Sky Blockage Adjusted CR	']
ls = df["Season"]
sd = df["Heliocentric Distance"]

# declare min and max sun distances
MIN = 1.38
MAX = 1.67
 
# declare sun distance bins      
avg_cr = []
std_error = []
bins = ['1.38-1.409', '1.409-1.438', '1.438-1.467', '1.467-1.496', '1.496-1.525', '1.525-1.554', '1.554-1.583', '1.583-1.612', '1.612-1.641', '1.641-1.67']
end_bin = [1.409, 1.438, 1.467, 1.496, 1.525, 1.554, 1.583, 1.612, 1.641,1.67]

# calculate the average count rate within each bin and add to list, omitting non numerical values in the data               
for i in range(1409, 1699, 29):
    sum = 0
    num_vals = 0
    std_error_list = []
    for j in range(len(cr)):
        if ((i-29) < (sd[j]*1000))  and ((sd[j]*1000)< i):
            if math.isnan(cr[j]) is False:
                sum += cr[j]
                num_vals+=1
                std_error_list.append(cr[j])
              
    std_error.append(sem(std_error_list, nan_policy='omit'))
    avg_cr.append(sum/num_vals)

# create a file called ls_bin.csv and add the bin sizes and labels as rows, use this when making the first row
# with open('sd_bin.csv', 'w', newline='') as file:
      # writer = csv.writer(file)
     
      # writer.writerow(["Heliocentric Distance Bin","Heliocentric Distance","Avg Cr (low_ssn_60)"])
      # for i in range(0,10):
      #     writer.writerow([bins[i], end_bin[i], avg_cr[i]])

# open a file called sd_bin.csv and add the list of average count rates as a column
df = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/sd_bin.csv")
df["Avg Cr (high_ssn_180)"] = avg_cr
df.to_csv('/Users/naomiweiss/SSL Files/spyder scripts/sd_bin.csv', index=False)
        
