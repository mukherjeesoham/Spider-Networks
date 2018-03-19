# File to compute the number of connections between 
# R > G, G < R, G > G and R > R
# TODO: Check the code; there seems to be unnatural trends in the data.

import numpy as np
import glob
import pandas as pd

files = glob.glob("../../output/csv/ADJ/ADJ_A_*.csv")

CWC = []
CNC = []

for i, _file in enumerate(files):
	ID =  _file.split("/")[-1].split(".")[0]

	# weighted relations
	ADJ    = np.loadtxt(_file, delimiter=",")
	H1, H2 = np.vsplit(ADJ,2)
	RR, RG = np.hsplit(H1,2)
	GR, GG = np.hsplit(H2,2)  
	CWC.append([np.sum(RR)/np.sum(ADJ), np.sum(RG)/np.sum(ADJ), \
				np.sum(GR)/np.sum(ADJ), np.sum(GG)/np.sum(ADJ), ID])

	# binary weighted relations
	ADJ[ADJ > 0] = 1
	H1, H2 = np.vsplit(ADJ,2)
	RR, RG = np.hsplit(H1,2)
	GR, GG = np.hsplit(H2,2)  
	CNC.append([np.sum(RR)/np.sum(ADJ), np.sum(RG)/np.sum(ADJ), \
				np.sum(GR)/np.sum(ADJ), np.sum(GG)/np.sum(ADJ), ID])

CWC = np.array(CWC)
CNC = np.array(CNC)
print np.shape(CWC)

DATAFRAME1 = pd.DataFrame({'ID':CWC[:,4], 'RR':CWC[:, 0], 'RG':CWC[:,1],\
					'GR':CWC[:,2], 'GG':CWC[:,3]})
DATAFRAME1.to_csv('../../output/network/graph/connections_weighted.csv')

DATAFRAME2 = pd.DataFrame({'ID':CWC[:,4], 'RR':CNC[:, 0], 'RG':CNC[:,1],\
					'GR':CNC[:,2], 'GG':CNC[:,3]})
DATAFRAME2.to_csv('../../output/network/graph/connections_binary.csv')

