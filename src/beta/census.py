import numpy as np
import glob

files = glob.glob("*.csv" )
file_list = []
for i, file in enumerate(files):
	file_list.append([int(file.split("_")[2].split(".")[0][1:]), file])
FL = np.array(file_list)
file_list = FL[FL[:,0].argsort()][:,1]

for file in file_list:
	print 40*'-'
	print file.split(".")[0]
	print 40*'-'
	DATA     = np.loadtxt(file, skiprows=1, delimiter=',')
	TRIAL_ID = np.unique(DATA[:,1])
	
	if(0):
		WINNERS = np.zeros((len(TRIAL_ID), 2))
		for _k, _trial in enumerate(TRIAL_ID):
			SUB_TRIAL = DATA[DATA[:,1] == _trial][:, 1:4]
			PLAYERS, COUNTS = np.unique(SUB_TRIAL[:,2], return_counts=True)
			WINNERS[_k][0] = _trial
			WINNERS[_k][1] = np.argmax(COUNTS)

		WINNERS = WINNERS[WINNERS[:,1] > 0]
		print "Retreat side distribution: ",  np.unique(WINNERS[:,1], return_counts=True)[1]
		
		if(0):
			for row in WINNERS:
				print row

	if(0):
		WINNERS = np.zeros((len(TRIAL_ID), 2))
		RATIO = []
		for _k, _trial in enumerate(TRIAL_ID):
			SUB_TRIAL = DATA[DATA[:,1] == _trial][:, 1:4]
			ATTACKERS = SUB_TRIAL[:,1]

			if len(ATTACKERS[ATTACKERS>20]) > 0 :
				RATIO.append(1.0*len(ATTACKERS[ATTACKERS<20])/(1.0*len(ATTACKERS[ATTACKERS>20])))

		print np.mean(np.array(RATIO))

	if(1):
		WINNERS = np.zeros((len(TRIAL_ID), 2))
		RATIO = []
		for _k, _trial in enumerate(TRIAL_ID):
			SUB_TRIAL = DATA[DATA[:,1] == _trial][:, 1:4]
			RETREAT = SUB_TRIAL[:,2]

			if len(RETREAT[RETREAT==14]) > 0 :
				RATIO.append(1.0*len(RETREAT[RETREAT==10])/(1.0*len(RETREAT[RETREAT==14])))

		print "%1.4f"%np.mean(np.array(RATIO))








