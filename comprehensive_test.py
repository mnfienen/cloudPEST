'''
comprehensive test script for cloudPEST:

N.B.! This starts one instance but kills it at the end.

'''
from cloudPEST import *

# query images available
myims = query_images()
for i,j in enumerate(myims.ami_id):
	print 'ami_id = {0}:  description = {1}'.format(j,myims.description[i])

# run an instance
run_instances(myims.ami_id[0], 1, 'mnf_office','mnf_runner',insttype='t1.micro')

# query instances to see what's running
myisnt = query_instances()

mycurrinst = query_instances(specific_instances = myinst.instance_id[0])

# stop instance
stop_instances(myinst.instance_id[0])

# start instance
start_instances(myinst.instance_id[0])

# terminate instance
terminate_instances(myinst.instance_id[0])