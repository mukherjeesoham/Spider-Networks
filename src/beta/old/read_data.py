"""
Code expected to generate the csv for R. Needs serious debugging.
"""

import numpy as np
import pandas as pd
import os
import edges as ed


########################################################
# Read CSV Data
########################################################

#reading data
CC = pd.read_csv('../data/color_coding.csv', usecols=['color ID', 'code'])
SI = pd.read_csv('../data/SC_SR.csv')

#----------------------------------------
print "\nFound the following headers ..." 
print "-------------------------------"
for i,j  in enumerate(SI.columns):
	print i,'', j
#----------------------------------------

#modify which columns you want
cols = [4, 7, 9]
SI = pd.read_csv('../data/SC_SR.csv', usecols=cols)

# ########################################################
# # Clean data
# ########################################################

#populate NaN's
CS = CC.fillna(0)
DS = SI.fillna(0)

# filter trials with one participant, and empty rows.
DS = DS[DS.ix[:,1] != 1]	
DS = DS[DS.ix[:,2] != 0]	

# #stripping white spaces
DS.ix[:,2] = DS.ix[:,2].str.strip()	

#convert into numpy arrays
D = np.array(DS).T 
C = np.array(CS).T

#picking the ID.
ID_C = D[2]
ID_N = np.copy(ID_C)

#convert strings to unique IDs
for h, i in enumerate(C[0]):
	np.put(ID_N, np.where(ID_C == i), C[1][h])

#convert unmarked individals to UN.
for j, i in enumerate(ID_N):
	if isinstance(i, basestring) == True:	#replacing Unmarked with NA
		ID_N[j] = 'Unmarked'

#populating trial vector.
repeat = []

for i, j in enumerate(D[0]):
	if j != 0:
		repeat.append(i)

# #update C (trial vector) with the last value
C = np.hstack((np.diff(repeat),len(D[2]) - np.sum(np.diff(repeat))))

#find trials which are surviving.
A = np.unique(D[0])
A = A[A > 0]

#create the trial column vector
B = np.repeat(A, C)

#generate cleaned up data i.e Final Data
FD = np.vstack((B, ID_N))

#display final data 
print "\nReduced data set for association index:"
print "-------------------------------"
for j, i in enumerate(FD.T):
	print i[0], '\t', i[1]

#wrting data to file
file = open('../test/FD_SC_SR.csv', 'w+')
file.writelines('%s\t%s\n'%('#T', '#ID'))
file.writelines('%s\t%s\n'%('---', '---'))
for i in FD.T:
	file.writelines('%r\t%r\n'%(i[0], i[1]))
file.close()

########################################################
# Create the association matrix.
########################################################

#creating the adjacency matrix.
ADJ = np.zeros((40, 40))

# populate the adjacency matrix
for k in range(0, 40):
	for l in range(0, 40):
		print '\n------------- calculating AI for : ', k+1, l+1
		ADJ[k][l] = ed.association_index_attacker(k+1, l+1, FD)
		print '\n---------------------------------- '


# ########################################################
# # Output
# ########################################################
np.savetxt('../R_data/R_SC_SR_parse.csv', ADJ, fmt='%.4f', delimiter=',')


