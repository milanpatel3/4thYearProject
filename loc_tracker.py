'''
Created on Jan 20, 2018

@author: keton
'''
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.Qt import pyqtSignal
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import *

class loc_tracker(QtCore.QObject):
    latitude = 0.0
    longitude = 0.0

    def __init__(self, user_int):
        super(loc_tracker, self).__init__()
        self.ui = user_int
    
    @QtCore.pyqtSlot(float, float, int)
    def addtoPath(self,lat,long, index):
        self.ui.addPath(lat, long, index)
    
    @QtCore.pyqtSlot(int)
    def remPath(self, index):
        self.ui.remPath(index)
    