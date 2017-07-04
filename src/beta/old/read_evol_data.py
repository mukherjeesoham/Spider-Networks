"""
Reads CSV frame data using Pandas to see how the network evolves over trials.
and generates the association matrix.

Input  : sheet_ID <frame ID>
Output : S_ID_DIR, R_ID_DIR

"""

import numpy as np
import pandas as pd
import os
import sna_association_index_attacker as ed

#--------------------------------------------------------------------------------
def read_evolution(sheet_ID):
	CC = pd.read_csv('~/Documents/Network_Analysis/Playground/data/color_coding.csv', usecols=['color ID', 'code'])	
	C = np.array(CC.fillna(0)).T

	#mention the headers
	data_columns = [4, 7, 9]	
	info_columns = [0, 1]

	INFO = pd.read_csv(sheet_ID, usecols=info_columns)
	FRAME_ID = 'F%r_%s' %(int(INFO.ix[0,0]), INFO.ix[0,1])

	DATA = pd.read_csv(sheet_ID, usecols=data_columns).fillna(0)
		
	DS = DS[DS.ix[:,1] != 1]
	DS = DS[DS.ix[:,2] != 0]
	DS.ix[:,2] = DS.ix[:,2].str.strip()	

	D = np.array(DS).T 

	ID_C = D[2]
	ID_N = np.copy(ID_C)


	for h, i in enumerate(C[0]):
		np.put(ID_N, np.where(ID_C == i), C[1][h])

	for j, i in enumerate(ID_N):
		if isinstance(i, basestring) == True:	
			ID_N[j] = 'Unmarked'


	repeat = []
	for i, j in enumerate(D[0]):
		if j != 0:
			repeat.append(i)

	C = np.hstack((np.diff(repeat),len(D[2]) - np.sum(np.diff(repeat))))
	A = np.unique(D[0])
	A = A[A > 0]

	B = np.repeat(A, C)
	FD = np.vstack((B, ID_N))

	if not os.path.exists('./S_EV_ID_DIR'):
		os.makedirs('./S_EV_ID_DIR')

	file = open('./S_EV_ID_DIR/EV_S_ID_%s.asc'%(FRAME_ID), 'w+')
	file.writelines('%s\t%s\n'%('#T', '#ID'))
	file.writelines('%s\t%s\n'%('---', '---'))
	for i in FD.T:
		file.writelines('%r\t%r\n'%(i[0], i[1]))
	file.close()

	ADJ = np.zeros((40, 40, len(C)))

	def evolve(FD_evolve, n):
		for k in range(0, 40):
			for l in range(0, 40):
				ADJ[k][l][n] = ed.association_index_attacker(k+1, l+1, FD_evolve)

	for i, j in enumerate(C):
		k = np.sum(C[0:i+1])
		FD_I = FD[:, 0:k]
		evolve(FD_I, i)


	if not os.path.exists('./R_EV_ID_DIR'):
		os.makedirs('./R_EV_ID_DIR')

	for l in range(0, len(C)):
		np.savetxt('./R_EV_ID_DIR/R_EV_%s_%s.csv' %(FRAME_ID.split(" ", 1)[0], 100+l+1), ADJ[:,:,l], fmt='%.4f', delimiter=',')
	
	return "Parsed evolution data for %r." %(FRAME_ID.split(" ", 1)[0])
