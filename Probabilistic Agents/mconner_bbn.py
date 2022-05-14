'''
CPSC 415 -- Homework #5
Morgan Conner, University of Mary Washington, fall 2021
'''

import sys

def requirement_check():

	if len(sys.argv) < 3:
		print("Usage: mconner_bbn.py bbnFileName.bbn exact|approx 'query'")
		sys.exit(1)

	#Checks bbn file
	bbn_file = sys.argv[1]
	if '.bbn' not in bbn_file:
		print("Unknown file. Add .bbn if it's a file.")
		sys.exit(2)
	
	bbn_filePath = '/' + bbn_file
	if not Path(bbn_filePath).is_file():
		print("{} can't be located. Files should be placed in the same folder as mconner_bbn.py.".format(bbn_file))
		sys.exit(3)
	#else:
		#check format of file
	
	#Checks exact and approx
	if sys.argv[2] not in ['exact', 'approx']:
		print("{} not vaild. Must be one of the following: exact, approx.".format(sys.argv[2]))
		sys.exit(4)

	#Checks query syntax
	query = sys.argv[3]
	if query[0] or query[-1] != '"':
		print('{} must be surrounded by quotes like "{}"'.format(query,query))
		sys.exit(5)
	elif (query not in ['|', '~', '^']) and (query[0] or query[-1] != '"'):
		print("{} contains invalid logical operator. Only |, ~, and ^ are legal.".format(query))
		sys.exit(6)

	#Check if query is variable in file
	with open(bbn_file) as passed_file:
		data = passed_file.readlines()
		if query not in data:
			print("{} is an invalid query.".format(query))
