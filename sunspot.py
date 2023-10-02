#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 19:29:26 2021

@author: naomiweiss
"""

import pandas as pd
import math
import csv
from datetime import datetime

sunspot = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/sunspot_data.csv")

years = sunspot['1818']
months = sunspot['1']
days = sunspot['2']
ss_numbers = sunspot['-1']

df = pd.read_csv("/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv")

mex_dates = df["Start Time"]
mex_years = []; mex_months = []; mex_days = []
ss_dates = []

for i in range(len(years)):
    str_d = str(str(years[i])+'-'+str(months[i])+'-'+str(days[i]))
    d = datetime.strptime((str_d),'%Y-%m-%d')
    ss_dates.append(d)
    
dictionary = dict(zip(ss_dates, ss_numbers))
# for d in dates:
#     year = int(d[0:4])
#     month = int(d[5:7])
#     day = int(d[8:10])
#     mex_years.append(year)
#     mex_months.append(month)
#     mex_days.append(day)


matched_sunspot = []; fixed_mex_dates = []
for i in mex_dates:
    start_time = i[0:10]
    start_time = datetime.strptime(start_time,'%Y-%m-%d')
    fixed_mex_dates.append(start_time)
    
for i in fixed_mex_dates:
    matched_sunspot.append(dictionary.get(i))
# for i in range(len(mex_years)):
#     for j in range(len(years)):
#         if (mex_years[i] == years[j]):
#             if(mex_months[i] == months[j]):
#                 if(mex_days[i] == days[j]):
#                     matched_sunspot.append(ss_numbers[j])
    

df["Sunspot Number"] = matched_sunspot
df.to_csv("/Users/naomiweiss/SSL Files/spyder scripts/mex_ima_2004-2006.csv", index=False)





