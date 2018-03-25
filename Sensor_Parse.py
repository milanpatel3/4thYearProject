'''
Created on Mar 11, 2018

@author: Milan Patel
'''

import os
from collections import Counter

def most_common(lst):
    data = Counter(lst)
    return max(lst, key=data.get)

def Parse_Sensor(datapath):
    sensor_path = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Sensor_Data\\sensor(0).txt"
    f = open(datapath, 'r')
    lines = f.readlines()
    f.close()

    light = []
    temp = []
    pressure = []
    altitude = []
    humidity = []

    for i in lines:
        if "Light" in i:
            light.append(i[8:])
        if "Temperature" in i:
            temp.append(i[14:])
        if "Pressure" in i:
            pressure.append(i[11:])
        if "Altitude" in i:
            altitude.append(i[11:])
        if "Humidity" in i:
            humidity.append(i[11:])

    l = most_common(light)
    t = most_common(temp)
    p = most_common(pressure)
    a = most_common(altitude)
    h = most_common(humidity)
    data = [t,h,l,p,a]
    return(data)

def Parse_Location(locpath):
    f = open(locpath, 'r')
    lines = f.readlines()
    f.close()
    lat = 0
    long = 0
    for i in lines:
        if "lat" in i:
            lat = i[4:]
        if "long" in i:
            long = i[5:]

    data = [lat, long]
    return(data)

    