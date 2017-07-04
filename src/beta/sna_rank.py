"""
Looks at which individuals
1. Came most number of times.
2. Their rank in attack
"""

import numpy as np
import math
import os

def rank(DATA, FRAME_ID):
	TN = DATA.T[0]
	ID = DATA.T[1]

	rankings = np.zeros((len(np.unique(TN)), 40))

	for i, j in enumerate(np.unique(TN)):
		sub_data = DATA[DATA[:,0] == j]
		ID = sub_data.T[1]
		for k, l in enumerate(ID):
			if l != 'U' and math.isnan(l) == False:
				rankings[i][l-1] = (1.0 - k/(len(ID)*1.0)) 	#the rank function

	rank_score = np.mean(rankings, axis = 0)

	if not os.path.exists('/Users/apple/Documents/Network_Analysis/Playground/output/T_Rank'):
		os.makedirs('/Users/apple/Documents/Network_Analysis/Playground/output/T_Rank')
	np.savetxt('/Users/apple/Documents/Network_Analysis/Playground/output/T_Rank/RK_%s.csv' %(FRAME_ID.split(" ", 1)[0]), rank_score, fmt='%.4f', delimiter=',')
