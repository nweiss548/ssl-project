#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 09:53:53 2022

@author: naomiweiss
"""

import math as m
import pandas as pd
import spiceypy as spice


# rotates any vector about the z-axis by an angle theta, where
# clockwise is from x towards y, just like the azimuth angle in spc
# theta is in RADIANS!!
def rotate_z (theta, x, y, z):
  x1 = x*m.cos(theta) - y*m.sin(theta)
  y1 = y*m.cos(theta) + x*m.sin(theta)
  z1 = z
  
  return [x1, y1, z1]


# rotates any vector about the y-axis by an angle theta, where
# clockwise is from z towards x
# theta is in RADIANS!!
def rotate_y (theta, x, y, z):
  x1 = x*m.cos(theta) - z*m.sin(theta)
  y1 = y
  z1 = z*m.cos(theta) + x*m.sin(theta)
  
  return [x1, y1, z1]


# calculates solar zenith angle from sunstate coordinates (GSE at earth, MSO at Mars etc.)
def sza (x, y, z):
  return m.acos(x/m.sqrt(x*x + y*y + z*z))



# this procedure should calculate the magnetic zenith angle, i.e. how
# far behind the magnetic field shadow the spacecraft is.

# the function arguments are the three components of the magnetic
# field and the spacecraft position, in MSO coordinates, respectively.
def get_bza (bx, by, bz, scx, scy, scz):

    # calculate the theta and phi angles of the magnetic field
    b_mag = m.sqrt(bx*bx + by*by + bz*bz)
    b_theta = m.acos(bz/b_mag)
    b_phi = m.asin(by/m.sqrt(bx*bx + by*by))
    
    
    # now rotate the spacecraft position around the Z axis by the magnetic 
    # field phi angle, to get z-rotated spacecraft position vectors sx,
    # sy, sz
    sx, sy, sz = rotate_z(-b_phi, scx, scy, scz)
    
    #  now rotate these new position vectors around the  rotated y-axis
    #  theta, to get the spacecraft position vector in a new coordinate
    #  frame where, instead of the +x- axis being a line to the sun, instead
    #  it is the interplanetary magnetic field
    posx_B, posy_B, posz_B = rotate_y(-b_theta, sx, sy, sz)
    
    
    # in this coordinate frame, the magnetic zenith angle can be easily
    # calculated the same way we would normally calculate the solar zenith angle
    sza_b = sza(posx_B, posy_B, posz_B)

    # not needed, but just in case we ever want to calculate the
    # "magnetic local time"
    # phi = m.atan(posx_B/posy_B)
    # lt_b = (12.0 + phi*12/m.pi) % 24
 
    # return the magnetic zenith angle
    return sza_b
 


# get list of all mgs ephemeris files 
df = pd.read_csv("/Users/naomiweiss/SSL Files/mgs sep event files/mgs_info recent (without sep events).csv")

times = df['Start Time']

et_times = []
for i in times:
    et_times.append(spice.str2et(str(i)))

# set reference frame and target/observer
reference_frame = "MAVEN_MSO"
target = "MGS"
observer = "MARS"

# get position and longitude of spacecraft for the listed times
mgs_pos = []
for t in et_times:
    [pos, ltime] = spice.spkpos(target, t, reference_frame,'NONE', observer)
    mgs_pos.append(pos)

bza = []
b_init = 10000
for i in range(len(mgs_pos)):
    b = get_bza(m.cos(0), m.sin(0), 0, mgs_pos[i][0], mgs_pos[i][1], mgs_pos[i][2])
    b = m.degrees(b)
    bza.append(b)
    if b<b_init:
        b_init = b
        
for i in range(20):
    print(bza[i])
# df["BZA"] = bza
# df.to_csv('/Users/naomiweiss/SSL Files/mgs sep event files/mgs_info recent (without sep events).csv', index=False)


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    