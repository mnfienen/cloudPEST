'''
cloudPEST   version 1.0
	Implementing fixes for proper operation on Windows operating system
	    version 1.01 
	Further Windows-related fixes

a m!ke@usgs joint
mnfienen@usgs.gov

cloudPEST is a series of python functions designed for implementation
of parallel PEST computing using beoPEST on the Amazon EC2 cloud.

Prerequisite for use of these functions is proper installation of the
ec2-api tools available from Amazon (aws.amazon.com), and an AWS account.

IMPORTANT NOTE:  Even experimenting with these tools will incur charges
from AWS for every instance started.  Partial hours are charged at the 
full hour rate (see http://aws.amazon.com/ec2/#pricing for details)
and any instances left running and not properly shut down will incur
charges as well. 

It is recommended to verify on the AWS console that instances are
properly stopped or terminated at the end of a session.
'''
import os
import time
import sys
import subprocess as sub

###################
# Classes to hold data for cloudPEST
###################
class master:
	def __init__(self):
		self.ami_id      = [] # optional
		self.instance_id = [] # optional
		self.address     = [] # can be computer name, IP, or DNS address
		self.port        = [] # port opened if using beoPEST
		
class instances:
	def __init__(self):
		self.instance_id = []
		self.ami_id      = []
		self.state       = []
		self.password    = []
		self.ip_address  = []
		self.private_DNS = []
		self.public_DNS  = []
		self.group       = []
		self.port        = []

class images:
	def __init__(self):
		self.ami_id      = []
		self.description = []

		
		
#####################################################
#                   MAIN functions                  #
#####################################################

