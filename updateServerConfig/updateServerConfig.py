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
# updateServerConfig.py
#
# Provides operations to retrieve and update the server.xml file for a 
# Liberty collectiveMember server managed by a collective controller.
# 
# The first positional parameter is either "get" or "put".  When the parameter
# is "get", the server.xml for the target server will be retrieved into the
# local file system.  When the parameter is "put", the server.xml will be
# pushed to the server from the local file server.  The typical usage of this
# script will be to retrieve the server.xml using "get", update it using a
# test editor, and replace it using "put".
#
# The configuration files are obtained from the collective controller.  The
# collective controller is also referred to as the "routing server" in some
# messages produced by the JMX runtime.
#
# Required parameters:
# --serverName= The name of the server which is installed on the host and 
#               usrdir described by serverHost and serverUsrdir, and whose
#               server.xml is to be modified.
# --serverHost= The host name where the collectiveMember is installed.
# --serverUsrdir= The usr directory where the collectiveMember is installed.
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
# --localDir= The name of a directory on the local machine where the server.xml
#             can be stored.  If this parameter is not supplied, the current
#             directory will be used.
#
# ex. jython updateServerConfig.py get --serverName=server1 --serverHost=localhost --serverUsrdir=/wlp/usr --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2 --localDir=/home/user/config/server1
#

import os
import sys
import traceback

from restConnector import JMXRESTConnector
import wlp_arguments as arguments
from wlp_arguments import MBeanArgs
import wlp_serverConfig as server

import java.lang.Throwable

# Arguments specifying the host where the member server is located.
SERVER_NAME = '--serverName'
SERVER_HOST = '--serverHost'
SERVER_USRDIR = '--serverUsrdir'

# Argument specifying the directory on the local machine where the configuration
# files (server.xml) should be stored on a get, and read from on a put.
LOCAL_DIR = '--localDir'

# Subclass of command line arguments for updateServerConfig
class UpdateServerConfigArgs(MBeanArgs):
  # UpdateServerConfigArgs constructor 
  def __init__(self):
    # Make the list of value arguments that we accept
    valueParms = [SERVER_NAME, SERVER_HOST, SERVER_USRDIR, LOCAL_DIR]
    valueParms += arguments.MBEAN_VALUE_PARMS
    MBeanArgs.__init__(self, 1, arguments.STANDARD_KEYWORD_PARMS, valueParms)

  # Obtains our usage string
  def getUsage(self):
    usageString = SERVER_NAME + "=serverName " + \
                  SERVER_HOST + "=host " + \
                  SERVER_USRDIR + "=usrdir " + \
                  MBeanArgs.getUsage(self) + \
                  "[" + LOCAL_DIR + "=directory]"
    return usageString

  # Print usage of this command
  def printUsage(self):
    print "Usage: jython updateServerConfig.py operation " + self.getUsage()

  # Print required options
  def printRequiredHelp(self):
    print SERVER_NAME + "= The name of the server which is installed on the host and"
    print self.printHelpPad(SERVER_NAME) + "usrdir described by serverHost and serverUsrdir, and whose"
    print self.printHelpPad(SERVER_NAME) + "server.xml is to be modified."
    print
    print SERVER_HOST + "= The host name where the collectiveMember is installed."
    print
    print SERVER_USRDIR + "= The usr directory where the collectiveMember is installed."
    print
    MBeanArgs.printRequiredHelp(self)


  # Prints help information for optional args
  def printOptionalHelp(self):
    MBeanArgs.printOptionalHelp(self)
    print
    print LOCAL_DIR + " The name of a directory on the local machine where the server.xml"
    print self.printHelpPad(LOCAL_DIR) + "can be stored.  If this parameter is not supplied, the current"
    print self.printHelpPad(LOCAL_DIR) + "directory will be used."

  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Used to modify the configuration (server.xml) for a server manged by the"
    print "collective controller.  The collective controller is also referred to as the "
    print "\"routing server\" in some messages.  The operation can be \"get\" or \"put\":"
    print
    print "get - Obtain the server.xml and store it into the directory specified"
    print self.printHelpPad("get -") + "by " + LOCAL_DIR 
    print
    print "put - Update the server.xml on the server with the copy obtained from"
    print self.printHelpPad("put -") + "the directory specified by " + LOCAL_DIR
    print "This action will push the server.xml file to the server"
    print "Ensure that the remote server directory is"
    print "configured to be writable by the filetransfer operations. e.g."
    print "    <remoteFileAccess>"
    print "        <writeDir>${server.config.dir}/</writeDir>"
    print "    </remoteFileAccess>"
    print
    MBeanArgs.printHelp(self)
    print
    print "Example: jython updateServerConfig.py get --serverName=server1 --serverHost=localhost --serverUsrdir=/wlp/usr --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2 --localDir=/tmp/liberty/config/defaultServer"
    
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
        if ((positionalParm != "get") and (positionalParm != "put")):
          print "The operation must be \"get\" or \"put\" "
          self.printUsage()
          missingArg = True

      return (missingArg == None)
    else:
      return False

if __name__ == '__main__':
  argParser = UpdateServerConfigArgs()
  if (argParser.parse(sys.argv) == True):
    try:
      JMXRESTConnector.trustStore = argParser[arguments.TRUST_STORE]
      JMXRESTConnector.trustStorePassword = argParser[arguments.TRUST_STORE_PASSWORD]
    
      connector = JMXRESTConnector()
      connector.connect(argParser[arguments.HOSTNAME], 
                        int(argParser[arguments.PORT]), 
                        argParser[arguments.USERNAME],
                        argParser[arguments.PASSWORD])
      mconnection = connector.getMBeanServerConnection()

      serverConfig = server.config(mconnection, argParser[SERVER_HOST],
                                   argParser[SERVER_USRDIR],
                                   argParser[SERVER_NAME])

      if (LOCAL_DIR in argParser):
        configPath = argParser[LOCAL_DIR]
      else:
        configPath = os.getcwd()

      if (argParser.getPositional(0) == "get"):
        serverConfig.get(configPath)
      else:
        serverConfig.put(configPath)

    except java.lang.Throwable, t:
      print "An exception was caught while processing the updateServerConfig command"
      if (arguments.DEBUG not in argParser):
        print t.toString()
      else:
        t.printStackTrace()
    except Exception, e:
      print "A python exception was caught while processing the updateServerConfig command"
      if (arguments.DEBUG not in argParser):
        print e
      else:
        print traceback.format_exc()
