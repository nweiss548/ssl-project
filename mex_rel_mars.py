#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 18:32:53 2021

@author: naomiweiss
"""

import spiceypy as spice
import os
from datetime import datetime
import matplotlib.pyplot as plt
from dateutil.relativedelta import relativedelta

def makePlanetPositionPlot(title, size=8, axisLimit=1.5e+04, sunSize=3390):

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
    axis3d.scatter([0.0], [0.0], [0.0], s=sunSize, c="orange")

    #Add a title
    plt.title(title, y=1.025)
    
    #Return the plt
    return axis3d, fig

def addPlanetToPlot(axis3D, planetPosition, size, color):
    return axis3D.scatter([planetPosition[0]], [planetPosition[1]], [planetPosition[2]], s=size, c=color)


#Define the kernels path
kernelsPath = "/Users/naomiweiss/SSL Files/mars project files/kernels/"

#Define the path to the leap second kernel
leapSecondsKernelPath = os.path.join(kernelsPath, "naif0012.tls")

#Define the path to the solar system ephemeris kernel
solarSystemEphermisKernelPath = os.path.join(kernelsPath, "de405.bsp")

#Define the path to MEX ephemeris kernel
MEXEphermisKernelPath = os.path.join(kernelsPath, "ORMM__040201000000_00060.BSP")

#Define the path to the MEX frame kernel
MEXFrameKernelPath = os.path.join(kernelsPath, "maven_v09.tf.txt")

#Load the kernels
spice.furnsh(leapSecondsKernelPath)
spice.furnsh(solarSystemEphermisKernelPath)
spice.furnsh(MEXEphermisKernelPath)
spice.furnsh(MEXFrameKernelPath)

#Data set start time
startTime = datetime(2004, 2, 2)
startTimeString = str(startTime)

#Use SPICE's str2et function to convert our time string to ET time
startTimeET = spice.str2et(startTimeString)


# Use MSO (.tf) frame kernel 
referenceFrame = "MAVEN_MSO"
target = "MEX"
observer = "MARS"

#Get MEX positions and light time between Mars and MEX
[MEXpos, ltime] = spice.spkpos(target, startTimeET, referenceFrame,'NONE', observer)


#Convert to et
#etTimes = [spice.str2et(str(x)) for x in times]


#Make the plot
axis3D, fig = makePlanetPositionPlot('MEX position relative to Mars')
addPlanetToPlot(axis3D, MEXpos, 20, 'green')


times = [startTime]
for i in range(1, 25):
    times.append(startTime + relativedelta(hours=i))

#Convert to et
etTimes = [spice.str2et(str(x)) for x in times]

MEXPositions = spice.spkpos(target, etTimes, referenceFrame,'NONE', observer)[0]
print(MEXPositions)

#Add the data
for MEXpos in MEXPositions:
    addPlanetToPlot(axis3D, MEXpos, 20, 'green')


axis3D.view_init(0, 30)
plt.show()


spice.kclear()




