#!/Users/elliottkrome/anaconda/bin/python

# Library imports
import xlrd
import numpy as np    # np will be alias for numpy when calling numpy functions


file_loc="/Users/elliottkrome/Downloads/templytics/Source_data.xlsx"
wb=xlrd.open_workbook(file_loc) # open workbook
data=wb.sheet_by_index(0)       # pick a sheet to read in


max_row=0                       # how manr rows in excel file to loop through
max_row=max(max_row,data.nrows)
# how many rows will our matrix be (determined by number of measles occurence)
meas_row=0
for row in range(max_row):
    if str(data.cell_value(row,0))=="Measles":   
        meas_row=meas_row+1

# make measles matrix
arr=[[0 for x in range(4)] for x in range(meas_row)]
meas_num=0
for row in range(max_row): 
    if str(data.cell_value(row,0))=="Measles":
        # Col(2) country, Col(7) year, Col(8) num_cases
        arr[meas_num][0] = data.cell_value(row,2)
        arr[meas_num][1] = data.cell_value(row,7)
        arr[meas_num][2] = data.cell_value(row,8)
        meas_num=meas_num+1

# create new empty matrix "arr_measles"
# for storing  unique combinations of country/year,
# only                                                        
arr_measels=[[0 for x in range(4)] for x in range(meas_num)]  
am_counter=0          # for keeping track of number unique country/year combinations found so far
does_exist=0          # boolean for finding if combination does exist
for row in range(meas_num):
    # handles countries whose names doesnt work for unknown reasons
    if row!=14 and row!=296 and row!=491 and row!=537 and\
       row!=576 and row!=588 and row!=430 and row!=434 and\
       row!=565 and row!=762:

        country = str(arr[row][0])                                # break string by spaces
        co = country.split()                                      # take only stuff before first space

	for existing_row in range(am_counter+1):                  # check if unique country/year exists
	    if co[0]==str(arr_measels[existing_row][0]):          # check if country matches
                if arr[row][1]==arr_measels[existing_row][1]:     # if cntry match, check if yr match
                    does_exist=1
        if does_exist==1:
            for which_row_matches in range(am_counter+1):         # check if row re country/year exists
	        if co[0]==arr_measels[which_row_matches][0]:      # country matching
                    if arr[row][1]==arr_measels[which_row_matches][1]: # year matching
                        arr_measels[which_row_matches][2] = arr_measels[which_row_matches][2] + arr[row][2]
	else:                                                     # if no country/year combo, make new
            arr_measels[am_counter+1][0]= co[0]                   # append new row with country
            arr_measels[am_counter+1][1]= arr[row][1]             # append new row with year
	    arr_measels[am_counter+1][2]= arr[row][2]             # append new row with occurences
            am_counter=am_counter+1                               # increment am_counter
        does_exist=0;                                             # reset does_exist 

count=1
is_found=0
corr_matrix=[[0 for x in range(12)] for x in range(am_counter)]
for row in range (am_counter):
    country = arr_measels[row][0]
    year = arr_measels[row][1]
    for crow in range (am_counter):
        if corr_matrix[crow][0]==country:
            is_found=1
            foundloc=crow
    if is_found==1:
        if year==2008:
	    corr_matrix[foundloc][1]=arr_measels[row][2]
	if year==2009:
	    corr_matrix[foundloc][2]=arr_measels[row][2]
	if year==2010:
            corr_matrix[foundloc][3]=arr_measels[row][2]
       	if year==2011:
            corr_matrix[foundloc][4]=arr_measels[row][2]
	if year==2012:
            corr_matrix[foundloc][5]=arr_measels[row][2]
	if year==2013:
            corr_matrix[foundloc][6]=arr_measels[row][2]
	if year==2014:
            corr_matrix[foundloc][7]=arr_measels[row][2]
	if year==2015:
            corr_matrix[foundloc][8]=arr_measels[row][2]
    else:
        corr_matrix[count][0]=country
	if year==2008:
            corr_matrix[count][1]=arr_measels[row][2]
        if year==2009:
            corr_matrix[count][2]=arr_measels[row][2]
        if year==2010:
            corr_matrix[count][3]=arr_measels[row][2]
        if year==2011:
            corr_matrix[count][4]=arr_measels[row][2]
        if year==2012:
            corr_matrix[count][5]=arr_measels[row][2]
        if year==2013:
            corr_matrix[count][6]=arr_measels[row][2]
        if year==2014:
            corr_matrix[count][7]=arr_measels[row][2]
        if year==2015:
            corr_matrix[count][8]=arr_measels[row][2]
        count=count+1
    is_found=0


# append std and mean
how_many_countrys=0
P=[0 for x in range(8)]                # initialize P 
for a in range(count):                 # iterate over each row of country matrix from above
    for b in range(8):                 # store all the yearly cases data in Matrix P
        P[b]= int(corr_matrix[a][b+1])
    corr_matrix[a][9]=np.std(P)        # std deviation
    corr_matrix[a][10]=np.mean(P)      # mean
    how_many_countrys=how_many_countrys+1


zmatrix=np.zeros((115,8),dtype=float)
for i in range(0,113):
    for j in range(1,8):
        if corr_matrix[i][9]!=0:
            zmatrix[i][j-1]=(corr_matrix[i][j]-corr_matrix[i][10])/corr_matrix[i][9]




solution=np.zeros((114,114),dtype=float)

for i in range(1,113):                # loop through rows in sol
    for j in range(1,113):            # loop through cols in sol
        solution[i][j]=(zmatrix[i][0]*zmatrix[j][1] + zmatrix[i][1]*zmatrix[j][2]\
                        + zmatrix[i][2]*zmatrix[j][3] + zmatrix[i][3]*zmatrix[j][4]\
                        + zmatrix[i][4]*zmatrix[j][5] + zmatrix[i][5]*zmatrix[j][6])/6


sum=0
output=[[0 for x in range(2)]for x in range(113)]
for i in range(3,113):
    for j in range(3,113):
        if j!=75:
            sum=float(solution[i][j])+sum
    output[i][0]=corr_matrix[i][0]
    output[i][1]=sum/113
    sum=0

for i in range(0,113):
    print "%-20s      %f"%(output[i][0], output[i][1])

