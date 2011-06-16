cloudPEST Open File Report distribution codes.

The files in this folder contain Python codes implementing the techniques
described in U.S. Geological Survey the cloudPEST Open-File Report 2011-1062.

The file cloudPEST.py contains the code that is used on a local machine
to start, stop, and otherwise control virtual machines (instances) on the cloud.

The remaining files contain code that should be deployed on each instance
on the cloud.

Details of all these files are contained in the U.S. Geological Survey Open-File Report 2011-1062
(also available at http://pubs.usgs.gov/of/2011/2062).

SPECIAL INSTRUCTIONS FOR WINDOWS USERS
There are a few issues that make using the Amazon EC2 tools a bit more 
challenging in the Windows environment. The instructions at tinyurl.com/ec2-win
are good, but we recommend the following changes:
1) Set the environment variables through control panel if you can
2) for JAVA_HOME, use "" like "c:\Program Files\java\jre6" because the space
in 'Program Files' causes trouble. Also, point to the "jre*" folder under "java"
rather than just the "java" folder.

VERSION HISTORY
v 1.0 Bug Fix Release
  Fixed problem with installation on Windows operating system.
v 0.1 Initial Release, March 24, 2011
