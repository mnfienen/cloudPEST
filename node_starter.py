from cloudPESTclient import *
import sys
import os
import time

##################################
### M A I N    F U N C T I O N ###
##################################
ofp = open(os.path.normpath('c:\\runner\\Node_starter\\node_starter.log.txt'),'a')
sys.stdout=ofp
sys.stderr=ofp



# now read in the FTP parameter file 
FTPadd,FTPflag, FTPdir = readFTPparfile()

# if FTPflag is true, pull down the detailed parfile from FTP
if FTPflag:
	retrieveFTPparfile(FTPadd, FTPdir)
# now parse the par file to obtain run information
bPcasename, bPexec, bPhost, bPport, bPlocalNodes = readRUNparfile()
# finally, open subprocesses for each node and store in a list to keep alive
live_nodes = []
print bPlocalNodes
for bPCurrentNode in bPlocalNodes:
	a = StartNode(bPcasename, bPexec, bPhost, bPport, bPCurrentNode)
	live_nodes.append(a)
for a in live_nodes:
	a.wait()
	print live_nodes
