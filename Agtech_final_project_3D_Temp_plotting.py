# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 15:18:37 2022

@author: zinge
"""

import urllib.request
from matplotlib import axes, axis
from matplotlib.collections import PolyCollection
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os.path
import matplotlib.dates as mdates
import datetime as dt
import matplotlib as mpl
from matplotlib import cm
from pandas.tseries.frequencies import to_offset
#from scipy.signal import savgol_filter

# define names of files
filename1 = "Station1.csv"
filename2 = "Station2.csv"
filename3 = "Station3.csv"

# define what to download
channels1 = "1777871"
channels2="1766721"
channels3="1777982"
fields = "1,2,3,4,5,6"
minutes = "1"

# download using Thingspeak's API 1
url = f"https://api.thingspeak.com/channels/{channels1}/fields/{fields}.csv?minutes={minutes}"
data = urllib.request.urlopen(url)
d = data.read()

# save data to csv
file = open(filename1, "w")
file.write(d.decode('UTF-8'))
file.close()

# download using Thingspeak's API 2
url = f"https://api.thingspeak.com/channels/{channels2}/fields/{fields}.csv?minutes={minutes}"
data = urllib.request.urlopen(url)
d = data.read()

# save data to csv
file = open(filename2, "w")
file.write(d.decode('UTF-8'))
file.close()

# download using Thingspeak's API 3
url = f"https://api.thingspeak.com/channels/{channels3}/fields/{fields}.csv?minutes={minutes}"
data = urllib.request.urlopen(url)
d = data.read()

# save data to csv
file = open(filename3, "w")
file.write(d.decode('UTF-8'))
file.close()

# opening files as data frames
station1 = pd.read_csv("Station1.csv")
station2 = pd.read_csv("Station2.csv")
station3 = pd.read_csv("Station3.csv")

# defining the file containing all average tempartures and sensor locations (the main file)
filename4 = "Final Sensor Locations & Measurments.csv"
df4 = pd.read_csv(filename4)

# calculating mean temp for each sensor
avg_box1_sht1 = station1['field1'].mean()
avg_box1_sht2 = station1['field2'].mean()
avg_box1_ds1_15 = station1['field3'].mean()
avg_box1_ds1_11 = station1['field4'].mean()
avg_box1_ds1_13 = station1['field5'].mean()
avg_box1_ds1_14 = station1['field6'].mean()
avg_box2_sht1 = station2['field1'].mean()
avg_box2_sht2 = station2['field2'].mean()
avg_box2_ds1_7 = station2['field3'].mean()
avg_box2_ds1_8 = station2['field4'].mean()
avg_box2_ds1_9 = station2['field5'].mean()
avg_box2_ds1_10 = station2['field6'].mean()
avg_box3_sht1 = station3['field1'].mean()
avg_box3_sht2 = station3['field2'].mean()
avg_box3_ds1_16 = station3['field3'].mean()
avg_box3_ds1_18 = station3['field4'].mean()
avg_box3_ds1_17 = station3['field5'].mean()
avg_box3_ds1_19 = station3['field6'].mean()

# creating a list of all the means
mean_list = [avg_box1_sht1, avg_box1_sht2, avg_box1_ds1_15, avg_box1_ds1_11, avg_box1_ds1_13,
             avg_box1_ds1_14, avg_box2_sht1, avg_box2_sht2, avg_box2_ds1_7, avg_box2_ds1_8,
             avg_box2_ds1_9, avg_box2_ds1_10, avg_box3_sht1, avg_box3_sht2, avg_box3_ds1_16,
             avg_box3_ds1_18, avg_box3_ds1_17, avg_box3_ds1_19]

# updating the main file
df4['temp_c'] = mean_list
# replacing negative temp reads with 'nan'
df4['temp_c']=df4['temp_c'].mask(df4['temp_c'].lt(0), np.nan)

# creating the 3d graph

""" #plotting the greenhouse
#walls (read as a matrix, every colums is a position vector for the polygon corner)
x_walls =  [0,0,0,  0],      [15,15,15,15],[15,0,0,15],  [15,0,0,15]
y_walls = [0,0,6.5,6.5]  , [0,6.5,6.5,0],[0,0,0,0],    [6.5,6.5,6.5,6.5]
z_walls =  [0,  2.1,2.1,0], [0,0,2.1,2.1],[0,0,2.1,2.1],[0,0,2.1,2.1]

surfaces = []

for i in range(len(x_walls)):
    surfaces.append( [list(zip(x_walls[i],y_walls[i],z_walls[i]))] )

for surface in surfaces:
    axes.add_collection3d(PolyCollection(surface,ec='b',fc=(0, 0, 0, 0)))

#roof
x_roof = [15,0,0,15],     [0,15,15,0],          [0,0,0],[15,15,15]
y_roof = [0,0,3.25, 3.25],[6.5,6.5,3.25,3.25],  [0,3.25,6.5],[0,3.25,6.5]
z_roof = [2.1,2.1,3,3],   [2.1,2.1,3,3],        [2.1,3,2.1],[2.1,3,2.1]

surfaces = []

for i in range(len(x_roof)):
    surfaces.append( [list(zip(x_roof[i],y_roof[i],z_roof[i]))] )

for surface in surfaces:
    axis.add_collection3d(PolyCollection(surface,ec='r',fc=(0., 0., 0., 0.)))
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(projection='3d') """

#sensors
x = df4.lengh_windows
y = df4.width_m
z = df4.hight_m
t = df4.temp_c

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_trisurf(x, y, z, cmap=cm.coolwarm, linewidth=0)

ax.set_xlabel('$length$')
ax.set_ylabel('$width$')
ax.set_zlabel('$hight$')
plt.legend(loc="upper left")

img = ax.scatter(x, y, z, c=t, cmap=plt.get_cmap("plasma"))
fig.colorbar(img)
plt.show()