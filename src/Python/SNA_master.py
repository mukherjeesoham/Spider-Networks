#==============================================================================
# SM 2/2016
# Master file to execute all pre-processing of the data. The pipeline includes
# 	1. Reads CSV data for the spider social network trials. [sna_parse_csv]
# 	2. generates the adjacency matrix for every dataset. [sna_association_index]
# 	3. Computes rank. [sna_rank]
# 	4. Checks for consistency measures. [sna_rank]
#==============================================================================

import numpy as np
import glob
import os
import SNA_parse_csv as RD

path = '../../datasets/Final/SNA/F_ID_*.csv'
file_list = glob.glob(path)

print "\n==> SNA_master: Starting to parse data from CSV file."
for file in file_list:
	print 80*'-'
	print "Loading file on path: %s" %file

	# Parse attacker and comer data.
	RD.read(file, PARSE='Attacker')
	# RD.read(file, PARSE='Comer')

print 80*'-'
print 'Parse complete. All done!'
