#==============================================================================
# SM 8/2018
# Parse dead spiders data and be able to pass the choice vector
# to the random network generator
#==============================================================================

import numpy as np
import pandas as pd
import os

def deletedeadspiders(FRAME_ID):
    C  = np.array(pd.read_csv('../datasets/color-coding/color_coding.csv', usecols=['color ID', 'code']).fillna(0)).T
    DS = np.array(pd.read_csv('../datasets/dead-spiders/dead-spiders.csv', usecols=['Frame ID', 'ID of dead spider']).fillna(0)).T
    ID = DS[1]

    for h, i in enumerate(C[0]):
        np.put(ID, np.where(ID == i), C[1][h])

    return np.delete(np.arange(1, 41), ID[np.where(DS[0] == FRAME_ID)] - 1)
