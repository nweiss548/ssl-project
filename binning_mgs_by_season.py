#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 23:46:13 2023

@author: naomiweiss
"""
import pandas as pd
import csv
import matplotlib.pyplot as plt
import math
from scipy.stats import sem

df = pd.read_csv("/Users/naomiweiss/SSL Files/mgs sep event files/finding season and sun dist correlation for mgs/high_ssn split/high_ssn_60.csv")

cr = df['Sky Blockage Adjusted CR	']
ls = df["Season"]
sd = df["Heliocentric Distance"]

               
avg_cr = []
std_error = []
bins = ['0-36', '36-72', '72-108', '108-144', '144-180', '180-216', '216-252', '252-288', '288-324', '324-360']
end_bin = [36, 72, 108, 144, 180, 216, 252, 288, 324, 360]
for i in range(36, 396, 36):
    sum = 0
    num_vals = 0
    std_error_list = []
    for j in range(len(cr)):
        if ((i-36) < ls[j])  and ls[j]< i:
            if math.isnan(cr[j]) is False:
                sum += cr[j]
                num_vals+=1
                std_error_list.append(cr[j])
    print(num_vals)
    avg_cr.append(sum/num_vals)
    std_error.append(sem(std_error_list, nan_policy='omit'))

print(std_error)

# df = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/ls_bin.csv")
# df["Avg Cr (high_ssn_180)"] = avg_cr
# df.to_csv('/Users/naomiweiss/SSL Files/spyder scripts/ls_bin.csv', index=False)


# with open('ls_bin.csv', 'w', newline='') as file:
#      writer = csv.writer(file)
     
#      writer.writerow(["Season Bin","Season","Avg Cr (low_ssn_60)"])
#      for i in range(0,10):
#          writer.writerow([bins[i], end_bin[i], avg_cr[i]])
        

# plt.scatter(sd, cr, s=area, alpha=0.5)
# plt.show()