# cloudPEST client utilities
import datetime
import os
import time
from ftplib import FTP
import subprocess as sub

#####################################################################
### simple function to parse par file lines returning first value ###
#####################################################################
def parseLine(line):
    tmp = line.strip().split()
    return tmp[0]


##############################################
### function to read in FTP parameter file ###
##############################################
def readFTPparfile():
	# changeable path
    infile = r'c:\\runner\\Node_starter\\node_start_ftp.par'
    indat = open(infile,'r').readlines()
    FTPflag = parseLine(indat.pop(0))
    if FTPflag:
        FTPaddress = parseLine(indat.pop(0))
        FTPdir = parseLine(indat.pop(0))             
    else:
        FTPaddress = False
    return FTPaddress,bool(int(FTPflag)), FTPdir

####################################################
### function to retrieve parameter file from FTP ###
####################################################
def retrieveFTPparfile(FTPadd, FTPdir):
    from ftplib import FTP
    ftp = FTP(FTPadd)
    # asssuming anonymous FTP for the moment
    ftp.login()
    ftp.cwd(FTPdir)
	# changeable path
	ftp.retrbinary('RETR ' +  'node_start_runs.par',open(r'c:\\runner\\Node_starter\\node_start_runs.par','wb').write)


    
###############################################
### function to read in runs parameter file ###
###############################################    
def readRUNparfile():
	# changeable path
	indat = open(r'c:\\runner\\Node_starter\\node_start_runs.par','r').readlines()
    bPcasename = parseLine(indat.pop(0))
    bPexec = parseLine(indat.pop(0))
    bPhost = parseLine(indat.pop(0))
    bPport = parseLine(indat.pop(0))
    bPlocalNodes = []
    for line in indat:
        bPlocalNodes.append(parseLine(line))
    return bPcasename, bPexec, bPhost, bPport, bPlocalNodes

###########################################
###  function to fire off a single node ###
###########################################
def StartNode(bPcasename, bPexec, bPhost, bPport, bPCurrentNode):
    p=sub.Popen([os.path.normpath(bPCurrentNode + '/' + bPexec), 
    bPcasename, r'/h', bPhost + ':' + bPport],cwd=os.path.normpath(bPCurrentNode))
    return p
    