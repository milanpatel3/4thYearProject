'''
Created on Dec 27, 2017

@author: Milan Patel
'''
import serial
import binascii
from pip._vendor.pyparsing import unichr
import Decompress_Rec_Zip
import IRMA_GUI2
import zipfile
import time
from _datetime import timedelta
import datetime
from datetime import *
import os


class ser_Watcher:
    def __init__(self, ui):
        self.recpath = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\XBEE\\Rec.zip"
        self.port = "COM4"
        self.baud = 19200
        self.ser = serial.Serial(self.port, self.baud, timeout=5)
        self.output = b''
        self.data = b''
        self.unzip = False
        self.filedata = []
        self.filewrite = ""
        self.addsec = 240
        self.ui = ui
    
    def run(self):
        self.ser.close()
        self.ser.open()
        
        while 1:
            self.rec = self.ser.inWaiting()
            if(self.rec):
                self.start = datetime.now()
                self.delay = self.start + timedelta(seconds=self.addsec)
                print(self.delay)
                self.ui.Update_Rec_Label( True)
                while(datetime.now() <= self.delay):
                    self.data = self.ser.read(1024)
                    self.filedata.append(self.data)

                                    
                self.ser.flushInput()
                self.output = b''.join(self.filedata)
                print(len(self.output))
                EOCD = b'06054b50'
                index = self.output.find(EOCD)
                
                if(EOCD in self.output):
                    print("Failure Code 1: EOCD not found. ZIP file error.")
                elif((len(self.output) - index) != 44):
                    print("Failure Code 2: EOCD found, but incomplete file.")
                
                if(len(self.output)%2 != 0):
                    print("Failure Code 3: Received odd length byte stream. File cannot be made.")
                else:          
                    self.f = open(self.recpath, 'wb')
                    self.output = binascii.unhexlify(self.output)
                    self.f = open(self.recpath, 'wb')
                    self.f.write(self.output)                  
                    self.f.close()
                    self.unzip = Decompress_Rec_Zip.decompress_zip(self.ui.imgindexmax)
                    #os.remove(self.recpath)

                self.rec = 0
                self.data = ""
                self.output = b''
                self.ui.Update_Rec_Label( False)
                self.ser.close()
                self.ser.open()
                continue

    