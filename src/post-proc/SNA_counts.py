# File to compute the number of connections between 
# R > G, G < R, G > G and R > R
# TODO: Check the code; there seems to be unnatural trends in the data.

import numpy as np
import glob
import matplotlib.pyplot as plt
from numpy import linalg as LA
import matplotlib.gridspec as gridspec

files = glob.glob("../../output/csv/ADJ/ADJ_A_*.csv")

fig = plt.figure()
GS1 = gridspec.GridSpec(2, 2)
ax1 = fig.add_subplot(GS1[0])
ax2 = fig.add_subplot(GS1[1])

ax3 = fig.add_subplot(GS1[2])
ax4 = fig.add_subplot(GS1[3])



metadata = []
connections = np.zeros((len(files), 8))

for i, _file in enumerate(files):
	ADJ    = np.loadtxt(_file, delimiter=",")
	H1, H2 = np.vsplit(ADJ,2)
	RR, RG = np.hsplit(H1,2)
	GR, GG = np.hsplit(H2,2)  

	metadata.append("_".join(_file.split("/")[-1].split(".")[-2].split("_")[2:]))
	connections[i] = np.array([np.size(RR[RR > 0]), np.size(GG[GG > 0]), 
		np.size(GR[GR > 0]), np.size(RG[RG > 0]),
		np.mean(RR), np.mean(GG), np.mean(GR), np.mean(RG)])

locs   =  [0,1,2,3] 
labels = ["RR", "GG", 'GR', "RG"]
DC, SCDR, SCSR = np.vsplit(connections, 3)

ax1.plot(np.sum(DC[:, 0:4], axis=0), "r--o", label='DC')
ax1.plot(np.sum(SCDR[:, 0:4], axis=0), "b--o", label='SCDR')
ax1.plot(np.sum(SCSR[:, 0:4], axis=0), "g--o", label='SCSR')
ax1.set_ylabel("Total number of connections")
ax1.set_xticks(locs)
ax1.set_xticklabels(labels)
ax1.legend(frameon=False)

ax2.plot(np.median(DC[:, 0:4], axis=0), "r--o", label='DC')
ax2.plot(np.median(SCDR[:, 0:4], axis=0), "b--o", label='SCDR')
ax2.plot(np.median(SCSR[:, 0:4], axis=0), "g--o", label='SCSR')
ax2.set_ylabel("Median number of connections")
ax2.set_xticks(locs)
ax2.set_xticklabels(labels)
ax2.legend(frameon=False)

ax3.plot(np.mean(DC[:, 4:], axis=0), "r--o", label='DC')
ax3.plot(np.mean(SCDR[:, 4:], axis=0), "b--o", label='SCDR')
ax3.plot(np.mean(SCSR[:, 4:], axis=0), "g--o", label='SCSR')
ax3.set_ylabel("Mean strength of connections")
ax3.set_xticks(locs)
ax3.set_xticklabels(labels)
ax3.legend(frameon=False)

ax4.plot(np.median(DC[:, 4:], axis=0), "r--o", label='DC')
ax4.plot(np.median(SCDR[:, 4:], axis=0), "b--o", label='SCDR')
ax4.plot(np.median(SCSR[:, 4:], axis=0), "g--o", label='SCSR')
ax4.set_ylabel("Median strength of connections")
ax4.set_xticks(locs)
ax4.set_xticklabels(labels)
ax4.legend(frameon=False)


plt.show()