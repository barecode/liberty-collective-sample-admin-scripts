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
# transferAppToServer.py
#
# Provides operations to transfer an application to a Liberty collective member.
# managed by a collective controller.
# 
# The first positional parameter is the application to transfer.
#
# Required parameters:
# --serverName= The name of the member server which is installed on the host and 
#               usrdir described by serverHost and serverUsrdir.
# --serverHost= The host name where the collective member is installed.
# --serverUsrdir= The usr directory where the collective member is installed.
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
# ex. jython transferAppToServer.py /opt/apps/myApplication.war --serverName=member1 --serverHost=localhost --serverUsrdir=/wlp/usr --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2 
#

import os
import sys
import traceback

from restConnector import JMXRESTConnector
import wlp_arguments as arguments
from wlp_arguments import MBeanArgs
import wlp_serverConfig as server

import java.net.URLEncoder
import java.lang.Throwable

# Arguments specifying which member server to use
SERVER_NAME = '--serverName'
SERVER_HOST = '--serverHost'
SERVER_USRDIR = '--serverUsrdir'

# Subclass of command line arguments for transferAppToServer
class TransferAppToServerArgs(MBeanArgs):

  # TransferAppToServerArgs constructor 
  def __init__(self):
    # Make the list of value arguments that we accept
    valueParms = [SERVER_NAME, SERVER_HOST, SERVER_USRDIR]
    valueParms += arguments.MBEAN_VALUE_PARMS
    MBeanArgs.__init__(self, 1, arguments.STANDARD_KEYWORD_PARMS, valueParms)

  # Obtains our usage string
  def getUsage(self):
    usageString = SERVER_NAME + "=serverName " + \
                  SERVER_HOST + "=host " + \
                  SERVER_USRDIR + "=usrdir " + \
                  MBeanArgs.getUsage(self) 
    return usageString

  # Print usage of this command
  def printUsage(self):
    print "Usage: jython transferAppToServer.py path/to/app " + self.getUsage()

  # Print required options
  def printRequiredHelp(self):
    print SERVER_NAME + "= The name of the server to transfer the application to "
    print
    print SERVER_HOST + "= The host name where the collective member is installed"
    print
    print SERVER_USRDIR + "= The usr directory where the collective member is installed"
    print 
    MBeanArgs.printRequiredHelp(self)


    
  # Prints help information for optional args
  def printOptionalHelp(self):
    MBeanArgs.printOptionalHelp(self)

  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Used to transfer an application to a member server manged by a collective"
    print "controller.  The collective controller is also referred to as the"
    print "\"routing server\" in some messages."
    print
    print "This action will push the application file to the member server"
    print "Ensure that the remote application directory is "
    print "configured to be writable by the filetransfer operations. e.g."
    print "    <remoteFileAccess>"
    print "        <writeDir>${server.config.dir}/</writeDir>"
    print "    </remoteFileAccess>"
    print
    MBeanArgs.printHelp(self)
    print
    print "Example: jython transferAppToServer.py path/to/app --serverName=member1 --serverHost=localhost --serverUsrdir=/wlp/usr --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2"
    
  # Validate that the arguments are specified correctly.
  def validate(self):
    # First validate the MBean arguments
    if MBeanArgs.validate(self): 
      # Then validate update server config arguments
      missingArg = None
      if (SERVER_NAME not in self):
        missingArg = SERVER_NAME
      elif (SERVER_HOST not in self):
        missingArg = SERVER_HOST
      elif (SERVER_USRDIR not in self):
        missingArg = SERVER_USRDIR

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
  argParser = TransferAppToServerArgs()
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

      # Get a new connection to the MBean server for this member.
      serverConnection = connector.getMBeanServerConnection()
      serverConfig = server.config(mconnection, argParser[SERVER_HOST],
                                   argParser[SERVER_USRDIR],
                                   argParser[SERVER_NAME])  

      # Push the application file out
      print "Pushing the application to server " +argParser[SERVER_HOST]+","+argParser[SERVER_USRDIR]+","+argParser[SERVER_NAME]
      serverConfig.pushApp(appPath)
      
    except java.lang.Throwable, t:
      print "An exception was caught while processing the transferAppToServer command"
      if (arguments.DEBUG not in argParser):
        print t.toString()
      else:
        t.printStackTrace()
    except Exception, e:
      print "A python exception was caught while processing the transferAppToServer command"
      if (arguments.DEBUG not in argParser):
        print e
      else:
        print traceback.format_exc()
