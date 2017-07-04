"""
Code expected to generate the csv for R. Needs serious debugging.
"""

import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt

list = glob.glob('/Users/apple/Documents/Network_Analysis/Playground/output/P_DIR/census*')

RC     = []
labels = []

for i in list:
    j = i.split('/')[-1]
    k = j.split('.')[0]
    l = k.split('_', 3)[1]
    m = k.split('_', 3)[2]

    N, AF, CF, R, S = np.loadtxt(i, delimiter=',', skiprows=1, unpack=True)
    R = R[R>0]

    RC.append(S)
    labels.append(l)

# plt.xlim(0, 12)
# plt.ylim(0, 6)
plt.ylabel('Frequency')

plt.xlabel('Number of attack instances + Number of comer instances')
plt.title('AF + CF')

colors = ['r', 'g', 'm']
plt.hist(RC, 10, histtype='bar', alpha = 0.5, color=colors, label=labels)
plt.legend(fontsize='small')
plt.grid()
plt.show()
# plt.savefig('/Users/apple/Downloads/mratio_%s_%s.pdf' %(l,m))

    # plt.close()
    #
    # plt.hist(S, bins=12, color='red', alpha = 0.3)
    # plt.ylabel('Frequency')
    # plt.xlabel('Number of attack instances + Number of comer instances')
    # plt.xlim(0, 12)
    # plt.ylim(0, 18)
    # plt.title('Participation AF + CF : %s %s' %(l, m))
    # plt.savefig('/Users/apple/Downloads/par_%s_%s.pdf' %(l,m))
    # plt.close()
