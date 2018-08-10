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
# updateClusterConfig.py
#
# Provides operations to retrieve and update the server.xml files for a 
# Liberty static cluster managed by a collective controller.
# 
# The first positional parameter is either "get" or "put".  When the parameter
# is "get", the server.xml for each server in the target cluster will be 
# retrieved into the local file system.  When the parameter is "put", the 
# server.xml for each server will be pushed from the local directory.  The 
# typical usage of this script will be to retrieve the server.xml using "get", 
# update it using a test editor, and replace it using "put".
#
# The configuration files are obtained from the collective controller.  The
# collective controller is also referred to as the "routing server" in some
# messages produced by the JMX runtime.
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
# --clusterName= The name of the static cluster to operate on.
# 
# Optional parameters:
# --help= Displays help text.
# --debug= Displays additional details when an error occurs.
# --localDir= The name of a directory on the local machine where the server.xml
#             files can be stored.  If this parameter is not supplied, the 
#             current directory will be used.  A subdirectory will be created
#             for each cluster member, and the server.xml will be stored inside
#             that directory.
#
# ex. jython updateClusterConfig.py get --clusterName=cluster1 --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2 --localDir=/home/user/config/cluster1
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

# Argument specifying the directory on the local machine where the configuration
# files (server.xml) should be stored on a get, and read from on a put.
LOCAL_DIR = '--localDir'

# Subclass of command line arguments for updateClusterConfig
class UpdateClusterConfigArgs(MBeanArgs):

  # UpdateClusterConfigArgs constructor 
  def __init__(self):
    # Make the list of value arguments that we accept
    valueParms = [CLUSTER_NAME, LOCAL_DIR]
    valueParms += arguments.MBEAN_VALUE_PARMS
    MBeanArgs.__init__(self, 1, arguments.STANDARD_KEYWORD_PARMS, valueParms)

  # Obtains our usage string
  def getUsage(self):
    usageString = CLUSTER_NAME + "=clusterName " + \
                  MBeanArgs.getUsage(self) + \
                  "[" + LOCAL_DIR + "=directory]"
    return usageString

  # Print usage of this command
  def printUsage(self):
    print "Usage: jython updateClusterConfig.py operation " + self.getUsage()

  # Print required options
  def printRequiredHelp(self):
    print CLUSTER_NAME + "= The name of the cluster whose server.xml files are to "
    print self.printHelpPad(CLUSTER_NAME) + "be modified."
    print
    MBeanArgs.printRequiredHelp(self)


  # Prints help information for optional args
  def printOptionalHelp(self):
    MBeanArgs.printOptionalHelp(self)
    print
    print LOCAL_DIR + " The name of a directory on the local machine where the server.xml"
    print self.printHelpPad(LOCAL_DIR) + "files can be stored.  If this parameter is not supplied, the"
    print self.printHelpPad(LOCAL_DIR) + "current directory will be used.  A subdirectory will be"
    print self.printHelpPad(LOCAL_DIR) + "created for each cluster member, and the server.xml will be"
    print self.printHelpPad(LOCAL_DIR) + "stored inside it."

  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Used to modify the configuration (server.xml) for a static cluster manged by "
    print "the collective controller.  The collective controller is also referred to as "
    print "the \"routing server\" in some messages.  The operation can be \"get\" or"
    print  "\"put\":"
    print
    print "get - Obtain the server.xml files and store it into the directory specified"
    print self.printHelpPad("get -") + "by " + LOCAL_DIR 
    print
    print "put - Update the server.xml files on the server with the copy obtained from"
    print self.printHelpPad("put -") + "the directory specified by " + LOCAL_DIR
    print "This action will push the server.xml file to all cluster members"
    print "Ensure that the remote members directories are"
    print "configured to be writable by the filetransfer operations."
    print "    <remoteFileAccess>"
    print "        <writeDir>${server.config.dir}</writeDir>"
    print "    </remoteFileAccess>"
    print
    MBeanArgs.printHelp(self)
    print
    print "Example: jython updateClusterConfig.py get --clusterName=cluster1 --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2  --localDir=/tmp/liberty/config/cluster1"
    
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
        if ((positionalParm != "get") and (positionalParm != "put")):
          print "The operation must be \"get\" or \"put\" "
          self.printUsage()
          missingArg = True

      return (missingArg == None)
    else:
      return False

if __name__ == '__main__':
  argParser = UpdateClusterConfigArgs()
  if (argParser.parse(sys.argv) == True):
    try:
      # Make sure that the path for the configuration files exists in the
      # local file system.
      if (LOCAL_DIR in argParser):
        configPath = argParser[LOCAL_DIR]
      else:
        configPath = os.getcwd()

      if ((os.path.exists(configPath) == False) or 
          (os.path.isdir(configPath) == False)):
        raise IOError("Cannot store cluster configuration to the supplied path: " + str(configPath))

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

              # Create a directory for the member server's configuration.
              encodedUserdir = java.net.URLEncoder.encode(serverInfo[1], "UTF-8")
              pathToServerConfig = configPath + os.sep + serverInfo[0] + \
                          os.sep + encodedUserdir + os.sep + serverInfo[2]
              if (os.path.exists(pathToServerConfig) == False):
                os.makedirs(pathToServerConfig)

              # Put or get the configuration file for this member server.
              if (argParser.getPositional(0) == "get"):
                print "Getting configuration for server " + member
                serverConfig.get(pathToServerConfig)
              else:
                print "Putting configuration for server " + member
                serverConfig.put(pathToServerConfig)
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
          print "The operation was not performed on the following members [host,userdir,name]:"
          for member in problemMembers:
            print str(member)  

    except java.lang.Throwable, t:
      print "An exception was caught while processing the updateClusterConfig command"
      if (arguments.DEBUG not in argParser):
        print t.toString()
      else:
        t.printStackTrace()
    except Exception, e:
      print "A python exception was caught while processing the updateClusterConfig command"
      if (arguments.DEBUG not in argParser):
        print e
      else:
        print traceback.format_exc()
