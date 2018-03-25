import os
import GetPicList
from GetPicList import GetNormPicList, GetThermPicList, GetSensorDataList,\
    GetLocList
import WatchNewPic
import loc_tracker
import threading
import XBEE_COMS
import Sensor_Parse
import loc_Parse
import Send_Loc_List
import UAV_Location_Tracking
#import map
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import QUrl
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.Qt import pyqtSignal
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import *
from _overlapped import NULL
import time
from _datetime import timedelta, datetime


class Ui_TabWidget(object):
    

    '''set the index
        Because there will be multiple images in the stream we will use an index to identify them
        On initialization we will always show image number 0  
        We also get a list of all images currently in the folder and the index max of the list
        The list contains the full path of the image
        This will allow any picture to be shown regardless of extension type
        We will use this list in all picture updates and changes  
        This index will also be used to identify the sensor data file being referenced
        And the index will correspond to the location waypoints
    '''
    
    normpicDir = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Normal_Image\\"
    thermpicDir = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Thermal_Image\\"
    sensorDir = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Sensor_Data\\"
    locDir = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Location\\"

    current_img = "norm"
    imgindex = 0
    norm = GetNormPicList(normpicDir)
    imgindexmax = len(norm) - 1
    therm = GetThermPicList(thermpicDir)
    sensor_data = GetSensorDataList(sensorDir)
    locations = GetLocList(locDir)
    
    
    
    def setupUi(self, TabWidget):
        #Create the Tab Widget Object
        
        #These are all the variables and arrays which will be used to link the GUI to
        #the Google Maps API. Arrays to store waypoint and UAV locations and variables to update text labels
        self.waypoints = []
        self.lat_level = -1
        self.long_level = -1
        self.path_complete = 0
        self.waypoint_reached = 0
        self.UAVLocations = []
        self.base_lat = str(45.3985574)
        self.base_long = str(-75.7124743)
        self.waypoints.append([self.base_lat, self.base_long])
        self.UAVLocations.append([self.base_lat, self.base_long])
        self.currWaypoint = "B"
        self.loc_list_max = 0
        self.local_map = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\test_map.html"
        
        
        #All the created objects will be on the first tab. This is tab index 0. On GUI displayed as Tab 1
        TabWidget.setObjectName("TabWidget")
        TabWidget.resize(1641, 928)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        
        '''
            Create Labels to show the output of the sensor data
        '''
        #Add the label which will show the Humidity sensor output
        self.horizontalLayout_37 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.HumRead = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.HumRead.setFont(font)
        self.HumRead.setAlignment(QtCore.Qt.AlignCenter)
        self.HumRead.setObjectName("HumRead")
        self.horizontalLayout_37.addWidget(self.HumRead)
        self.gridLayout.addLayout(self.horizontalLayout_37, 6, 10, 1, 2)        
        
        #Add the label which will show the Magnetometer sensor output
        self.horizontalLayout_34 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_34.setObjectName("horizontalLayout_34")
        self.MagnetRead = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.MagnetRead.setFont(font)
        self.MagnetRead.setAlignment(QtCore.Qt.AlignCenter)
        self.MagnetRead.setObjectName("MagnetRead")
        self.horizontalLayout_34.addWidget(self.MagnetRead)
        self.gridLayout.addLayout(self.horizontalLayout_34, 12, 10, 1, 2)
        
        #Add the label which will show the Light sensor output
        self.horizontalLayout_36 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.LightRead = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.LightRead.setFont(font)
        self.LightRead.setAlignment(QtCore.Qt.AlignCenter)
        self.LightRead.setObjectName("LightRead")
        self.horizontalLayout_36.addWidget(self.LightRead)
        self.gridLayout.addLayout(self.horizontalLayout_36, 8, 10, 1, 2)
        
        #This is the label which will show the output of the altitude sensor data
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.AltRead = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.AltRead.setFont(font)
        self.AltRead.setAlignment(QtCore.Qt.AlignCenter)
        self.AltRead.setObjectName("AltRead")
        self.horizontalLayout_12.addWidget(self.AltRead)
        self.gridLayout.addLayout(self.horizontalLayout_12, 16, 10, 1, 2)
        
        #This label will show the output of the acceleration sensor
        self.horizontalLayout_35 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.AccelRead = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.AccelRead.setFont(font)
        self.AccelRead.setAlignment(QtCore.Qt.AlignCenter)
        self.AccelRead.setObjectName("AccelRead")
        self.horizontalLayout_35.addWidget(self.AccelRead)
        self.gridLayout.addLayout(self.horizontalLayout_35, 10, 10, 1, 2)
        
        #This is the label to show the output of the Barometric Pressure Sensor
        self.horizontalLayout_33 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.PressRead = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.PressRead.setFont(font)
        self.PressRead.setAlignment(QtCore.Qt.AlignCenter)
        self.PressRead.setObjectName("PressRead")
        self.horizontalLayout_33.addWidget(self.PressRead)
        self.gridLayout.addLayout(self.horizontalLayout_33, 14, 10, 1, 2)
        
        #This label will show the output of the temperature sensor
        self.horizontalLayout_38 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_38.setObjectName("horizontalLayout_38")
        self.TempRead = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.TempRead.setFont(font)
        self.TempRead.setAlignment(QtCore.Qt.AlignCenter)
        self.TempRead.setObjectName("TempRead")
        self.horizontalLayout_38.addWidget(self.TempRead)
        self.gridLayout.addLayout(self.horizontalLayout_38, 4, 10, 1, 2)
        
        
        '''
            Create a set of labels and layouts
            the layouts will be used in spacing and formatting of the GUI
            the labels will inidicate the location of output data (i.e. temperature, and battery level)
        '''
        
        #Create a Line to seperate labels for easier visibility
        #Also define horizontal layouts to provide spacing needed
        self.horizontalLayout_41 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_41.setSpacing(1)
        self.horizontalLayout_41.setObjectName("horizontalLayout_41")
        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_41.addWidget(self.line_2)
        self.gridLayout.addLayout(self.horizontalLayout_41, 5, 8, 1, 4)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.gridLayout.addLayout(self.horizontalLayout_16, 17, 1, 1, 1)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.gridLayout.addLayout(self.horizontalLayout_13, 17, 3, 1, 1)
        
        #Create layouts to provide spacing in the GUI for easier visbility
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.gridLayout.addLayout(self.horizontalLayout_17, 17, 5, 1, 1)
        
        #Add labels to indicate to the user what the progress bar and sensor data output is for
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 8, 1, 2)
        self.horizontalLayout_29 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.label_7 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_29.addWidget(self.label_7)
        self.gridLayout.addLayout(self.horizontalLayout_29, 10, 8, 1, 2)
        self.horizontalLayout_28 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_9 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_28.addWidget(self.label_9)
        self.gridLayout.addLayout(self.horizontalLayout_28, 14, 8, 1, 2)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_8 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_11.addWidget(self.label_8)
        self.gridLayout.addLayout(self.horizontalLayout_11, 12, 8, 1, 2)
        self.horizontalLayout_30 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_6 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_30.addWidget(self.label_6)
        self.gridLayout.addLayout(self.horizontalLayout_30, 8, 8, 1, 2)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_10 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_8.addWidget(self.label_10)
        self.gridLayout.addLayout(self.horizontalLayout_8, 16, 8, 1, 2)
        
        
        #More labels created to indentify what where the sensor output will be
        self.horizontalLayout_31 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.label_5 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_31.addWidget(self.label_5)
        self.gridLayout.addLayout(self.horizontalLayout_31, 6, 8, 1, 2)
        self.horizontalLayout_32 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.label_4 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_32.addWidget(self.label_4)
        self.gridLayout.addLayout(self.horizontalLayout_32, 4, 8, 1, 2)
        self.horizontalLayout_39 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_39.setSpacing(1)
        self.horizontalLayout_39.setObjectName("horizontalLayout_39")
        self.line = QtWidgets.QFrame(self.tab)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_39.addWidget(self.line)
        self.gridLayout.addLayout(self.horizontalLayout_39, 3, 8, 1, 4)
        self.horizontalLayout_46 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_46.setObjectName("horizontalLayout_46")
        self.line_7 = QtWidgets.QFrame(self.tab)
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.horizontalLayout_46.addWidget(self.line_7)
        self.gridLayout.addLayout(self.horizontalLayout_46, 13, 8, 1, 4)
        self.horizontalLayout_44 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_44.setObjectName("horizontalLayout_44")
        self.line_5 = QtWidgets.QFrame(self.tab)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_44.addWidget(self.line_5)
        self.gridLayout.addLayout(self.horizontalLayout_44, 9, 8, 1, 4)
        self.horizontalLayout_43 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_43.setObjectName("horizontalLayout_43")
        self.line_4 = QtWidgets.QFrame(self.tab)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_43.addWidget(self.line_4)
        self.gridLayout.addLayout(self.horizontalLayout_43, 7, 8, 1, 4)
        self.horizontalLayout_45 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_45.setObjectName("horizontalLayout_45")
        self.line_6 = QtWidgets.QFrame(self.tab)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.horizontalLayout_45.addWidget(self.line_6)
        self.gridLayout.addLayout(self.horizontalLayout_45, 11, 8, 1, 4)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.gridLayout.addLayout(self.horizontalLayout_10, 17, 10, 1, 1)
        
        #Add labels for clarity in GUI
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_18.addWidget(self.label)
        self.gridLayout.addLayout(self.horizontalLayout_18, 0, 8, 1, 4)
        
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.Rec_Status = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Rec_Status.setFont(font)
        self.Rec_Status.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.Rec_Status.setObjectName("Rec_Status")
        self.horizontalLayout_9.addWidget(self.Rec_Status)
        self.horizontalLayout_18.addLayout(self.horizontalLayout_9)
        
        #More Labels to indicate the sensor output location
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 10, 1, 2)
        self.horizontalLayout_47 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_47.setObjectName("horizontalLayout_47")
        self.line_8 = QtWidgets.QFrame(self.tab)
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.horizontalLayout_47.addWidget(self.line_8)
        self.gridLayout.addLayout(self.horizontalLayout_47, 15, 8, 1, 4)
      
        '''
            Indicate the Battery Level of the Drone in a Progress Bar
        '''
        
        #Add a progress bar to indicate the battery level of the drone
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.BatteryLevel = QtWidgets.QProgressBar(self.tab)
        self.BatteryLevel.setMinimumSize(QtCore.QSize(0, 25))
        self.BatteryLevel.setMaximumSize(QtCore.QSize(900, 25))
        self.BatteryLevel.setProperty("value", 24)
        self.BatteryLevel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.BatteryLevel.setObjectName("BatteryLevel")
        self.verticalLayout.addWidget(self.BatteryLevel)
        self.gridLayout.addLayout(self.verticalLayout, 1, 8, 1, 4)
        
        '''
            Create the Buttons for the Drone Commands to Return Home and Hover in Place
        '''
        
        #Create the Return Home Button, which will send the command to tell the drone to return to main base
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.HomeButton = QtWidgets.QPushButton(self.tab)
        self.HomeButton.setMaximumSize(QtCore.QSize(150, 50))
        self.HomeButton.setObjectName("HomeButton")
        self.horizontalLayout.addWidget(self.HomeButton)
        self.gridLayout.addLayout(self.horizontalLayout, 17, 11, 1, 1)
        
        #Create the button that will tell the drone to Hover in Place
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.HoverButton = QtWidgets.QPushButton(self.tab)
        self.HoverButton.setMaximumSize(QtCore.QSize(150, 50))
        self.HoverButton.setObjectName("HoverButton")
        self.horizontalLayout_7.addWidget(self.HoverButton)
        self.gridLayout.addLayout(self.horizontalLayout_7, 17, 8, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        
        '''
            Create the Image Layout and the Buttons to change the images (Normal, Thermal, Previous, Next)
        '''
        
        #Create the button to show the Normal Image capture from the GoPro camera
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.NormImg = QtWidgets.QPushButton(self.tab)
        self.NormImg.setMaximumSize(QtCore.QSize(150, 50))
        self.NormImg.setObjectName("NormImg")
        self.horizontalLayout_15.addWidget(self.NormImg)
        self.gridLayout.addLayout(self.horizontalLayout_15, 17, 4, 1, 1)
        self.NormImg.clicked.connect(self.ShowNormImg)
        
        #Create the button which will show the thermal image captures
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.ThermImg = QtWidgets.QPushButton(self.tab)
        self.ThermImg.setMaximumSize(QtCore.QSize(150, 50))
        self.ThermImg.setObjectName("ThermImg")
        self.horizontalLayout_5.addWidget(self.ThermImg)
        self.gridLayout.addLayout(self.horizontalLayout_5, 17, 2, 1, 1)
        self.ThermImg.clicked.connect(self.ShowThermImg)
        
        #Create the button to change to the next image
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.NextPic = QtWidgets.QPushButton(self.tab)
        self.NextPic.setMaximumSize(QtCore.QSize(150, 50))
        self.NextPic.setObjectName("NextPic")
        self.horizontalLayout_4.addWidget(self.NextPic)
        self.gridLayout.addLayout(self.horizontalLayout_4, 17, 6, 1, 1)
        self.NextPic.clicked.connect(self.ShowNextImg)
        
        #Create the button to show the Previous image
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.PrevPic = QtWidgets.QPushButton(self.tab)
        self.PrevPic.setMaximumSize(QtCore.QSize(150, 50))
        self.PrevPic.setObjectName("PrevPic")
        self.horizontalLayout_6.addWidget(self.PrevPic)
        self.gridLayout.addLayout(self.horizontalLayout_6, 17, 0, 1, 1)
        self.PrevPic.clicked.connect(self.ShowPrevImg)
        
        #This is where the image will be shown.
        #It is a label with the PixMap setting, which we will adjust as required
        self.image = QtWidgets.QLabel(self.tab)
        self.image.setMaximumSize(QtCore.QSize(900, 850))
        self.image.setText("")
        self.image.setScaledContents(True)
        self.image.setObjectName("image")
        self.image.setPixmap(QPixmap(self.norm[0]))
        self.gridLayout.addWidget(self.image, 0, 0, 17, 8)
        
        '''    
            Add the second tab to the window
            This is where we will show the map
            This is tab index 1. But labeled Tab 2 on the GUI
        '''
        
        TabWidget.addTab(self.tab, "")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab1)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout_4.setHorizontalSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        
        '''
            Add labels to update location information for the current location and the target location
        '''
        
        self.horizontalLayout_70 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_70.setObjectName("horizontalLayout_70")
        self.alt_label = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.alt_label.setFont(font)
        self.alt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.alt_label.setObjectName("alt_label")
        self.alt_label.setText("0")
        self.horizontalLayout_70.addWidget(self.alt_label)
        self.gridLayout_4.addLayout(self.horizontalLayout_70, 3, 2, 1, 1)
        
        self.horizontalLayout_79 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_79.setObjectName("horizontalLayout_79")
        self.long_label = QtWidgets.QLabel(self.tab1)
        self.long_label.setMinimumSize(QtCore.QSize(150, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.long_label.setFont(font)
        self.long_label.setAlignment(QtCore.Qt.AlignCenter)
        self.long_label.setObjectName("long_label")
        self.long_label.setText(str(self.base_long))
        self.horizontalLayout_79.addWidget(self.long_label)
        self.gridLayout_4.addLayout(self.horizontalLayout_79, 2, 2, 1, 1)
        
        self.horizontalLayout_80 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_80.setObjectName("horizontalLayout_80")
        self.latitude_label = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.latitude_label.setFont(font)
        self.latitude_label.setAlignment(QtCore.Qt.AlignCenter)
        self.latitude_label.setObjectName("latitude_label")
        self.latitude_label.setText(str(self.base_lat))
        self.horizontalLayout_80.addWidget(self.latitude_label)
        self.gridLayout_4.addLayout(self.horizontalLayout_80, 1, 2, 1, 1)
        
        self.horizontalLayout_82 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_82.setObjectName("horizontalLayout_82")
        self.next_long_label = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.next_long_label.setFont(font)
        self.next_long_label.setAlignment(QtCore.Qt.AlignCenter)
        self.next_long_label.setObjectName("next_long_label")
        self.horizontalLayout_82.addWidget(self.next_long_label)
        self.gridLayout_4.addLayout(self.horizontalLayout_82, 2, 3, 1, 1)
        
        
        self.horizontalLayout_81 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_81.setObjectName("horizontalLayout_81")
        self.next_lat_label = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.next_lat_label.setFont(font)
        self.next_lat_label.setAlignment(QtCore.Qt.AlignCenter)
        self.next_lat_label.setObjectName("next_lat_label")
        self.horizontalLayout_81.addWidget(self.next_lat_label)
        self.gridLayout_4.addLayout(self.horizontalLayout_81, 1, 3, 1, 1)
        
        self.horizontalLayout_83 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_83.setObjectName("horizontalLayout_83")
        self.next_alt_label = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.next_alt_label.setFont(font)
        self.next_alt_label.setAlignment(QtCore.Qt.AlignCenter)
        self.next_alt_label.setObjectName("next_alt_label")
        self.horizontalLayout_83.addWidget(self.next_alt_label)
        self.gridLayout_4.addLayout(self.horizontalLayout_83, 3, 3, 1, 1)
        
        '''
            Add buttons for functionality
            Buttons are:
                Emergency Landing
                Return Home
                Hover
                Send Command
                
        '''
        
        self.horizontalLayout_73 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_73.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_73.setObjectName("horizontalLayout_73")
        self.emerg_land_button = QtWidgets.QPushButton(self.tab1)
        self.emerg_land_button.setMinimumSize(QtCore.QSize(90, 50))
        self.emerg_land_button.setMaximumSize(QtCore.QSize(150, 50))
        self.emerg_land_button.setObjectName("emerg_land_button")
        self.horizontalLayout_73.addWidget(self.emerg_land_button)
        self.gridLayout_4.addLayout(self.horizontalLayout_73, 6, 3, 1, 1)
        
        
        self.horizontalLayout_71 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_71.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_71.setObjectName("horizontalLayout_71")
        self.return_base_button = QtWidgets.QPushButton(self.tab1)
        self.return_base_button.setMinimumSize(QtCore.QSize(90, 50))
        self.return_base_button.setMaximumSize(QtCore.QSize(150, 50))
        self.return_base_button.setObjectName("return_base_button")
        self.horizontalLayout_71.addWidget(self.return_base_button)
        self.gridLayout_4.addLayout(self.horizontalLayout_71, 6, 1, 1, 1)
        
        
        self.horizontalLayout_74 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_74.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_74.setObjectName("horizontalLayout_74")
        self.hover_button = QtWidgets.QPushButton(self.tab1)
        self.hover_button.setMinimumSize(QtCore.QSize(90, 50))
        self.hover_button.setMaximumSize(QtCore.QSize(150, 50))
        self.hover_button.setObjectName("hover_button")
        self.horizontalLayout_74.addWidget(self.hover_button)
        self.gridLayout_4.addLayout(self.horizontalLayout_74, 6, 2, 1, 1)
        
        
        
        
        self.horizontalLayout_76 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_76.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_76.setObjectName("horizontalLayout_76")
        self.send_command_button = QtWidgets.QPushButton(self.tab1)
        self.send_command_button.setMinimumSize(QtCore.QSize(90, 50))
        self.send_command_button.setMaximumSize(QtCore.QSize(150, 50))
        self.send_command_button.setObjectName("send_command_button")
        self.horizontalLayout_76.addWidget(self.send_command_button)
        self.gridLayout_4.addLayout(self.horizontalLayout_76, 5, 2, 1, 1)
        self.send_command_button.clicked.connect(self.Send_Path_List)
        
        
        '''
            Create Labels for visual display on interface
            These labels are static values and do not need specific identifiers
        '''                 
        self.horizontalLayout_84 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_84.setObjectName("horizontalLayout_84")
        self.label_23 = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_23.setWordWrap(True)
        self.label_23.setObjectName("label_23")
        self.horizontalLayout_84.addWidget(self.label_23)
        self.gridLayout_4.addLayout(self.horizontalLayout_84, 0, 2, 1, 1)
        
        
        self.horizontalLayout_85 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_85.setObjectName("horizontalLayout_85")
        self.label_22 = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_22.setObjectName("label_22")
        self.horizontalLayout_85.addWidget(self.label_22)
        self.gridLayout_4.addLayout(self.horizontalLayout_85, 0, 1, 1, 1)
        
        
        self.horizontalLayout_86 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_86.setObjectName("horizontalLayout_86")
        self.label_25 = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_25.setFont(font)
        self.label_25.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_86.addWidget(self.label_25)
        self.gridLayout_4.addLayout(self.horizontalLayout_86, 1, 1, 1, 1)
        
        
        self.horizontalLayout_87 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_87.setObjectName("horizontalLayout_87")
        self.label_26 = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_26.setFont(font)
        self.label_26.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_87.addWidget(self.label_26)
        self.gridLayout_4.addLayout(self.horizontalLayout_87, 2, 1, 1, 1)
        
        
        self.horizontalLayout_88 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_88.setObjectName("horizontalLayout_88")
        self.label_27 = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_88.addWidget(self.label_27)
        self.gridLayout_4.addLayout(self.horizontalLayout_88, 3, 1, 1, 1)
        
        
        self.horizontalLayout_89 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_89.setObjectName("horizontalLayout_89")
        self.label_24 = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_24.setFont(font)
        self.label_24.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_89.addWidget(self.label_24)
        self.gridLayout_4.addLayout(self.horizontalLayout_89, 0, 3, 1, 1)
        
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_12 = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_14.addWidget(self.label_12)
        self.gridLayout_4.addLayout(self.horizontalLayout_14, 4, 1, 1, 1)
        
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.Curr_WP_Number = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Curr_WP_Number.setFont(font)
        self.Curr_WP_Number.setAlignment(QtCore.Qt.AlignCenter)
        self.Curr_WP_Number.setObjectName("Curr_WP_Number")
        self.Curr_WP_Number.setText(str(self.currWaypoint))
        self.horizontalLayout_19.addWidget(self.Curr_WP_Number)
        self.gridLayout_4.addLayout(self.horizontalLayout_19, 4, 2, 1, 1)
        
        
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.Next_WP_Number = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Next_WP_Number.setFont(font)
        self.Next_WP_Number.setAlignment(QtCore.Qt.AlignCenter)
        self.Next_WP_Number.setObjectName("Next_WP_Number")
        self.Next_WP_Number.setText("1")
        self.horizontalLayout_20.addWidget(self.Next_WP_Number)
        self.gridLayout_4.addLayout(self.horizontalLayout_20, 4, 3, 1, 1)
        
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_11 = QtWidgets.QLabel(self.tab1)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_9.addWidget(self.label_11)
        self.gridLayout_4.addLayout(self.horizontalLayout_9, 0, 4, 1, 1)
        
        '''
            Create a list which will show all locations
                Both past locations and future waypoints
                The future waypoints can be editied by adding/removing
                Past waypoint data will be locked into place
        '''
        
        self.horizontalLayout_78 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_78.setObjectName("horizontalLayout_78")
        self.location_list = QtWidgets.QListWidget(self.tab1)
        self.location_list.setMinimumSize(QtCore.QSize(300, 500))
        self.location_list.setMaximumSize(QtCore.QSize(300, 500))
        self.location_list.setObjectName("location_list")
        self.horizontalLayout_78.addWidget(self.location_list)
        self.firstItem = str(self.loc_list_max) + '    ||    ' + str([self.base_lat,self.base_long])
        self.location_list.addItem(self.firstItem)
        self.gridLayout_4.addLayout(self.horizontalLayout_78, 1, 4, 6, 1)
        
        
        
        '''
            Create map display
        ''' 
        
        
        self.horizontalLayout_69 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_69.setObjectName("horizontalLayout_69")
        self.label_21 = QtWidgets.QLabel(self.tab1)
        self.map = QWebEngineView(self.tab1)
        self.map.setObjectName("map_display")
        self.map.setMinimumSize(500, 500)
        self.map.setMaximumSize(720, 1000)
        self.map.load(QtCore.QUrl.fromLocalFile(self.local_map))
        
        self.tracker = QWebChannel()
        self.map_updates = loc_tracker.loc_tracker(self)
        self.tracker.registerObject('loc_tracker', self.map_updates)
        self.map.page().setWebChannel(self.tracker)

        
        self.horizontalLayout_69.addWidget(self.map)
        
        '''
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_69.addWidget(self.label_21)
        spacerItem = QtWidgets.QSpacerItem(700, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_69.addItem(spacerItem)
        '''
        self.gridLayout_4.addLayout(self.horizontalLayout_69, 0, 0, 7, 1)
        
        
        
        
        
        
        
        self.gridLayout_5.addLayout(self.gridLayout_4, 0, 0, 1, 1)
        TabWidget.addTab(self.tab1, "")
        

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget"))
        self.NormImg.setText(_translate("TabWidget", "Normal Image"))
        self.label_2.setText(_translate("TabWidget", "Sensor"))
        self.label_7.setText(_translate("TabWidget", "Acceleration"))
        self.label_9.setText(_translate("TabWidget", "Pressure"))
        self.label_8.setText(_translate("TabWidget", "Magnetometer"))
        self.label_6.setText(_translate("TabWidget", "Light"))
        self.label_10.setText(_translate("TabWidget", "Altitude"))
        self.label_5.setText(_translate("TabWidget", "Humidity"))
        self.label_4.setText(_translate("TabWidget", "Temperature"))
        self.HomeButton.setText(_translate("TabWidget", "Return Home"))
        self.NextPic.setText(_translate("TabWidget", "Next Picture"))
        self.ThermImg.setText(_translate("TabWidget", "Thermal Image"))
        self.PrevPic.setText(_translate("TabWidget", "Previous Picture"))
        self.label.setText(_translate("TabWidget", "Battery Level"))
        self.label_3.setText(_translate("TabWidget", "Measurement"))
        self.HoverButton.setText(_translate("TabWidget", "Hover"))
        self.Rec_Status.setText(_translate("TabWidget", "Not Recieving"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "Tab 1"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "Tab 1"))
        self.alt_label.setText(_translate("TabWidget", "25 m"))
        #self.label_21.setText(_translate("TabWidget", "TextLabel"))
        self.hover_button.setText(_translate("TabWidget", "Hover"))
        self.emerg_land_button.setText(_translate("TabWidget", "Emergency Land"))
        self.send_command_button.setText(_translate("TabWidget", "Send Command"))
        self.label_23.setText(_translate("TabWidget", "<html><head/><body><p>Current</p><p>Reading</p></body></html>"))
        self.label_22.setText(_translate("TabWidget", "Direction"))
        self.label_25.setText(_translate("TabWidget", "Latitude"))
        self.label_26.setText(_translate("TabWidget", "Longitude"))
        self.label_27.setText(_translate("TabWidget", "Altitude"))
        self.label_24.setText(_translate("TabWidget", "<html><head/><body><p>Next</p><p>Location</p></body></html>"))
        self.return_base_button.setText(_translate("TabWidget", "Return Home"))
        self.label_12.setText(_translate("TabWidget", "<html><head/><body><p>Waypoint</p><p>Tracker</p></body></html>"))
        self.label_11.setText(_translate("TabWidget", "<html><head/><body><p>UAV Path List</p><p>Location || [Latitude, Longitude]</p></body></html>"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab1), _translate("TabWidget", "Tab 2"))
        
        
           
    '''
        Define the button click actions for the image display
    '''
    '''
        def ShowPrevImg(self)
        This function shows the previous image        
        Paramters - none
        
        Functionality - This will show the previous image in the folder based on the image index.
                        If at the minimum index, we wrap around to the highest index and scroll through again.
                        This function will check the current state of the picture if it is showing a normal image or thermal image.
                        At the end it will update the image label with the Pixmap pointing to the new picture
                        
        Output - none
                    This function updates the image display
    '''    
    def ShowPrevImg(self):
        if (Ui_TabWidget.imgindex != 0):
            Ui_TabWidget.imgindex -= 1
        elif (Ui_TabWidget.imgindex == 0):
            Ui_TabWidget.imgindex = Ui_TabWidget.imgindexmax
        
        data = Sensor_Parse.Parse_Sensor(self.sensor_data[Ui_TabWidget.imgindex])    
        location = loc_Parse.Parse_Location(self.locations[Ui_TabWidget.imgindex])

        
        if Ui_TabWidget.current_img == "norm":                
            self.image.setPixmap(QtGui.QPixmap(Ui_TabWidget.norm[Ui_TabWidget.imgindex]))
        
        elif Ui_TabWidget.current_img == "therm":
            self.image.setPixmap(QtGui.QPixmap(Ui_TabWidget.therm[Ui_TabWidget.imgindex]))
            
        Ui_TabWidget.Update_Sensor_Display(self, data)
        Ui_TabWidget.Update_Loc_Display(self, location)

            
            
    '''
        def ShowNextImg(self)
        This function shows the next image        
        Paramters - none
        
        Functionality - This will show the next image in the folder based on the image index.
                        If at the maximum index, we wrap around to the lowest index and scroll through again.
                        This function will check the current state of the picture if it is showing a normal image or thermal image.
                        At the end it will update the image label with the Pixmap pointing to the new picture
                        
        Output - none
                    This function updates the image display
    '''    
    def ShowNextImg(self):
        if (Ui_TabWidget.imgindex == Ui_TabWidget.imgindexmax):
            Ui_TabWidget.imgindex = 0
        else:
            Ui_TabWidget.imgindex += 1
            
        data = Sensor_Parse.Parse_Sensor(self.sensor_data[Ui_TabWidget.imgindex])    
        location = loc_Parse.Parse_Location(self.locations[Ui_TabWidget.imgindex])
            
        if Ui_TabWidget.current_img == "norm":
            self.image.setPixmap(QtGui.QPixmap(Ui_TabWidget.norm[Ui_TabWidget.imgindex]))
        
        elif Ui_TabWidget.current_img == "therm":
            self.image.setPixmap(QtGui.QPixmap(Ui_TabWidget.therm[Ui_TabWidget.imgindex]))
        
        Ui_TabWidget.Update_Sensor_Display(self, data)
        Ui_TabWidget.Update_Loc_Display(self, location)

    '''
        def ShowThermImg(self)
        This function shows the Thermal image        
        Paramters - none
        
        Functionality - This will show the thermal image in the folder, at the reset index of 0
                        The change only occurs if the image currently being shown is a normal image.
                        At the end it will update the image label with the Pixmap pointing to the new picture
                        
        Output - none
                    This function updates the image display
    '''
    def ShowThermImg(self):
        if Ui_TabWidget.current_img == "norm":
            Ui_TabWidget.current_img = "therm"
            #Ui_TabWidget.imgindex = 0
            self.image.setPixmap(QtGui.QPixmap(Ui_TabWidget.therm[Ui_TabWidget.imgindex]))
    
    '''
        def ShowNormImg(self)
        This function shows the Normal image        
        Paramters - none
        
        Functionality - This will show the normal image in the folder, at the reset index of 0
                        The change only occurs if the image currently being shown is a thermal image.
                        At the end it will update the image label with the Pixmap pointing to the new picture
                        
        Output - none
                    This function updates the image display
    '''    
    def ShowNormImg(self):

        if Ui_TabWidget.current_img == "therm":
            Ui_TabWidget.current_img = "norm"
            #Ui_TabWidget.imgindex = 0
            self.image.setPixmap(QtGui.QPixmap(Ui_TabWidget.norm[Ui_TabWidget.imgindex]))

    '''
        def UpdateImageList(self, adddir, tag)
        This function uses the WatchNewPic script to monitor the folders for the images.
        If a new image is seen in the folder, it is added to the corresponding list of images (normal or thermal)        
        Paramters - adddir - This is the full path of the image added to the folder, which is passed from the WatchNewPic script
                    tag - this variable indicates whether the image was a normal, or a thermal image added
        
        Functionality - This function will update the list with the newest picture added to the folder.
                        It will not update the screen automatically.
                            This is because if someone is looking at the picture, we do not want to update the picture right away and a person
                                has to scroll all the way back to get to their previous picture
                        
        Output - none
                    This function updates the list of the thermal image, or normal image.
                    And update the maximum index number variable for the list
    '''
    def UpdateImageList(self, adddir, tag):
        if(tag == "norm"):
            Ui_TabWidget.norm.append(adddir)
            Ui_TabWidget.imgindexmax = len(Ui_TabWidget.norm) - 1
        elif(tag == "therm"):
            Ui_TabWidget.therm.append(adddir)
            Ui_TabWidget.imgindexmax = len(Ui_TabWidget.therm) - 1
        elif(tag == "sensor"):
            Ui_TabWidget.sensor_data.append(adddir)
            Ui_TabWidget.imgindexmax = len(Ui_TabWidget.sensor_data) - 1
        elif(tag=="location"):
            Ui_TabWidget.locations.append(adddir)
            #add instruction to add UAV Loc to array for tracking
            Ui_TabWidget.imgindexmax = len(Ui_TabWidget.locations) - 1
            Ui_TabWidget.UAV_Tracking_Lock(self, adddir)



    def UAV_Tracking_Lock(self, new_loc_path):    
        UAV_Loc = loc_Parse.Parse_Location(new_loc_path)
        self.UAVLocations.append(UAV_Loc)
        index = len(self.UAVLocations) - 1
        waypoint_info = [str(self.waypoints[index][0]), str(self.waypoints[index][1])]
        if(len(self.UAVLocations) == 2 and len(self.waypoints) >= 2):
            levels = UAV_Location_Tracking.define_Level(UAV_Loc, waypoint_info)
            if not levels:
                pass
            else:
                self.lat_level = levels[0]
                self.long_level = levels[1]
                self.waypoint_reached = 1
                
                    
        elif(len(self.UAVLocations) > 2 and len(self.waypoints) >= len(self.UAVLocations)):    
            levels = UAV_Location_Tracking.check_Level(self.lat_level, self.long_level, UAV_Loc, waypoint_info)
            if not levels:
                pass
            elif(levels == True):
                pass
            else:
                self.lat_level = levels[0]
                self.long_level = levels[1]
                self.waypoint_reached = index
            
            
        
    '''
        def Update_Rec_Label(self, active)
        This function is linked to the XBEE_COMS script. When the XBEE is active and reading it will change the text label to receiving
        Paramters - active - This indicates if the XBEE is active in data reception/transmission
        
        Functionality - This function will update the label to show if there is incoming data being received
                        or outgoing data being sent
                        
        Output - none
                    This function updates the label display
    '''
    def Update_Sensor_Display(self, data):
        self.TempRead.setText(data[0])
        self.HumRead.setText(data[1])
        self.LightRead.setText(data[2])
        self.PressRead.setText(data[3])
        self.AltRead.setText(data[4])
        self.alt_label.setText(data[4])
        
    def Update_Loc_Display(self, location):
        self.latitude_label.setText(location[0])
        self.long_label.setText(location[1])
        
    def Update_Rec_Label(self, active):
        if(active == True):
            self.Rec_Status.setText("Recieving")
        else:
            self.Rec_Status.setText("Not Recieving")
    '''
        def addPath(self, lat, long)
        This function is called from the loc_tracker web channel link.
        Paramters - lat, long - This is the latitude and longitude of the added waypoint
        
        Functionality - The location of the marker added to the map will be appended to the array on the GUI to update the list display
                        
        Output - none
                    This function adds to the waypoint tracker and updates the list display
    '''
    def addPath(self, lat, long, index):
        self.waypoints.insert(index, [str(lat),str(long)])
        print(self.waypoints)
        self.loc_list_max += 1
        self.string = str(self.loc_list_max) + '    ||    ' + str([lat,long])
        self.location_list.addItem(self.string)
        if(index == 1):
            self.next_lat_label.setText(str(lat))
            self.next_long_label.setText(str(long))
            self.next_alt_label.setText("75m")
        
        
    '''
        def remPath(self, index)
        This function is called from the loc_tracker web channel link.
        Paramters - index - The index of the waypoint to be removed.
        
        Functionality - The marker which is removed on the map is also removed from the array in the GUI code.
                        Additionally, the function to udpate the list display is also called.
                        
        Output - none
                    This function removes to the waypoint from the array and updates the list display
    '''
    def remPath(self, index):
        self.waypoints.pop(index)
        self.loc_list_max -= 1
        self.location_list.clear()

        self.list_index = 0
        for items in self.waypoints:
            self.updated_Item = str(self.list_index) + '    ||    ' + str(self.waypoints[self.list_index])
            self.location_list.addItem(self.updated_Item)
            self.list_index += 1
        
    
    def setBaseLoc(self, lat, long):
        self.base_lat = lat
        self.base_long = long
        print("base loc set")
    
    def setUAVLoc(self, lat, long):
        self.UAVLocations.append([lat, long])
        print(self.UAVLocations)
        self.latitude_label.setText(str(lat))
        self.long_label.setText(str(long))
        
    def Send_Path_List(self):
        Send_Loc_List.Create_File( self.waypoints)
    
    

#This is the main program routine which will create the GUI window and run
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TabWidget = QtWidgets.QTabWidget()
    ui = Ui_TabWidget()
    ui.setupUi(TabWidget)
    TabWidget.show()
    w = WatchNewPic.Watcher(ui.normpicDir, ui.thermpicDir, ui.sensorDir, ui.locDir, ui)
    thread1 = threading.Thread(target=w.run, daemon=True)
    thread1.start()
    #x = XBEE_COMS.ser_Watcher(ui)
    #thread2 = threading.Thread(target=x.run, daemon=True)
    #thread2.start()
    
    #l = loc_tracker.loc_tracker(ui)
    #thread3 = threading.Thread(target=l, daemon=True)
    #thread3.start()
    
    try:
        sys.exit(app.exec_())
    except:
        pass

