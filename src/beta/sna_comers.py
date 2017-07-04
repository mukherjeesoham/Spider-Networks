"""
Read DATA CSV frame data generated from the excel files using Pandas
and generates the association matrix.

Input  : sheet_ID <frame ID>
Output : S_ID_DIR, R_ID_DIR, R_CM_DIR (comer network)

"""

import numpy as np
import pandas as pd
import os
import sna_association_index as ed
import sna_rank as rk

#--------------------------------------------------------------------------------
def read(sheet_ID):

	CC = pd.read_csv('/Users/apple/Documents/Network_Analysis/Playground/data/color_coding.csv', usecols=['color ID', 'code'])
	C = np.array(CC.fillna(0)).T

	#mention the headers
	data_columns = [4, 7, 9, 10, 14]
	info_columns = [0, 1]

	INFO = pd.read_csv(sheet_ID, usecols=info_columns)

	if int(INFO.ix[0,0]) < 10:
		FRAME_ID = '%s_F0%r' %(INFO.ix[0,1].split(" ")[0], int(INFO.ix[0,0]))
	else:
		FRAME_ID = '%s_F%r' %(INFO.ix[0,1].split(" ")[0], int(INFO.ix[0,0]))

	DATA = pd.read_csv(sheet_ID, usecols=data_columns).fillna(0)
	
	DATA = DATA[DATA.ix[:,1] != 1]
	DATA = DATA[DATA.ix[:,2] != 0]

	DATA.ix[:,2::4] = DATA.ix[:,4].str.strip().fillna(0)

	D = np.array(DATA).T

	ID_C  = D[2]
	ID_N  = np.copy(ID_C)

	ID_CM = D[4]
	ID_M  = np.copy(ID_CM)

	CF_R  = D[3]

	for h, i in enumerate(C[0]):
		np.put(ID_N, np.where(ID_C == i), C[1][h])

	for j, i in enumerate(ID_N):
		if isinstance(i, basestring) == True:
			ID_N[j] = 'U'

	for h, i in enumerate(C[0]):
		np.put(ID_M, np.where(ID_CM == i), C[1][h])

	for j, i in enumerate(ID_M):
		if isinstance(i, basestring) == True:
			ID_M[j] = 'U'

	for j, i in enumerate(CF_R):
		if i == 'R':
			CF_R[j] = 10.0
		elif i == 'G':
			CF_R[j] = 14.0
		elif i.lower() == 'up':
			CF_R[j] = 12.0
		elif i.lower() == 'down':
			CF_R[j] = 18.0

	repeat = []
	for i, j in enumerate(D[0]):
		if j != 0:
			repeat.append(i)

	C = np.hstack((np.diff(repeat),len(D[2]) - np.sum(np.diff(repeat))))
	A = np.unique(D[0])
	A = A[A > 0]

	B = np.repeat(A, C)
	FD = np.vstack((B, ID_N, CF_R, ID_M))

	DATAFRAME = pd.DataFrame({'D0: Trial':FD[0],'D1: ID':FD[1],'D2: Retreat':FD[2], 'D3: Comers':FD[3]})
	DATAFRAME.to_csv('/Users/apple/Documents/Network_Analysis/Playground/output/comers/%s.csv'%(FRAME_ID.split(" ", 1)[0]), sep = ',')

file = '/Users/apple/Documents/Network_Analysis/Playground/data/TD_18_03_2015/F-ID 5-Table 1.csv'
read(file)
