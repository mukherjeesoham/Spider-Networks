import numpy as np
import pandas as pd
import os
import sna_association_index as ed
import sna_rank as rk

#--------------------------------------------------------------------------------
def read(sheet_ID):
	C = np.array(pd.read_csv('/Users/apple/Documents/Network_Analysis/Playground/data/color_coding.csv', usecols=['color ID', 'code']).fillna(0)).T

	INFO = pd.read_csv(sheet_ID, usecols=[0,1])
	if int(INFO.ix[0,0]) < 10:
		FRAME_ID = '%s_F0%r' %(INFO.ix[0,1].split(" ")[0], int(INFO.ix[0,0]))
	else:
		FRAME_ID = '%s_F%r' %(INFO.ix[0,1].split(" ")[0], int(INFO.ix[0,0]))

	data_columns = [4, 13, 14]
	DATA = pd.read_csv(sheet_ID, usecols=data_columns).fillna(0)


	DATA = DATA[DATA.ix[:,2] != 0]
	print DATA
	if DATA.empty:
		print 'No comer data found. Aborting.'
		return 0
	print '---------------'
	DATA.ix[:,2] = DATA.ix[:,2].str.strip()
	print DATA

	D = np.array(DATA).T

	T    = D[0]
	NC   = D[1]
	ID_C = D[2]

	for h, i in enumerate(C[0]):
		np.put(ID_C, np.where(ID_C == i), C[1][h])

	for k in range(0, len(ID_C)):
		if isinstance(ID_C[k], basestring) == True:
			ID_C[k] = -1

	R1 = []
	for i, j in enumerate(D[0]):
		if j != 0:
			R1.append(i)
	C = np.hstack((np.diff(R1),len(D[2]) - np.sum(np.diff(R1))))
	A = np.unique(D[0])
	A = A[A > 0]
	B = np.repeat(A, C)

	REC_DATA = np.vstack((B, ID_C))
	DATAFRAME = pd.DataFrame({'D0: Trial':REC_DATA[0],'D1: Comers':REC_DATA[1]})

	if not os.path.exists('/Users/apple/Documents/Network_Analysis/Playground/output/P_DIR'):
		os.makedirs('/Users/apple/Documents/Network_Analysis/Playground/output/P_DIR')

	DATAFRAME.to_csv('/Users/apple/Documents/Network_Analysis/Playground/output/P_DIR/C_ID_%s.csv'%(FRAME_ID.split(" ", 1)[0]), sep = ',')


file = '/Users/apple/Documents/Network_Analysis/Playground/data/TD_18_03_2015/F-ID 11-Table 1.csv'
read(file)
