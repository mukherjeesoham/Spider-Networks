"""
Code exclusively for computing association_index_attacker using full association index 
given the pair M, N and data D.
"""

import numpy as np

def association_index_attacker(M, N, D):

	TR = D[0]
	ID = D[1]

	X    = 0.0
	Y_AB = 0.0
	Y_A  = 0.0
	Y_B  = 0.0

		#get X
	for i in range(0, len(ID) - 1):
		if np.array_equal(ID[i:i+2], [M,N]) and TR[i] == TR[i+1]:
			X += 1.0

	if X == 0.0:
		return 0		
	
	D = D.T
	for j in np.unique(TR):
		W = D[D[:, 0] == j]	#sample based on trial.
		ID_T = W[:,1]

		#get Y_AB 
		if M in ID_T and N in ID_T:
			if np.abs(np.argwhere(ID_T == N)[0,0] - np.argwhere(ID_T == M)[0,0]) != 1:
				A_1 = np.abs(np.argwhere(ID_T == N)[0,0] - np.argwhere(ID_T == M)[0,0]) != 1
				B_1 = np.abs(np.argwhere(ID_T == N)[0,0] - np.argwhere(ID_T == M)[0,0])
				C_1 = np.argwhere(ID_T == M)[0,0]
				D_1 = np.argwhere(ID_T == N)[0,0]
				Y_AB += 1.0

		#get Y_A and Y_B
		if M in ID_T and N not in ID_T:
			Y_A  += 1.0

		if M not in ID_T and N in ID_T:
			Y_B  += 1.0

	AI = X / (X + Y_AB + Y_A + Y_B)

	return AI 
	