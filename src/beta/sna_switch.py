"""
Looks at which individuals
1. Switched sides.
2. Frequency of 'switch.'
Reads the data from S_ID_DIR.
"""

import numpy as np
import math
import os

def switch(file):
	DATA = np.genfromtxt(file, comments = '#')
	switch_census = np.zeros(np.shape(DATA)[0])
	switch_ID = np.zeros(40)
	switch_back = np.zeros((40,2))

	for j, i in enumerate(DATA):
		if math.isnan(i[1]) == True:	
			switch_census[j] = -1
		elif (i[1] <= 20 and i[2] == 1) or (i[1] > 20 and i[2] == -1):
			switch_census[j] = 1
			switch_ID[i[1]-1]  += 1.0
			switch_back[i[1]-1][0] += 1.0


		elif (i[1] <= 20 and i[2] == -1) or (i[1] > 20 and i[2] == 1):
			switch_census[j] = 0
			switch_back[i[1]-1][1] += 1.0


	A, B = np.unique(switch_census, return_counts = True)
	C, D =  np.unique(switch_ID, return_counts = True)

	W = switch_back[:,0]*switch_back[:,1]
	E = len(W[W > 0])

	print A
	print 'percentage switch: ', (100.0*B[-1])/np.sum(B)
	print B

	print '------------'

	print C
	print D

	print '------------'

	print E












