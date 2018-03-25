'''
Created on Oct 27, 2017

@author: Milan Patel
'''

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from os import path

def GetNormPicList(picDir):
    norm = []   
    #Get the list for normal images
    for root, dirs, files in os.walk(picDir):
        for file in files:
            norm.append(os.path.join(root, file))
            
    return norm

def GetThermPicList(picDir):
    therm = []
    for root,dirs, files in os.walk(picDir):
        for file in files:
            therm.append(os.path.join(root, file))
                
    return therm

def GetSensorDataList(dataDir):
    sensor = []
    for root,dirs, files in os.walk(dataDir):
        for file in files:
            sensor.append(os.path.join(root, file))
                
    return sensor

def GetLocList(locDir):
    locations = []
    for root,dirs, files in os.walk(locDir):
        for file in files:
            locations.append(os.path.join(root, file))
                
    return locations