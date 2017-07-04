"""
Code expected to generate the csv for R. Needs serious debugging.
"""

import numpy as np
import pandas as pd
import os
from igraph import *

########################################################
# Read CSV Data
########################################################

#reading color codes.
CC = pd.read_csv('~/Toolkit/Presentation/data/color_coding.csv', usecols=['color ID', 'code'])
SI = pd.read_csv('~/Toolkit/Presentation/data/SC_SR.csv', usecols=['Trail No.', 'No. of Attacker', 'ID of attackers'])

########################################################
# Clean data
########################################################

#populate NaN's
DS = SI.fillna(0)
CS = CC.fillna(0)

#filter trials with one participant, and empty rows.
DS = DS[DS.ix[:,1] != 1]	#filters trails with one participant
DS = DS[DS.ix[:,2] != 0]	#filters rows where there is no ID data.

#stripping white spaces
DS.ix[:,2] = DS.ix[:,2].str.strip()	#strip white spaces from ID data

#convert into numpy arrays
D = np.array(DS).T
C = np.array(CS).T

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

C = np.diff(repeat)
G = len(D[2]) - np.sum(C)

#update C with the last value
C = np.hstack((C,G))

#find trials which are surviving.
A = np.unique(D[0])
A = A[A > 0]

#create the trial column vector
B = np.repeat(A, C)

#generate cleaned up data i.e Final Data
FD = np.vstack((B, ID_N))


#----------------------------------------
# FD = FD.T[0:21, :]
# print FD
# FD = FD.T
#----------------------------------------

#wrting data to file
file = open('../test/FD.csv', 'w+')
for i in FD.T:
	file.writelines('%r\t\t\t%r\n'%(i[0], i[1]))
file.close()

#creating the adjacency matrix.
ADJ = np.zeros((40, 40))

########################################################
# Create the association matrix.
########################################################

def association_index_attacker(M, N, D):

	TR = D[0]
	ID = D[1]

	X    = 0.0
	Y_AB = 0.0
	Y_A  = 0.0
	Y_B  = 0.0

	#get X (occur in the whole vector: next to each other, and in the same trail)
	for i in range(0, len(ID) - 1):
		if np.array_equal(ID[i:i+2], [M,N]) and TR[i] == TR[i+1]:
			print 'Found at : ', i, 'continuing...'
			X += 1.0

	print "X : ", X

	if X == 0.0:
		print '%r : %r not found. Exiting.' %(M, N)
		return 0

	D = D.T
	for j in np.unique(TR):
		print "\n------------------Trial : ", j
		W = D[D[:, 0] == j]	#sample based on trial.

		ID_T = W[:,1]
		print 'ID: ', ID_T

		#get Y_AB (both occur in W, but not next to each other)
		if M in ID_T and N in ID_T:
			if np.abs(np.argwhere(ID_T == N)[0,0] - np.argwhere(ID_T == M)[0,0]) != 1:

				#debugging inner loop
				A_1 = np.abs(np.argwhere(ID_T == N)[0,0] - np.argwhere(ID_T == M)[0,0]) != 1
				B_1 = np.abs(np.argwhere(ID_T == N)[0,0] - np.argwhere(ID_T == M)[0,0])
				C_1 = np.argwhere(ID_T == M)[0,0]
				D_1 = np.argwhere(ID_T == N)[0,0]

				print B_1,C_1,D_1

				print 'Updating Y_AB...'
				Y_AB += 1.0

		#get Y_A and Y_B (only one of them occurs in W)
		if M in ID_T and N not in ID_T:
			print 'Updating Y_A...'
			Y_A  += 1.0

		if M not in ID_T and N in ID_T:
			print 'Updating Y_B...'
			Y_B  += 1.0

		print 'Y_A  : ', Y_A
		print 'Y_B  : ', Y_B
		print 'Y_AB : ', Y_AB


	#to restrict division by zero
	AI = X / (X + Y_AB + Y_A + Y_B)
	print '\nAI : ', AI



	return AI 	#association index

# populate the adjacency matrix
for k in range(0, 40):
	for l in range(0, 40):
		print '\n------------- calculating AI for : ', k+1, l+1
		ADJ[k][l] = association_index_attacker(k+1, l+1, FD)
		print '\n---------------------------------- '




########################################################
# Output
########################################################

np.savetxt('../R_data/R_SC_SR.csv', ADJ, fmt='%.4f', delimiter=',')
os.system('open ~/Toolkit/Presentation/R_data/R_SC_SR.csv')
