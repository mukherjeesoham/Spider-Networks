"""
ReaDATA CSV frame data generated from the excel files using Pandas
and generates the association matrix.

Input  : sheet_ID <frame ID>
Output : S_ID_DIR, R_ID_DIR

"""

import numpy as np
import pandas as pd
import os

import sna_association_index_attacker as ed
import sna_rank as rk

#--------------------------------------------------------------------------------
def read(sheet_ID):

	CC = pd.read_csv('/Users/apple/Documents/Network_Analysis/Playground/data/color_coding.csv', usecols=['color ID', 'code'])
	C = np.array(CC.fillna(0)).T

	#mention the headers
	data_columns = [4, 7, 9, 10]
	info_columns = [0, 1]

	INFO = pd.read_csv(sheet_ID, usecols=info_columns)

	if int(INFO.ix[0,0]) < 10:
		FRAME_ID = '%s_F0%r' %(INFO.ix[0,1].split(" ")[0], int(INFO.ix[0,0]))
	else:
		FRAME_ID = '%s_F%r' %(INFO.ix[0,1].split(" ")[0], int(INFO.ix[0,0]))

	DATA = pd.read_csv(sheet_ID, usecols=data_columns).fillna(0)
	DATA = DATA[DATA.ix[:,1] != 1]
	DATA = DATA[DATA.ix[:,2] != 0]
	DATA.ix[:,2] = DATA.ix[:,2].str.strip()
	DATA.ix[:,3] = DATA.ix[:,3].str.strip()

	D = np.array(DATA).T

	ID_C = D[2]
	ID_N = np.copy(ID_C)

	CF_R = D[3]

	for h, i in enumerate(C[0]):
		np.put(ID_N, np.where(ID_C == i), C[1][h])

	for j, i in enumerate(ID_N):
		if isinstance(i, basestring) == True:
			ID_N[j] = 'U'

	repeat = []
	for i, j in enumerate(D[0]):
		if j != 0:
			repeat.append(i)

	C = np.hstack((np.diff(repeat),len(D[2]) - np.sum(np.diff(repeat))))
	A = np.unique(D[0])
	A = A[A > 0]

	B = np.repeat(A, C)
	FD = np.vstack((B, ID_N))

	# call rank function
	rk.rank(FD.T, FRAME_ID)

	if not os.path.exists('/Users/apple/Documents/Network_Analysis/Playground/output/S_ID_DIR'):
		os.makedirs('/Users/apple/Documents/Network_Analysis/Playground/output/S_ID_DIR')

	file = open('/Users/apple/Documents/Network_Analysis/Playground/output/S_ID_DIR/%s.txt'%(FRAME_ID.split(" ", 1)[0]), 'w+')
	file.writelines('#Dataset\t: %s\n'%(FRAME_ID.split(" ", 1)[0]))
	file.writelines('#N (T)\t: %r\n'%(len(np.unique(D[0])) - 1))
	file.writelines('%s\t%s\t%s\n'%('#T', '#ID', '#CF_R'))
	file.writelines('%s\t%s\t%s\n'%('#---', '#---', '#---'))
	for j, i in enumerate(FD.T):
		if CF_R[j] == 'R':
			file.writelines('%r\t%r\t%r\n'%(i[0], i[1], -1))
		elif CF_R[j] == 'G':
			file.writelines('%r\t%r\t%r\n'%(i[0], i[1], 1))
		else:
			file.writelines('%r\t%r\t%r\n'%(i[0], i[1], 0))
	file.close()

	ADJ = np.zeros((40, 40))

	for k in range(0, 40):
		for l in range(0, 40):
			ADJ[k][l] = ed.association_index_attacker(k+1, l+1, FD)

	if not os.path.exists('/Users/apple/Documents/Network_Analysis/Playground/output/R_DIR'):
		os.makedirs('/Users/apple/Documents/Network_Analysis/Playground/output/R_DIR')

	np.savetxt('/Users/apple/Documents/Network_Analysis/Playground/output/R_DIR/R_%s.csv' %(FRAME_ID.split(" ", 1)[0]), ADJ, fmt='%.4f', delimiter=',')
	return "Parsed data for %r." %(FRAME_ID.split(" ", 1)[0])
