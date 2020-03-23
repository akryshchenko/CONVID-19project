################################################################
################################################################
### Thomas Merkh, tmerkh@g.ucla.edu
### 3.22.2020
################################################################
### 
### This code parses data found at https://github.com/CSSEGISandData/COVID-19, which in turn is being used for the interactive interface found at https://plague.com/
### Original data sources: WHO, CDC, ECDC, NHC, DXY, 1point3acres, Worldometers.info, BNO, state and national government health department, and local media reports.
### 
### The resulting data matrix is(are) stored as a .mat file.
###
### Each row is a region, i.e. Hawaii, US.  The row information for each matrix row is contained in the corresponding file ending in '_row_info.txt'
### Each column corresponds to a particular date (sequential).  The date information can be found in the corresponding file ending in '_col_names.txt'
### Each entry of the matrix produced is referring to the number of "Confirmed", "Deaths", or "Recovered" patients with COVID19, on a particular date, in a particular place.
### 
### 
################################################################
### To run this:  The user needs to set the filepath correctly, this can be seen below where this Python program is being held outside the COVID19master folder downloadable from Github
### As the number of dates change, and possibly the number of locations being reported on, the size of the data matrix must change accordingly. 
################################################################
################################################################

import sys, os
import numpy as np
import scipy.io

cwd = os.getcwd()
print(cwd)

extensions = ["Confirmed","Deaths","Recovered"] # The endings of the 3 data files
extension  = extensions[0]                      # Done this way since the extension gets used later to save the matrix

filepath = cwd + "\\COVID19master\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_19-covid-" + extension + ".csv"

col_names = []
row_info = []                # Holds lists containing information about each row of the data matrix 
data = np.zeros((483,60))    # 483 regions reported on, 60 days for each

with open(filepath, 'rt') as myfile:
    lcount = 1
    for line in myfile:
        line = line.strip("\n")
        if(lcount == 1):
            col_names = line.split(",")
        else:
            linelist = line.split(",")
            if(len(linelist)-4 > len(col_names)-4):  # if true, this row had an extra "," in it, due to a different naming scheme used half way through
                # To fix, need to combine the first two entries
                linelist_fixed = [str(linelist[0]+linelist[1]).strip('"')] + linelist[2:]
                linelist = linelist_fixed
            data[lcount-1,:] = np.asarray([int(i) for i in linelist[4:]])
            row_info.append(linelist[:4])
        lcount += 1

#print(col_names)
#print(data)
#print(row_info)

## Save the data:

scipy.io.savemat(extension + ".mat", {extension : data})

MyFile = open(extension + '_col_names.txt','w')
for i in range(len(col_names)):
    if(i != len(col_names)-1):
        MyFile.write(col_names[i]+", ")
    else:
        MyFile.write(col_names[i])
MyFile.close()

MyFile = open(extension + '_row_info.txt','w')
for i in range(len(row_info)):
    if(i != len(row_info)-1):
        for j in range(len(row_info[i])):
            if(j != len(row_info[i])-1):
                MyFile.write(row_info[i][j]+", ")
            else:
                MyFile.write(row_info[i][j]+'\n')
    else:
        for j in range(len(row_info[i])):
            if(j != len(row_info[i])-1):
                MyFile.write(row_info[i][j]+", ")
            else:
                MyFile.write(row_info[i][j])
MyFile.close()

print("Program completed")