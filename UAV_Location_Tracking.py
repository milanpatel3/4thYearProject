'''
Created on Mar 12, 2018

@author: Milan Patel
'''
import math
from _operator import index



'''
Level        Decimal Accuracy        Latitude Tolerance(m)        Longitude Tolerance(m)
0                Perfect Match                0.000                        0.000
1                0.000001                     0.110                        0.096
2                0.000010                     1.110                        0.955
3                0.000100                    11.090                        9.551
4                0.001000                   110.870                       95.506
5                0.010000                  1108.740                      955.060
6                0.100000                 11087.440                     9550.600
7                1.000000                110870.400                    95506.000
'''

def define_Error_Table(level, tag):
    lat_error = [0, 0.11, 1.11, 11.09, 110.87, 1108.74, 11087.44, 110870.4]
    long_error = [0, 0.096, 0.955, 9.551, 95.506, 955.060, 9550.6, 95506]
    if("lat" in tag):
        return lat_error[level]
    elif("long" in tag):
        return long_error[level]
        
def define_Level( UAV_Loc = [], Ref_Loc = []):
    set_lat_level = False
    set_long_level = False
     
    UAV_lat = UAV_Loc[0]
    UAV_lat = UAV_lat[0:(UAV_lat.index('.') + 7)]
        
    UAV_long = UAV_Loc[1]
    UAV_long = UAV_long[0:(UAV_long.index('.') + 7)]
        
    Ref_lat = Ref_Loc[0]
    Ref_lat = Ref_lat[0:(Ref_lat.index('.') + 7)]
        
    Ref_long = Ref_Loc[1]
    Ref_long = Ref_long[0:(Ref_long.index('.') + 7)]
        
    counter = 0
    while (counter > -8):
        if(set_lat_level == False):
            if(counter == 0):
                if(UAV_lat in Ref_lat):
                    lat_level = 0
                    set_lat_level = True
                    break
                else:
                    counter -= 1
            else:
                if(UAV_lat[:counter] in Ref_lat):
                    lat_level = -1*counter
                    set_lat_level = True
                    break
                else:
                    counter -= 1
                        
                        
    counter = 0
    while (counter > -8):
        if(set_long_level == False):
            if(counter == 0):
                if(UAV_long in Ref_long):
                    long_level = 0
                    set_long_level = True
                    break
                else:
                    counter -= 1
            else:
                if(UAV_long[:counter] in Ref_long):
                    long_level = -1*counter
                    set_long_level = True
                    break
                else:
                    counter -= 1
        
    if (set_long_level == set_lat_level == True):
        levels = [lat_level, long_level]
        return levels
    else:
        return False
    
    
        
def check_Level( levels, index, UAV_Loc = [], Ref_Loc = []):
    
    lat_level = levels[index][0]
    long_level = levels[index][1]

    levels = define_Level(UAV_Loc, Ref_Loc)
    if (levels == False):
        return False
    else:
        if(lat_level == levels[0] and long_level == levels[1]):
            return True
        else:
            return levels
        
        

def Error_Calculator(level, tag, UAV_Loc, Ref_Loc):
    UAV_loc = UAV_Loc[0:(UAV_Loc.index('.') + 7)]
    Ref_loc = Ref_Loc[0:(Ref_Loc.index('.') + 7)]
    total_error = 0
    error_dist = 0    
    
    counter = -1
    while(counter >= -level):
        if(counter == -1):
            compare_UAV = UAV_loc[counter:]
            compare_Ref = Ref_loc[counter:]
            if(compare_Ref == compare_UAV):
                counter -= 1
                pass
            else:
                difference = math.fabs(float(compare_Ref) - float(compare_UAV))
                error_dist = define_Error_Table(-counter, tag)
                total_error += difference*error_dist
                counter -= 1
            
        else:
            compare_UAV = UAV_loc[counter:counter + 1]
            compare_Ref = Ref_loc[counter:counter + 1]
            if(compare_Ref == compare_UAV):
                counter -= 1
                pass
            else:
                difference = math.fabs(float(compare_Ref) - float(compare_UAV))
                error_dist = define_Error_Table(-counter, tag)
                total_error += difference*error_dist
                counter -= 1
    
    return total_error

