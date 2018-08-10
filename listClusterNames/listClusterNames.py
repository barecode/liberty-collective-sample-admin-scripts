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
# listClusterNames.py
#
# Lists the names of the clusters known to the collective controller.  A
# connection is made to the collective controller located at the given host 
# and port, and the request to list the cluster names is passed to the 
# ClusterManagerMBean.
# 
# Required parameters:
# --truststore= The path to the trust store to be used when establishing
#               a connection to the collectiveController.
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
# ex. jython listClusterNames.py --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2
#

import sys

from restConnector import JMXRESTConnector
import wlp_arguments as arguments
from wlp_arguments import MBeanArgs
import wlp_cluster as cluster

import java.lang.Throwable

# Subclass of command line arguments for listClusterNames
class ListClusterNamesArgs(MBeanArgs):

  # ListClusterNamesArgs constructor 
  def __init__(self):
	MBeanArgs.__init__(self, 0, arguments.STANDARD_KEYWORD_PARMS, arguments.MBEAN_VALUE_PARMS)

  # Print usage of this command
  def printUsage(self):
    print "Usage: jython listClusterNames.py " + self.getUsage()
    #MBeanArgs.printUsage(self)

  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Used to list the names of the clusters known to the collective controller."
    print
    MBeanArgs.printHelp(self)
    print "Example: jython listClusterNames.py --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2"
    
  # Validate that the arguments are specified correctly.
  def validate(self):
    if MBeanArgs.validate(self): 
	    # put subclass validation here
	    return True 
    else:
	    return False

# Lists cluster members
def listClusterNames(trustStore, trustStorePassword, hostname, port, username,
                     password):
    JMXRESTConnector.trustStore = trustStore
    JMXRESTConnector.trustStorePassword = trustStorePassword
    
    connector = JMXRESTConnector()
    connector.connect(hostname, port, username, password)
    mconnection = connector.getMBeanServerConnection()

    clusterManager = cluster.manager(mconnection)
    clusterNames = clusterManager.listClusterNames()
    
    return clusterNames

if __name__ == '__main__':
  argParser = ListClusterNamesArgs()
  if (argParser.parse(sys.argv) == True):
    try:
      results = listClusterNames(argParser[arguments.TRUST_STORE], 
                                 argParser[arguments.TRUST_STORE_PASSWORD],
                                 argParser[arguments.HOSTNAME], 
                                 int(argParser[arguments.PORT]), 
                                 argParser[arguments.USERNAME], 
                                 argParser[arguments.PASSWORD] )

      # See what the results were.
      if ((results != None) and (len(results) > 0)):
        print str(results)
      else:
        print "No clusters were defined"
            
    except java.lang.Throwable, t:
      print "An exception was caught while processing the listClusterMembers command"
      if (arguments.DEBUG not in argParser):
        print t.toString()
      else:
        t.printStackTrace()
