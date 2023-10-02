#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 09:44:14 2021

@author: naomiweiss
"""

#Importing all necessary toolkits
import spiceypy as spice
import os
from datetime import datetime
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

def makePlanetPositionPlot(title, size=8, axisLimit=1.5e+04, planetSize=3390):

    #Make the figure
    fig = plt.figure(figsize=(size, size))

    #Make sub plot
    axis3d = fig.add_subplot(111, projection='3d')

    #Set axis limits
    axis3d.set_xlim([-axisLimit, axisLimit])
    axis3d.set_ylim([-axisLimit, axisLimit])
    axis3d.set_zlim([-axisLimit, axisLimit])

    #Set axis labels
    axis3d.set_xlabel('X (km)')
    axis3d.set_ylabel('Y (km)')
    axis3d.set_zlabel('Z (km)')

    #Create the sun
    axis3d.scatter([0.0], [0.0], [0.0], s=planetSize, c="orange")

    #Add a title
    plt.title(title, y=1.025)
    
    #Return the plt
    return axis3d, fig

def addPlanetToPlot(axis3D, planetPosition, size, color):
    return axis3D.scatter([planetPosition[0]], [planetPosition[1]], [planetPosition[2]], s=size, c=color)


#Define the kernels path
kernels_Path = "/Users/naomiweiss/SSL Files/mars project files/kernels"

#Label all kernel names
kernels_To_Load = ['naif0012.tls', 'de405.bsp', 'maven_v09.tf.txt',
                   'ORMM__040201000000_00060.BSP']

#Create the meta kernel
meta_Kernel = [os.path.join(kernels_Path, k) for k in kernels_To_Load]

#Furnsh the meta kernel
spice.furnsh(meta_Kernel)


#Data set start time
start_Time = datetime(2004, 12, 11)
start_Time_String = str(start_Time)

# end_Time = datetime(2003, 3, 9)
# end_Time_String = str(end_Time)

#Use SPICE's str2et function to convert our times string to ET time
start_TimeET = spice.str2et(start_Time_String)
# end_TimeET = spice.str2et(end_Time_String)


#Set bodies and reference frame
referenceFrame = "MAVEN_MSO"
target = "MGS"
observer = "MARS"


#Get MEX positions and light time between Mars and MEX
[MEXpos, ltime] = spice.spkpos(target, start_TimeET, referenceFrame,'NONE', observer)


#Make the plot
axis3D, fig = makePlanetPositionPlot('MGS position relative to Mars')
addPlanetToPlot(axis3D, MEXpos, 20, 'green')


times = [start_Time]
for i in range(1, 50):
    times.append(start_Time + relativedelta(hours=i))

#Convert to et
etTimes = [spice.str2et(str(x)) for x in times]

MEXPositions = spice.spkpos(target, etTimes, referenceFrame,'NONE', observer)[0]
print(MEXPositions)

#Add the data
for MEXpos in MEXPositions:
    addPlanetToPlot(axis3D, MEXpos, 20, 'green')


axis3D.view_init(0, 30)
plt.show()


#Clear all kernels
spice.kclear()
