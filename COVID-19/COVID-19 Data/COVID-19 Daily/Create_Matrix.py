################################################################
################################################################
### Thomas Merkh, tmerkh@g.ucla.edu
### 4.1.2020
################################################################
### 
### This code parses data found at https://github.com/CSSEGISandData/COVID-19, which in turn is being used for the interactive interface found at https://plague.com/
### Original data sources: WHO, CDC, ECDC, NHC, DXY, 1point3acres, Worldometers.info, BNO, state and national government health department, and local media reports.
### 
### The resulting data matrices are stored as a .mat files.
###
### Each row is a region, i.e. Hawaii, US.  The row information for each matrix row is contained in the corresponding file ending in '_row_info.txt'
### Each column corresponds to a particular date (sequential).  The date information can be found in the corresponding file ending in '_col_names.txt'
### Each entry of the matrix produced is referring to the number of "Confirmed", "Deaths", or "Recovered" patients with COVID19, on a particular date, in a particular place.
### 
### 
################################################################
### To run this:  The user needs to set the filepath correctly, this can be seen below where this Python program is being held outside the COVID19master folder downloadable from Github
### The updated dataset as of the March 23rd has changed so that the naming conventions for deaths vs. confirmed vs recovered, global vs USA are basically all different. 
### This updated script takes this into account. 
################################################################
################################################################

import sys, os
import numpy as np
import scipy.io

#############################################################################
############## User - Please choose which extension 0, 1, or 2 ##############
#############################################################################

extensions = ["confirmed","deaths","recovered"] # The endings of the 3 data files
extension  = extensions[2]                      # Done this way since the extension gets used later to save the matrix

#############################################################################
#############################################################################
#############################################################################

# I set the file path by hand, one may use os.getcwd() to obtain the current working directory
filepath = "/home/tmerkh/CSSEGISandData/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_" + extension + "_global.csv"

# this is in place since recovered USA data is not available (as of april 1st 2020)
if(extension != "recovered"):
    filepath2 = "/home/tmerkh/CSSEGISandData/COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_" + extension + "_US.csv"

lcount  = 0
lcount2 = 0
with open(filepath, 'rt') as myfile:
    for line in myfile:
        if(lcount == 1):
            N_Days = len(line.split(","))-4  # There are 4 entries in each row which aren't dates
        lcount += 1

if(extension != "recovered"):
    with open(filepath2, 'rt') as myfile:
        for line in myfile:
            if(lcount2 == 0):
                if(extension == "confirmed"):
                    N_Days2 = len(line.split(","))-11 # There are 11 entries in each row which aren't dates for confirmed
                elif (extension == "deaths"):
                    N_Days2 = len(line.split(","))-12 # There are 12 entries in each row which aren't dates for deaths    
            lcount2 += 1

col_names = []
row_info  = []
data = np.zeros((lcount,N_Days))    # regions = rows, N_days :: global data

if(extension != "recovered"):
    col_names2 = []
    row_info2  = [] 
    data2 = np.zeros((lcount2,N_Days2))    # regions = rows, N_days :: USA data

# Global
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

# USA
if(extension != "recovered"):
    with open(filepath2, 'rt') as myfile:
        lcount2 = 1
        for line in myfile:
            line = line.strip("\n")
            if(lcount2 == 1):
                col_names2 = line.split(",")
            else:
                if(extension == "confirmed"):
                    linelist = line.split(",")
                    linelist_fixed = linelist[:10] + [str(linelist[10]+linelist[11]).strip('"')] + linelist[13:]
                    linelist = linelist_fixed
                    while(len(linelist[11:]) < N_Days2):
                        linelist.append('0')
                    data2[lcount2-1,:] = np.asarray([int(i) for i in linelist[11:]])
                    row_info2.append(linelist[:11])


                elif(extension == "deaths"):
                    linelist = line.split(",")
                    linelist_fixed = linelist[:10] + [str(linelist[10]+linelist[11]+linelist[12]).strip('"')] + linelist[13:]
                    linelist = linelist_fixed
                    if(len(linelist) == len(col_names2)):
                        data2[lcount2-1,:] = np.asarray([int(i) for i in linelist[12:]])
                        row_info2.append(linelist[:12])
            lcount2 += 1

## Save the data
cwd = os.getcwd()

# Make sure that the directory already exists
if not(os.path.isdir(cwd + "/TimeSeriesMatrices")):
    print("Creating TimeSeriesMatrices")
    os.mkdir(cwd + "/TimeSeriesMatrices")
os.chdir("TimeSeriesMatrices")


## Global First

scipy.io.savemat(extension + "global.mat", {extension+"global" : data})

MyFile = open(extension + '_col_names_global.txt','w')
for i in range(len(col_names)):
    if(i != len(col_names)-1):
        MyFile.write(col_names[i]+", ")
    else:
        MyFile.write(col_names[i])
MyFile.close()

MyFile = open(extension + '_row_info_global.txt','w')
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


## USA now
if(extension != "recovered"):
    scipy.io.savemat(extension + "USA.mat", {extension+"USA" : data2})
    MyFile = open(extension + '_col_names_USA.txt','w')
    for i in range(len(col_names2)):
        if(i != len(col_names2)-1):
            MyFile.write(col_names2[i]+", ")
        else:
            MyFile.write(col_names2[i])
    MyFile.close()
    
    MyFile = open(extension + '_row_info_USA.txt','w')
    for i in range(len(row_info2)):
        if(i != len(row_info2)-1):
            for j in range(len(row_info2[i])):
                if(j != len(row_info2[i])-1):
                    MyFile.write(row_info2[i][j]+", ")
                else:
                    MyFile.write(row_info2[i][j]+'\n')
        else:
            for j in range(len(row_info2[i])):
                if(j != len(row_info2[i])-1):
                    MyFile.write(row_info2[i][j]+", ")
                else:
                    MyFile.write(row_info2[i][j])
    MyFile.close()
os.chdir("..")
print("Program completed")