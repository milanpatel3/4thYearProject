'''
Created on Mar 12, 2018

@author: Milan Patel
'''
import os

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


    