def define_Error_Individual(levels, index, UAV_Loc = [], Ref_Loc = []):
    lat_level = levels[index][0]
    long_level = levels[index][1]
    if(lat_level == 0 and long_level == 0):
        errors = ['Latitude Error: 0m', 'Longitude Error: 0m' ]
        return errors
    elif(lat_level == 0 and long_level != 0):
        long_error = Error_Calculator(long_level, "long", UAV_Loc[1], Ref_Loc[1])
        errors = ['Latitude Error: 0m', 'Longitude Error: ' + str(long_error) + 'm']
        return errors
    elif(long_level == 0 and lat_level != 0):
        lat_error = Error_Calculator(lat_level, "lat", UAV_Loc[0], Ref_Loc[0])
        errors = ['Latitude Error: '+ str(lat_error) + 'm', 'Longitude Error: 0m']
        return errors
    else:
        lat_error = Error_Calculator(lat_level, "lat", UAV_Loc[0], Ref_Loc[0])
        long_error = Error_Calculator(long_level, "long", UAV_Loc[1], Ref_Loc[1])
        errors = ['Latitude Error: '+ str(lat_error) + 'm', 'Longitude Error: ' + str(long_error) + 'm']
        return errors
    
    

def define_Error_Full(levels, UAV_Loc = [], Ref_Loc = []):
    UAV_Loc = UAV_Loc
    Ref_Loc = Ref_Loc
    index_max = len(UAV_Loc) - 1
    errors_list = []
    counter = 0
    while(counter <= index_max):
        error_object = define_Error_Individual(levels, counter, UAV_Loc[counter], Ref_Loc[counter])
        errors_list.append(error_object)
        counter += 1
        
    create_Errors_File(errors_list)    
    return errors_list

def create_Errors_File(errors_list):
    error_output_file = 'C:\\Users\\keton\\Desktop\\Location_Errors.txt'
    f = open(error_output_file, 'w')
    max = len(errors_list) - 1
    counter = 0
    while(counter <= max):
        str_write = str(counter) + ': ' + errors_list[counter][0] + ', ' + errors_list[counter][1]
        f.write(str_write + '\n')
        f.flush()
        counter += 1
        
    f.close()


            
if __name__ == "__main__":
    import sys
    levels = []
    waypoints = [['45.3985574', '-75.7124743'], ['45.400090441839836', '-75.71779580268554'], ['45.404610224807946', '-75.71822495612793'], ['45.406176998501266', '-75.71204514655761'], ['45.40328445928038', '-75.70354790839843'], ['45.40093416210898', '-75.70766778144531']]
    UAV_Loc = [['45.3985574', '-75.7124743'], ['45.400836', '-75.717554'], ['45.404646', '-75.71823'], ['45.4012660', '-75.755761'], ['45.40328445928038', '-75.70354790839843'], ['45.40190416210898', '-75.70662778144531']]
    
    max_index = len(UAV_Loc) - 1
    output = define_Level(UAV_Loc[0], waypoints[0])    
    levels.append(output)
    errors = define_Error_Individual(levels, 0, UAV_Loc[0], waypoints[0])
    counter = 1
    while(counter <= max_index):
        changes = check_Level(levels, counter-1, UAV_Loc[counter], waypoints[counter])
        if(changes == True):
            levels.append(levels[len(levels) - 1])
        else:
            levels.append(changes) 
            
        errors = define_Error_Individual(levels, counter, UAV_Loc[counter], waypoints[counter])
        #print(errors) 
        
        counter += 1
    print(levels)
    
    full_errors = define_Error_Full(levels, UAV_Loc, waypoints)
    print(full_errors)
    '''
    errors = define_Error_Individual(levels, 0, UAV_Loc[0], waypoints[0]) 
    print(errors)        
    '''
            