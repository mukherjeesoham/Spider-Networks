"""
Reads CSV data for the spider social network trials.
and generates the adjacency matrix for every dataset.
"""

import sna_parse_extension as rd
import sna_switch as ss
import numpy as np
import glob
import os


# file_list = glob.glob('/Users/apple/Documents/Network_Analysis/Playground/data/TD_18_03_2015/F*.csv')

# for file in file_list:
# 	print "Working on file: %s \n" %file
# 	rd.read(file)


file_list = glob.glob('/Users/apple/Documents/Network_Analysis/Playground/output/S_ID_DIR/*')

for file in file_list:
	print "Working on file: %s \n" %file
	ss.switch(file)


print 'All done.'


