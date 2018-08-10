''' COPYRIGHT LICENSE: This information contains sample code provided in source code form. You may copy, modify, 
and distribute these sample programs in any form without payment to IBM for the purposes of developing, using, marketing or 
distributing application programs conforming to the application programming interface for the operating platform for which the sample code is written. 
Notwithstanding anything to the contrary, IBM PROVIDES THE SAMPLE SOURCE CODE ON AN "AS IS" BASIS AND IBM DISCLAIMS ALL WARRANTIES, 
EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, 
FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND ANY WARRANTY OR CONDITION OF NON-INFRINGEMENT. IBM SHALL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, 
INCIDENTAL, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR OPERATION OF THE SAMPLE SOURCE CODE. IBM HAS NO OBLIGATION TO PROVIDE MAINTENANCE, 
SUPPORT, UPDATES, ENHANCEMENTS OR MODIFICATIONS TO THE SAMPLE SOURCE CODE.

Copyright IBM Corp. 2013.
All Rights Reserved. Licensed Materials - Property of IBM. '''

#
# getClusterStatus.py
#
# Gets the cluster status for the given cluster.
# A connection is made to the collective controller located at the given
# host and port, and the request to get the status for the cluster is passed
# to the ClusterManagerMBean.
# 
# The first positional parameter is the cluster name.
#
# Required parameters:
# --truststore= The path to the trust store to be used when establishing
#               a connection to the collective controller.
# --truststorePassword= The password for the truststore specified by 
#                       --truststore.
# --host= The host name where the collective controller is running.
# --port= The https port where the collective controller is listening.
# --user= The user name to use when connecting to the collective controller.
# --password= The password to use when connecting to the collective controller.
# 
# Optional parameters:
# --help= Displays help text.
# --debug= Displays additional details when an error occurs.
#
# ex. jython getClusterStatus.py clusterName --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2
#

import sys

from restConnector import JMXRESTConnector
import wlp_arguments as arguments
from wlp_arguments import MBeanArgs
import wlp_cluster as cluster

import java.lang.Throwable

# Subclass of command line arguments
class GetClusterStatusArgs(MBeanArgs):

  # getClusterStatusArgs constructor 
  def __init__(self):
	MBeanArgs.__init__(self, 1, arguments.STANDARD_KEYWORD_PARMS, arguments.MBEAN_VALUE_PARMS)

  # Print usage of this command
  def printUsage(self):
    print "Usage: jython getClusterStatus.py clusterName " + self.getUsage()

  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Get the status for the given cluster."
    print
    MBeanArgs.printHelp(self)
    print "Example: jython getClusterStatus.py clusterName --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2"
    
  # Validate that the arguments are specified correctly.
  def validate(self):
    if MBeanArgs.validate(self): 
	    # put subclass validation here
	    return True 
    else:
	    return False

# Starts a cluster
def getClusterStatus(trustStore, trustStorePassword, hostname, port, username,
                     password, clusterName):
    JMXRESTConnector.trustStore = trustStore
    JMXRESTConnector.trustStorePassword = trustStorePassword
    
    connector = JMXRESTConnector()
    connector.connect(hostname, port, username, password)
    mconnection = connector.getMBeanServerConnection()

    clusterManager = cluster.manager(mconnection)
    status = clusterManager.getStatus(clusterName) #invoke get status for the cluster

    print "Status for cluster " + str(clusterName) + ": "+str(status)
    return status
    
if __name__ == '__main__':
  argParser = GetClusterStatusArgs()
  if (argParser.parse(sys.argv) == True):
    results = getClusterStatus(argParser[arguments.TRUST_STORE], 
                              argParser[arguments.TRUST_STORE_PASSWORD],
                              argParser[arguments.HOSTNAME], 
                              int(argParser[arguments.PORT]), 
                              argParser[arguments.USERNAME], 
                              argParser[arguments.PASSWORD], 
                              argParser.getPositional(0)) # Cluster name

