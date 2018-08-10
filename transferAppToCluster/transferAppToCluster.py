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

# NOTE:
# 		This script uses the FileTransfer MBean to upload the file, hence the remoteFileAccess element must be specified in the server.xml of the server that will have configuration update.
# 		Without this you will get a file permission error when using the script.
#
#		Here is an example of a remoteFileAccess element:
#		<remoteFileAccess>
#			<writeDir>${server.config.dir}</writeDir>
#		</remoteFileAccess>
#
# 		For further information and examples for remoteFileAccess, please visit the Information Center for "WebSphere Application Server V8.5 Liberty profile" 
#		and search for "List of provided MBean" or "remoteFileAccess".
#
# transferAppToCluster.py
#
# Provides operations to transfer an application to a Liberty static cluster
# managed by a collective controller.
# 
# The first positional parameter is the application war file to transfer.
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
# ex. jython transferAppToCluster.py /home/user/apps/myApplication.war --clusterName=cluster1 --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2 
#

import os
import sys
import traceback

from restConnector import JMXRESTConnector
import wlp_arguments as arguments
from wlp_arguments import MBeanArgs
import wlp_cluster as cluster
import wlp_serverConfig as server

import java.net.URLEncoder
import java.lang.Throwable

# Arguments specifying which cluster to use
CLUSTER_NAME = '--clusterName'

# Subclass of command line arguments for transferAppToCluster
class TransferAppToClusterArgs(MBeanArgs):

  # TransferAppToClusterArgs constructor 
  def __init__(self):
    # Make the list of value arguments that we accept
    valueParms = [CLUSTER_NAME]
    valueParms += arguments.MBEAN_VALUE_PARMS
    MBeanArgs.__init__(self, 1, arguments.STANDARD_KEYWORD_PARMS, valueParms)

  # Obtains our usage string
  def getUsage(self):
    usageString = MBeanArgs.getUsage(self) + \
                  CLUSTER_NAME + "=clusterName "
    return usageString

  # Print usage of this command
  def printUsage(self):
    print "Usage: jython transferAppToCluster.py /home/user/apps/myApplication.war " + self.getUsage()

  # Print required options
  def printRequiredHelp(self):
    print CLUSTER_NAME + "= The name of the cluster to transfer the application to"
    print
    MBeanArgs.printRequiredHelp(self)


  # Prints help information for optional args
  def printOptionalHelp(self):
    MBeanArgs.printOptionalHelp(self)

  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Used to transfer an application to a static cluster manged by a collective"
    print "controller.  The collective controller is also referred to as the"
    print "\"routing server\" in some messages."
    print
    print "This action will push the application file to all cluster members"
    print "Ensure that the remote application members directories are"
    print "configured to be writable by the filetransfer operations."
    print "    <remoteFileAccess>"
    print "        <writeDir>${server.config.dir}</writeDir>"
    print "    </remoteFileAccess>"
    print
    MBeanArgs.printHelp(self)
    print
    print "Example: jython transferAppToCluster.py /home/user/apps/myApplication.war -clusterName=cluster1 --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2 "
    
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

if __name__ == '__main__':
  argParser = TransferAppToClusterArgs()
  if (argParser.parse(sys.argv) == True):
    try:
      appPath = argParser.getPositional(0)

      if (os.path.exists(appPath) == False):
        raise IOError("Cannot transfer specified application, file does not exist: " + str(appPath))
      if (os.path.isfile(appPath) == False):
        raise IOError("Cannot transfer specified application, path is not a file: " + str(appPath))

      # Connect to the collective controller
      JMXRESTConnector.trustStore = argParser[arguments.TRUST_STORE]
      JMXRESTConnector.trustStorePassword = argParser[arguments.TRUST_STORE_PASSWORD]
    
      connector = JMXRESTConnector()
      connector.connect(argParser[arguments.HOSTNAME], 
                        int(argParser[arguments.PORT]), 
                        argParser[arguments.USERNAME],
                        argParser[arguments.PASSWORD])
      mconnection = connector.getMBeanServerConnection()

      # Get a list of the cluster members for the specified cluster.
      clusterManager = cluster.manager(mconnection)
      memberList = clusterManager.listMembers(argParser[CLUSTER_NAME])

      if ((memberList == None) or (len(memberList) == 0)):
        print "The cluster " + argParser[CLUSTER_NAME] + " did not contain any members"
      else:
        print ""
        # List of servers that had problems
        problemMembers = []

        for member in memberList:
          try:
            # The cluster manager returns member information in the form
            # host,userdir,servername.  Parse out those three parts.
            serverInfo = member.split(",")
            if (len(serverInfo) != 3):
              # If the cluster manager returned badly formed data, just skip
              # the bad member and continue.
              print "The cluster manager MBean returned an incorrectly formatted member name: " + str(member)
            else:
              # Get a new connection to the MBean server for this member.
              serverConnection = connector.getMBeanServerConnection()
              serverConfig = server.config(mconnection, serverInfo[0],
                                           serverInfo[1], serverInfo[2])

              # Push the application file out
              print "Pushing the application to server " + member
              serverConfig.pushApp(appPath)
          except java.lang.Throwable, t:
            print "An exception was caught while processing member " + member
            if (arguments.DEBUG not in argParser):
              print t.toString()
            else:
              t.printStackTrace()
            problemMembers.append(member)
          except Exception, e:
            print "A python exception was caught while processing member " + member
            if (arguments.DEBUG not in argParser):
              print str(e)
            else:
              print traceback.format_exc()
            problemMembers.append(member)
          print ""

        # Let the user know if there were problems.
        if (len(problemMembers) > 0):
          print "The operation failed on the following members [host,userdir,name]:"
          for member in problemMembers:
            print str(member)  

    except java.lang.Throwable, t:
      print "An exception was caught while processing the transferAppToCluster command"
      if (arguments.DEBUG not in argParser):
        print t.toString()
      else:
        t.printStackTrace()
    except Exception, e:
      print "A python exception was caught while processing the transferAppToCluster command"
      if (arguments.DEBUG not in argParser):
        print e
      else:
        print traceback.format_exc()
