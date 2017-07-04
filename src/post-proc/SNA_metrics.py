#===============================================================================
# SM 2/2016
# The code looks at which individuals
#	came most number of times and their rank in attack

#===============================================================================

import os
import math
import numpy as np
import glob
import pandas as pd

def rank(DATA, FRAME_ID):

	TN = DATA[0]
	ID = DATA[1]

	print "Computing metrics [Rank] for %s" %(FRAME_ID)
	set, count = np.unique(ID, return_counts = True)
	set_2, count_2 = np.unique(count, return_counts = True)

	rankings = np.zeros((len(np.unique(TN)), 40))
	DATA = DATA.T

	for i, j in enumerate(np.unique(TN)):
		sub_data = DATA[DATA[:,0] == j]
		ID = sub_data.T[1]
		for k, l in enumerate(ID):
			if l != 'U' and math.isnan(float(l)) == False:
				rankings[i][int(float(l)-1)] = (1.0 - k/(len(ID)*1.0)) 	#the rank function

	rank_score = np.mean(rankings, axis = 0)

	if not os.path.exists('../../output/network/metrics/rank'):
		os.makedirs('../../output/network/metrics/rank')
	np.savetxt('../../output/network/metrics/rank/rank_%s_%s.csv' %(FLAG, FRAME_ID.split(" ", 1)[0]), rank_score, fmt='%.4f', delimiter=',')
	return None

