#==============================================================================
# SM 2/2016
# Master file to execute all pre-processing of the data.
#==============================================================================

import numpy as np
import glob
import os
import SNA_parse_csv as RD
import SNA_compute_ADJ_matrix as ADJ
import SNA_generate_random_datasets as RADJ

#------------------------------------------------------------------------------
# Parse network data into CSV files
#------------------------------------------------------------------------------
path = '../datasets/csv/08-02-2018-15T/F_ID_*.csv'
file_list = glob.glob(path)

print 80*("-")
print "==> SNA_master: Starting to parse data from CSV file."
for file in file_list:
	RD.read(file, PARSE='Attacker')

#------------------------------------------------------------------------------
# Generate adjacency matrices
#------------------------------------------------------------------------------

path = '../output/csv/sequence/A_F*.csv'
file_list = glob.glob(path)

print 80*("-")
print "==> SNA_master: Starting to generate adjacency matrix from CSV file."
for file in file_list:
	ADJ.generate_attacker_matrix(file)
print 80*'-'

#------------------------------------------------------------------------------
# Generate adjacency matrices for random datasets
#------------------------------------------------------------------------------

path = '../output/csv/sequence/A_F*.csv'
file_list = glob.glob(path)

print 80*("-")
print "==> SNA_master: Starting to generate adjacency matrix from CSV file."
for file in file_list:
	RADJ.generate_random_attacker_matrix(file, 2)
print 80*'-'
