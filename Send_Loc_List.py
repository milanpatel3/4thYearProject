'''
Created on Mar 12, 2018

@author: Milan Patel
'''
def Create_File(waypoints = []):
    loc_list_file = "C:\\Users\\keton\\eclipse-workspace\\IRMA_GUI\\src\\Loc_List.txt"
    path_list = waypoints
    f = open(loc_list_file, "w")

    counter = 0
    for items in path_list:
        if(counter==0):
            f.write("B\n")
            f.write("Lat:" + str(items[0]) + "\n")
            f.write("Long:" + str(items[1]) + "\n")
            counter += 1
            f.flush()
        else:
            f.write(str(counter)+"\n")
            f.write("Lat:" + str(items[0]) + "\n")
            f.write("Long:" + str(items[1]) + "\n")
            counter += 1
            f.flush()
    f.close()
            