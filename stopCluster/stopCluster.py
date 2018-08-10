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
# stopCluster.py
#
# Stops a static cluster with the given cluster name.  A connection is
# made to the collective controller located at the given host and port,
# and the request to stop the cluster is passed to the ClusterManagerMBean.
#
# Required parameters:
# --clusterName= The name of the static cluster to operate on.
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
# ex. jython stopCluster.py --clusterName=clusterName --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2
#

import sys

from restConnector import JMXRESTConnector
import wlp_arguments as arguments
from wlp_arguments import MBeanArgs
import wlp_cluster as cluster

import java.lang.Throwable

# Arguments specifying which cluster to use
CLUSTER_NAME = '--clusterName'

# Subclass of command line arguments for stopCluster
class StopClusterArgs(MBeanArgs):

  # StopClusterArgs constructor 
  def __init__(self):
    # Make the list of value arguments that we accept
    valueParms = [CLUSTER_NAME]
    valueParms += arguments.MBEAN_VALUE_PARMS
    MBeanArgs.__init__(self, 0, arguments.STANDARD_KEYWORD_PARMS, valueParms)
    
  # Obtains our usage string
  def getUsage(self):
    usageString = MBeanArgs.getUsage(self) + \
                  CLUSTER_NAME + "=clusterName "
    return usageString
    		
  # Print usage of this command
  def printUsage(self):
    print "Usage: jython stopCluster.py " + self.getUsage()
    
  # Print required options
  def printRequiredHelp(self):
    print CLUSTER_NAME + "= The name of the cluster to stop"
    print
    MBeanArgs.printRequiredHelp(self)

  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Used to stop all cluster members in the cluster specified by the clusterName"
    print "parameter."
    print
    MBeanArgs.printHelp(self)
    print "Example: jython stopCluster.py --clusterName=clusterName --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2"
    
  # Validate that the arguments are specified correctly.
  def validate(self):
     # First validate the MBean arguments
    if MBeanArgs.validate(self): 
      # Then validate update server config arguments
      missingArg = None
      if (CLUSTER_NAME not in self):
        missingArg = CLUSTER_NAME
  
      if (missingArg != None):
        print "The following required argument is missing: " + missingArg
        self.printUsage()
      else :
        # Make sure the positional parameter was specified correctly.
        positionalParm = self.getPositional(0)
      return (missingArg == None)
    else:
      return False

    
# Stops a cluster
def stopCluster(trustStore, trustStorePassword, hostname, port, username,
                 password, clusterName):
    JMXRESTConnector.trustStore = trustStore
    JMXRESTConnector.trustStorePassword = trustStorePassword
    
    connector = JMXRESTConnector()
    connector.connect(hostname, port, username, password)
    mconnection = connector.getMBeanServerConnection()

    clusterManager = cluster.manager(mconnection)
    stopClusterResults = clusterManager.stop(argParser[CLUSTER_NAME], "")

    
    return stopClusterResults  

if __name__ == '__main__':
  argParser = StopClusterArgs()
  if (argParser.parse(sys.argv) == True):
    try:
      results = stopCluster(argParser[arguments.TRUST_STORE], 
                            argParser[arguments.TRUST_STORE_PASSWORD],
                            argParser[arguments.HOSTNAME], 
                            int(argParser[arguments.PORT]), 
                            argParser[arguments.USERNAME], 
                            argParser[arguments.PASSWORD], 
                            argParser[CLUSTER_NAME]) # Cluster name

      # See what the results of the stop were.  The returned map will have
      # an entry for each member server that we tried to stop.  The key
      # to the map is the results returned by the server command MBean, 
      # which contains the stderr, stdout, and return code of the command.
      if ((results != None) and (len(results) > 0)):
        for member in results:
          memberResults = results[member]
          if ((memberResults != None) and ("returnCode" in memberResults)):
            returnCode = memberResults["returnCode"]
            if (returnCode == 0):
              print str(member) + " stopped, RC=0"
            else:
              print str(member) + " not stopped, RC=" + str(returnCode)
          elif ((memberResults != None) and ("ExceptionMessage" in memberResults)):
            print str(member) + " stop operation resulted in an Exception: " + memberResults["ExceptionMessage"]
          else:
            print str(member) + " did not have any results reported or returned unexpected data!" + str(memberResults)
      else:
        print "No results were received from the stop cluster command"

    except java.lang.Throwable, t:
      print "An exception was caught while processing the stopCluster command"
      if (arguments.DEBUG not in argParser):
        print t.toString()
      else:
        t.printStackTrace()
