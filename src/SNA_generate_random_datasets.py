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
import SNA_parse_deadspiders as RDS

def scramble_dataset(REC_DATA, FRAME_ID):
    stream = REC_DATA.T
    trial  = np.unique(stream[:, 0])
    batch  = np.array([])
    for t in trial:
        batch = np.hstack((batch, np.random.choice(RDS.deletedeadspiders(FRAME_ID), len(stream[stream[:,0] == t]), replace=False).T + 1))
    stream[:, 1] = batch
    return stream.T

def generate_random_attacker_matrix(path, N):
    REC_DATA = np.array(pd.read_csv(path, usecols=['D0: Trial', 'D1: Attackers', 'D2: Retreat']).fillna(0)).T
    FRAME_ID = path.split("/")[-1].split(".")[0]
    if not os.path.exists('../output/csv/ADJ/random'):
    	os.makedirs('../output/csv/ADJ/random')
    for rindex in range(N):
        REC_RDATA = scramble_dataset(REC_DATA, FRAME_ID)
        ADJ = np.zeros((40, 40))
        for k in range(0, 40):
    	    for l in range(0, 40):
    		    ADJ[k][l] = ed.association_index_attacker(k+1, l+1, REC_RDATA)
        np.savetxt('../output/csv/ADJ/random/%s_R%r.csv' %(FRAME_ID, rindex+10000), ADJ, fmt='%.4f', delimiter=',')
        print "Generated randomized adjacency matrix for %s configuration %r" %(FRAME_ID, rindex)
    return None
