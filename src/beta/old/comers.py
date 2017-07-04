import numpy as np
import pandas as pd
import os
import glob

#color aspect
CC = pd.read_csv('../../data/color_coding.csv', usecols=['color ID', 'code'])	
CS = CC.fillna(0)
C = np.array(CS).T

#reading attack ID
file_ID = '../S_ID_DIR/S_ID_F1_SCDR.txt'
data = np.genfromtxt(file_ID)
ID = data.T[1]

#startign with comer ID
cols = [14]
file_CM = './F1.csv'
SI = pd.read_csv(file_CM, usecols=cols)
ID_N = np.array(SI.fillna(0))
ID_Comers =  ID_N[ID_N > 0]
for h, i in enumerate(C[0]):
	np.put(ID_Comers, np.where(ID_Comers == i), C[1][h])

ID_total = np.arange(1, 41, 1)

# for i in ID_Comers:
# 	np.delete(ID_total, np.where(ID_total == i))

for i in ID:
	np.delete(ID_total, np.where(ID_total == i))

print ID_total