#
# query_images
#
def query_images():
	# query for available AMIs owned by the user
	# find proper newline character for splitting output
	newline_char = determine_newline()
	ims = images()
	p=sub.Popen('ec2-describe-images -o self',shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
	p.wait()
	currout,currerr=p.communicate()
	currerr = parse_errors(currerr, newline_char)
	if len(currerr)>0:
		cmsg = '\nERROR: could not get image descriptions'
		error_handler('ec2-describe-instances',cmsg,currerr)
		sys.exit('function failed')
	else :
		currout = currout.split(newline_char)
		for i in reversed(range(len(currout))):
			if (currout[i]==''):
				del(currout[i])
		for line in currout:
			tmp = line.strip().split()
			if tmp != '':
				if tmp[0] == 'IMAGE':
					ims.ami_id.append(tmp[1])
					ims.description.append(tmp[2])
	return ims
#
# run_instances
#
def run_instances(ami_id,instance_count,keyname,group,insttype=[],cnodes=[],availzone=[]):
	# find proper newline character for splitting output
	newline_char = determine_newline()
	# available instance types: this must be updated as new types become available
	available_instance_types = [
			't1.micro',
	        'm1.small',
	        'm1.large',
	        'm1.xlarge',
	        'm2.xlarge',
	        'm2.2xlarge',
	        'm2.4xlarge',
	        'c1.medium',
	        'c1.xlarge'
	        ]
	type_default_flag=False
	avail_default_flag=False
	# check types for inputs
	if not isinstance(ami_id,str):
		sys.exit('\nERROR: Instances could not be run.\nami_id must be a string\n'
		         + ami_id + ' was the provided the ami_id')
	if not isinstance(instance_count,int):
		sys.exit('\nERROR: Instances could not be run.\ninstance_count must be an integer\n'
		         + instance_count + ' was the provided the instance_count')
	if not isinstance(keyname,str):
		sys.exit('\nERROR: Instances could not be run.\nkeyname must be a string\n'
		         + keyname + ' was the provided the keyname')
	if not isinstance(group,str):
		sys.exit('\nERROR: Instances could not be run.\ngroup must be a string\n'
		         + group + ' was the provided the group')
	# if called without an insttype variable specified, make type_default_flag True, else check the options
	if len(insttype) == 0:
		type_default_flag = True
	elif insttype not in available_instance_types:
		sys.exit('\nERROR: Instance type requested not supported\n'
		         + insttype + ' was the provided instance type')
	# if called without availzone variable specified, make avail_default_flag True
	if len(availzone) == 0:
		avail_default_flag = True
	
	# if called without an instances class, make one
	if len(cnodes) == 0:
		cnodes = instances()
		
	runstring = ami_id + ' -n ' + str(instance_count) + ' -k ' \
			+ keyname + ' -g ' + group
	if type_default_flag == False:
		runstring += ' -t ' + insttype
	if avail_default_flag == False:
		runstring += ' --availability-zone ' + availzone
	p=sub.Popen('ec2-run-instances ' + runstring, shell=True, stdout=sub.PIPE, stderr=sub.PIPE )
	p.wait()
	currout,currerr=p.communicate()
	currerr = parse_errors(currerr, newline_char)
	if len(currerr) > 0:
		cmsg = '\nERROR: Instances could not be run.'
		error_handler('ec2-run-instances',cmsg,currerr)
		sys.exit('function failed')
	else:
		for line in currout:
			if (line[0] == 'INSTANCE'):
				cnodes.ami_id.append(line[2])
				cnodes.instance_id.append(line[1])
				cnodes.group.append(line[4]) 
	print currout
		

#
# start_instances
#
def start_instances(instance_id):
	# find proper newline character for splitting output
	newline_char = determine_newline()

	if not isinstance(instance_id,list):
		a=[]
		a.append(instance_id)
		instance_id = a
	for curr_inst in instance_id:
		if not isinstance(curr_inst,str):
			sys.exit('\nERROR: Invalid instance_id provided - must be a string\n'
			         + curr_inst + ' was the provided instance name')
		p=sub.Popen('ec2-start-instances ' + curr_inst, shell=True, stdout=sub.PIPE, stderr=sub.PIPE )
		p.wait()
		currout,currerr=p.communicate()
		currerr = parse_errors(currerr, newline_char)
		if len(currerr) > 0:
			cmsg = '\nERROR: Instance ' + curr_inst + ' could not be started.'
			error_handler('ec2-start-instances',cmsg,currerr)
		else:
			if ((currout[0] == 'INSTANCE') and (currout[-1] == 'pending')):
				print '\nInstance ' + curr_inst + ' started -- status pending'
			
#
# query_instances
#
def query_instances(specific_instances = []):
	# find proper newline character for splitting output
	newline_char = determine_newline()
	instances_list = instances()
	if len(specific_instances) > 0:
		if not isinstance(specific_instances,list):
			a=[]
			a.append(specific_instances)
			specific_instances = a
		for curr_inst in specific_instances:
			if not isinstance(curr_inst,str):
				sys.exit('\nERROR: Invalid instance_id provided - must be a string\n'
			         + curr_inst + ' was the provided instance name')
			p=sub.Popen('ec2-describe-instances ' + curr_inst,shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
			currout,currerr=p.communicate()
			currerr = parse_errors(currerr, newline_char)
			if len(currerr) > 0:
				cmsg = '\nERROR: Instance ' + curr_inst + ' could not be queried.'
				error_handler('ec2-describe-instances',cmsg,currerr)
			else:
				for line in currout.split(newline_char):
					if len(line) > 0:
						if ((line.split()[0] == 'INSTANCE') and 
						    (line.split()[5] == 'running')):
						    	instances_list = parse_instance_string(instances_list,line)
							
	else:
		print '\n***\nAll instances will be returned\n***\n'
		p=sub.Popen('ec2-describe-instances', shell=True, stdout=sub.PIPE, stderr=sub.PIPE )
		currout,currerr=p.communicate()
		currerr = parse_errors(currerr, newline_char)
		if len(currerr) > 0:
			cmsg = '\nERROR: Instances could not be queried.'
			error_handler('ec2-describe-instances',cmsg,currerr)
		else:
			for line in currout.split(newline_char):
				if len(line) > 0:
					if ((line.split()[0] == 'INSTANCE') and
					    (line.split()[5] == 'running')):
						instances_list = parse_instance_string(instances_list,line)
	return instances_list

#
# stop_instances
#
def stop_instances(instance_id):
	# find proper newline character for splitting output
	newline_char = determine_newline()

	if not isinstance(instance_id,list):
		a=[]
		a.append(instance_id)
		instance_id = a
	for curr_inst in instance_id:
		if not isinstance(curr_inst,str):
			sys.exit('\nERROR: Invalid instance_id provided - must be a string\n'
			         + curr_inst + ' was the provided instance name')
		p=sub.Popen('ec2-stop-instances ' + curr_inst, shell=True, stdout=sub.PIPE, stderr=sub.PIPE )
		p.wait()
		currout,currerr=p.communicate()
		currerr = parse_errors(currerr, newline_char)
		if len(currerr) > 0:
			cmsg = '\nERROR: Instance ' + curr_inst + ' could not be stopped.'
			error_handler('ec2-stop-instances',cmsg,currerr)
		else:
			if ((currout[0] == 'INSTANCE') and (currout[1] == curr_inst)):
				print '\nInstance ' + curr_inst + ' stopped -- status: ' + currout[-1]
			
#
# terminate_instances
#
def terminate_instances(instance_id):
	# find proper newline character for splitting output
	newline_char = determine_newline()

	if not isinstance(instance_id,list):
		a=[]
		a.append(instance_id)
		instance_id = a
	for curr_inst in instance_id:
		if not isinstance(curr_inst,str):
			sys.exit('\nERROR: Invalid instance_id provided - must be a string\n'
			         + curr_inst + ' was the provided instance name')
		p=sub.Popen('ec2-terminate-instances ' + curr_inst, shell=True, stdout=sub.PIPE, stderr=sub.PIPE )
		p.wait()
		currout,currerr=p.communicate()
		currerr = parse_errors(currerr, newline_char)
		if len(currerr) > 0:
			cmsg = '\nERROR: Instance ' + curr_inst + ' could not be terminated.'
			error_handler('ec2-terminate-instances',cmsg,currerr)
		else:
			if ((currout[0] == 'INSTANCE') and (currout[1] == curr_inst)):
				print '\nInstance ' + curr_inst + ' terminated -- status: ' + currout[-1]
			

#####################################################
#                  UTILITY functions                #
#####################################################
#
# parse described instances
#
def parse_instance_string(myinst,instance_string):
	'''
	function used by the query_instances function to parse the images string
	returns an appended version of the instances class.
	'''
	tmp = instance_string.split()
	myinst.instance_id.append(tmp[1])
	myinst.ami_id.append(tmp[2])
	myinst.public_DNS.append(tmp[3])
	myinst.private_DNS.append(tmp[4])
	myinst.state.append(tmp[5])
	myinst.group.append(tmp[6])
	myinst.ip_address.append(tmp[13])
	myinst.password.append('not yet assigned')
	myinst.port.append('not yet assigned')
	
	
	return myinst
		
	

#
# parse_errors
#
def parse_errors(inerr,nlc):
	'''
	function to parse the "Deprecated Xalan" OSX 10.6 
	message and the blank entries from currerr
	'''
	inerr = inerr.split(nlc)
	for i in reversed(range(len(inerr))):
		if (('[Deprecated] Xalan:' in inerr[i])
	            or (inerr[i]=='')):
			del(inerr[i])
	return inerr
#
# error_handler
#
def error_handler(ec2_fun_name,cloudPEST_err_string,ec2_err_string):
	'''
	function to pring out the error messages from ec2 and those
	specified by cloudPEST, thence terminate the program
	'''
	print cloudPEST_err_string
	print ec2_fun_name + ' returned the following error:'
	if len(ec2_err_string) == 1:
		print ec2_err_string[0]
	else:
		for line in ec2_err_string:
			print line

#
# determine_newline
#
def determine_newline():
	'''
	function to set the correct newline character 
	 which is platform dependent.  This is used for splitting
	 the output.
	'''
	newline_char = '\n'
	if (('win' in sys.platform.lower()) and (sys.platform.lower() != 'darwin')):
		newline_char = '\r\n'
	return newline_char