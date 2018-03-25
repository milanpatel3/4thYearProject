'''
Created on Jan 3, 2018

@author: keton
'''

import PIL
from PIL import Image
import zipfile
import os

def decompress_zip(indexmax):
    recpath = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\XBEE\\Rec.zip"
    decom_path = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\XBEE\\"
    normpicDir = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Normal_Image\\"
    thermpicDir = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Thermal_Image\\"
    sensorDir = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Sensor_Data\\"
    locDir = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Location\\"



    rec_zip = zipfile.ZipFile(recpath)
    rec_zip.extractall(decom_path)
    for root, dirs, files in os.walk(decom_path):
        for file in files:
            if "norm" in file:
                newname = "image(" + str(indexmax + 1) + ").jpg"
                os.renames(os.path.join(root, file), os.path.join(normpicDir, newname))
            elif "therm" in file:
                newname = "thermimg(" + str(indexmax + 1) + ").jpg"
                os.renames(os.path.join(root, file), os.path.join(thermpicDir, newname))    
            elif "sensor" in file:
                newname = "sensor(" + str(indexmax + 1) + ").txt"
                os.renames(os.path.join(root, file), os.path.join(sensorDir, newname))
                f = open(os.path.join(sensorDir, newname), "r")
                out = f.read()
                f.close()
                f = open(os.path.join(sensorDir, newname), "w")
                f.write(out)
                f.flush()
                f.close()
            elif "location" in file:
                newname = "location(" + str(indexmax + 1) + ").txt"
                os.renames(os.path.join(root, file), os.path.join(locDir, newname))
                
                
    
    rec_zip.close()
    os.remove(recpath)
    return True
        
if __name__ == "__main__":
    decompress_zip(4)
        
        
'''
recpath = "C:\\Users\\keton\\Documents\\ELEC 4907 - Project\\Testing\Rec.jpg"
recpath1 = "C:\\Users\\keton\\Documents\\ELEC 4907 - Project\\Testing\Rec_resize.jpg"

image = Image.open(recpath)
resolution = (800,800)
newImage = image.resize(resolution)

newImage.save(recpath1, optimize=True, quality=95)
'''