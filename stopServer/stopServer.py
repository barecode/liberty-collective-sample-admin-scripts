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
# stopServer.py
#
# Stops a server with the given host name, usr directory, and server name.  
# A connection is made to the collective controller located at the given host 
# and port, and the request to stop the server is passed to the ServerCommandMBean.
# Note the server host name and collective controller host name are specified
# separately so they can be different from one another.
# This script can not be used to stop the controller that you are connecting to.
#
# 
# Required parameters:
# --serverName= The name of the member server to stop.
# --serverHost= The host name where the collective member is installed.
# --serverUsrdir= The usr directory where the collective member is installed.
# --truststore= The path to the trust store to be used when establishing
#               a connection to the collective controller.
# --truststorePassword= The password for the truststore specified by 
#                       --truststore
# --host= The host name where the collective controller is running.
# --port= The https port where the collective controller is listening.
# --user= The user name to use when connecting to the collective controller.
# --password= The password to use when connecting to the collective controller.
# 
# Optional parameters:
# --help= Displays help text.
# --debug= Displays additional details when an error occurs.
#
# ex. jython stopServer.py --serverName=member1 --serverHost=myhost.austin.ibm.com --serverUsrdir=/wlp/usr --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2 [--options="--clean --include=someValue"]
#

import sys

from restConnector import JMXRESTConnector
import wlp_arguments as arguments
from wlp_arguments import MBeanArgs
import wlp_server as server

import java.lang.Throwable

OPTIONS="--options"

## Arguments specifying the host where the member server is located.
SERVER_NAME = '--serverName'
SERVER_HOST = '--serverHost'
SERVER_USRDIR = '--serverUsrdir'

# Subclass of command line arguments for stopServer
class StopServerArgs(MBeanArgs):

  # StopServerArgs constructor 
  def __init__(self):
    valueParams = [SERVER_NAME, SERVER_HOST, SERVER_USRDIR]
    valueParams += arguments.MBEAN_VALUE_PARMS
    optional_parms=[OPTIONS]
    MBeanArgs.__init__(self, 0, arguments.STANDARD_KEYWORD_PARMS, valueParams, optional_parms)
  
  # Obtains our usage string
  def getUsage(self):
    usageString = SERVER_NAME + "=serverName " + \
                  SERVER_HOST + "=host " + \
                  SERVER_USRDIR + "=usrdir " + \
                  MBeanArgs.getUsage(self) + \
                  "[" + OPTIONS + "=\"options list\"]"
    return usageString

  # Print usage of this command
  def printUsage(self):
    print 
    print "Usage: jython stopServer.py " + self.getUsage()
    

  # Print required options
  def printRequiredHelp(self):
    print SERVER_NAME + "= The name of the member server to stop"
    print
    print SERVER_HOST + "= The host name where the collective member is installed"
    print
    print SERVER_USRDIR + "= The usr directory where the collective member is installed"
    print
    MBeanArgs.printRequiredHelp(self)

  # Prints help information for optional args 
  def printOptionalHelp(self):
    print "--options A space-delimited list of Liberty server command options.  The list must be enclosed in double quotes."
    print 

  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Used to stop a member server."
    print
    MBeanArgs.printHelp(self)
    print "Example: jython stopServer.py --serverName=member1 --serverHost=localhost --serverUsrdir=/wlp/usr --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2 --options=[\"--clean --include=someValue\"]"
 
  # Validate that the arguments are specified correctly.
  def validate(self):
    if MBeanArgs.validate(self): 
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
        return False
      else :
        # Make sure the positional parameter was specified correctly.
        positionalParm = self.getPositional(0)
      return (missingArg == None)
    else:
        return False


# Stops a server
def stopServer(trustStore, trustStorePassword, hostname, port, username,
                 password, host, usrdir, serverName, options):
    JMXRESTConnector.trustStore = trustStore
    JMXRESTConnector.trustStorePassword = trustStorePassword
    
    connector = JMXRESTConnector()
    connector.connect(hostname, port, username, password)
    mconnection = connector.getMBeanServerConnection()

    serverCommand = server.serverCommand(mconnection)
    stopServerResults = serverCommand.stop(host,usrdir,serverName,options)
    
    return stopServerResults  


argParser = StopServerArgs()
if (argParser.parse(sys.argv) == True):
  try:
    if OPTIONS in argParser:
      options= argParser[OPTIONS]
    else:
      options= None
    results= stopServer(argParser[arguments.TRUST_STORE], 
                         argParser[arguments.TRUST_STORE_PASSWORD],
                         argParser[arguments.HOSTNAME], 
                         int(argParser[arguments.PORT]), 
                         argParser[arguments.USERNAME], 
                         argParser[arguments.PASSWORD], 
                         argParser[SERVER_HOST],
                         argParser[SERVER_USRDIR],
                         argParser[SERVER_NAME],
                         options) # options
    if (arguments.DEBUG in argParser):
      print "stdErr= %s" % results.get("stdErr")
      print "stdOut= %s" % results.get("stdOut")
      print "returnCode= %s" % results.get("returnCode")
    returnCode= int(results.get("returnCode"))
    if (returnCode == 0):
    	print "Server stopped successfully"
    elif (returnCode == 1):
    	print "Server already stopped"
    else:
    	print "Server did not stop: return code = "+str(returnCode)
    exit(returnCode)
  except java.lang.Throwable, t:
    print "An exception was caught while processing the stopServer command"
    if (arguments.DEBUG not in argParser):
      print t.toString()
    else:
      t.printStackTrace()
    exit(-1)
