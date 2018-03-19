#===============================================================================
# SM 2/2016
# Code to generate the adjacency matrix for creating the network.
# Calls sna_association_index file.
#===============================================================================

import numpy as np
import os
import itertools
import SNA_compute_AI as ed
import pandas as pd

def generate_attacker_matrix(path):
    REC_DATA = np.array(pd.read_csv(path, usecols=['D0: Trial', 'D1: Attackers', 'D2: Retreat']).fillna(0)).T
    FRAME_ID = path.split("/")[-1].split(".")[0]

    ADJ = np.zeros((40, 40))
    for k in range(0, 40):
    	for l in range(0, 40):
    		ADJ[k][l] = ed.association_index_attacker(k+1, l+1, REC_DATA)

    if not os.path.exists('../output/csv/ADJ'):
    	os.makedirs('../output/csv/ADJ')

    np.savetxt('../output/csv/ADJ/%s.csv' %(FRAME_ID), ADJ, fmt='%.4f', delimiter=',')
    print "Generated adjacency matrix for %s" %(FRAME_ID)
    return None

def generate_comer_matrix(REC_DATA, FRAME_ID):
	ADJ = np.zeros((40, 40))

	T    = REC_DATA[0]
	ID_C = REC_DATA[1]
	REC_DATA = REC_DATA.T

	for i in np.unique(T):
		SD = REC_DATA[REC_DATA[:, 0] == i]
		SD = SD[:, 1]
		for i in list(itertools.combinations(SD, 2)):
			ADJ[i[0]-1, i[1]-1] += 1.0

	ADJ = ADJ/len(np.unique(T))

	if not os.path.exists('../../output/csv/ADJ'):
		os.makedirs('../../output/csv/ADJ')

	np.savetxt('../../output/csv/ADJ/ADJ_C_%s.csv' %(FRAME_ID.split(" ", 1)[0]), ADJ, fmt='%.4f', delimiter=',')
	print "Generated comer sequence adjacency matrix for %s." %(FRAME_ID.split(" ", 1)[0])
	return None
