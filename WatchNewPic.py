'''
Created on Oct 30, 2017

@author: Milan Patel
'''
import time
import glob
import IRMA_GUI2
import loc_Parse
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from urllib.request import FileHandler
from PyQt5 import QtCore, QtGui, QtWidgets

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

'''
    class Watcher:
        This class watcher creates a watchdog to monitor the directories
        
        Functions - init - this initializes all variables to use in the watcher class
                    run - this creates the watchdog observers to monitor the directories and trigger an event handler
                    
            def __init__(self, normDir, thermDir, ui)
            
                Paramters - normDir - This is the directory for the normal images
                            thermDir - This is the directory for the thermal images
                            ui - this is the current running open window of the GUI
        
                Functionality - this function just initializes all the variables locally.
                        
                Output - none  
                
            def run(self)
            
                Paramters - self - This allows us to use all variables locally set in __init__
        
                Functionality - this function creates two observers. One for each directory.
                                The observers then monitor the directories.
                                There is an event handler, which is called when either observer views a change in their respective directory
                        
                Output - none  

    
'''
class Watcher:

    def __init__(self, normDir, thermDir, sensorDir, locDir, ui):
        self.normPicDir = normDir
        self.thermPicDir = thermDir
        self.sensorDir = sensorDir
        self.locDir = locDir
        self.ui = ui
        self.observer1 = Observer()
        self.observer2 = Observer()
        self.observer3 = Observer()
        self.observer4 = Observer()


    def run(self):
        event_handler = Handler(self.ui)
        self.observer1.schedule(event_handler, self.normPicDir, recursive=True)
        self.observer2.schedule(event_handler, self.thermPicDir, recursive=True)
        self.observer3.schedule(event_handler, self.sensorDir, recursive=True)
        self.observer4.schedule(event_handler, self.locDir, recursive=True)
        self.observer1.start()
        self.observer2.start()
        self.observer3.start()
        self.observer4.start()

        try:
            while True:
                time.sleep(5)
        except:
            self.observer1.stop()
            self.observer2.stop()
            self.observer3.stop()
            self.observer4.stop()
            print ("Error")

        self.observer1.join()
        self.observer2.join()
        self.observer3.join()
        self.observer4.join()
        

'''
    class Handler:
        This class is where the event handler is implemented
        
        Functions - init - this initializes all variables to use in the Handler class
                    on_created - this is the event trigger. When a new file is created in the directory, 
                                    the event handler on_created is triggered to begin function calls
                    
            def __init__(self, mainTabWidget)
            
                Paramters - mainTabWidget - this is the current running open window of the GUI
        
                Functionality - this function just initializes all the variables locally.
                        
                Output - none  
                
            def on_created(self, event)
            
                Paramters - self - This allows us to use all variables locally set in __init__
                            event - this is the signal triggered when the observer sees a change in the directory
                                    an event is created, and this event shows the information of the change in the directory
        
                Functionality - this function is triggered when a new image appears in the normal or thermal image directory.
                                TIt then calls the UpdateImageList function in the IRMA_GUI2 window. But the call is made on the current active window
                                        which is mainTabWidget.
                                We sort through here if the update was made in the normal image directory or the thermal image directory.
                        
                Output - none  

    
'''
        
class Handler(FileSystemEventHandler):
    
    def __init__(self, mainTabWidget):
        self.mainTabWidget = mainTabWidget
    def on_created(self, event):
        # Take any action here when a file is first created.
        if "Normal_Image" in event.src_path:
            #Watcher.normList.append(event.src_path)
            #print ("Received created event - %s." % event.src_path)
            
            self.mainTabWidget.UpdateImageList( event.src_path, "norm")
        elif "Thermal_Image" in event.src_path:
            self.mainTabWidget.UpdateImageList( event.src_path, "therm")
            #Watcher.thermList.append(event.src_path)
            #print ("Received modified event - %s." % event.src_path)
        elif "Sensor_Data" in event.src_path:
            self.mainTabWidget.UpdateImageList( event.src_path, "sensor")
            
        elif "Location" in event.src_path:
            self.mainTabWidget.UpdateImageList( event.src_path, "location")
            