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
# 		This script uses the FileTransfer MBean to upload the file, hence the remoteFileAccess element must be specified in the server.xml of the server that the application will be installed.
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
# manageAppOnCluster.py
#
# Provides operations to install or uninstall an application on a
# Liberty static cluster managed by a collective controller.
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
# Either of the following:
# --install= The local path to the application to install in the cluster.
# --uninstall= The name of the application to uninstall from the cluster.
#
# Optional parameter:
# --appDir= The default location for installing apps is {server.config.dir}/apps.  You can specify
#           a different path for installing an application with this option.  If you specify a
#           relative path the script will install to ${server.config.dir}/<relative path>.
# --help= Displays help text.
# --debug= Displays additional details when an error occurs.

import sys
import time
from os.path import basename
import os
import shutil
import traceback

from restConnector import JMXRESTConnector
import wlp_arguments as arguments
from wlp_arguments import MBeanArgs
import wlp_cluster as cluster
import wlp_serverConfig as server

import java.net.URLEncoder
import java.lang.Throwable
from javax.management import ObjectName

# The JMX ObjectName of the routing context MBean
ROUTING_CONTEXT_MBEAN_OBJECT_NAME = "WebSphere:feature=collectiveController,type=RoutingContext,name=RoutingContext"

# The JMX ObjectName of the file transfer MBean
FILE_TRANSFER_MBEAN_OBJECT_NAME = "WebSphere:feature=restConnector,type=FileTransfer,name=FileTransfer"

                     
# ========================================================================
# The following arguments will be used for installing/uninstalling
# applications using the manageAppOnCluster script
# ========================================================================

# Argument specifying the local path to the application to install on the
# cluster
INSTALL = '--install'

# Argument specifying the name of the application to uninstall from the
# cluster
UNINSTALL = '--uninstall'

# Argument specifying the server app directory to install to or uninstall from
APP_DIR = '--appDir'

# Argument specifying which cluster to use
CLUSTER_NAME = '--clusterName'

# Subclass of command line arguments
class manageAppOnClusterArgs(MBeanArgs):

  # StartClusterArgs constructor 
  def __init__(self):
    valueParams = [INSTALL, UNINSTALL, CLUSTER_NAME]
    valueParams += arguments.MBEAN_VALUE_PARMS
    optionalParams = [APP_DIR]
    MBeanArgs.__init__(self, 0, arguments.STANDARD_KEYWORD_PARMS, valueParams, optionalParams)

  # Print usage of this command
  def printUsage(self):
    print "Usage: jython manageAppOnCluster.py action --clusterName=clusterName [--appDir=/home/user/apps]  " + self.getUsage()


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
    print APP_DIR + " The server app directory to install to or uninstall from."
    print self.printHelpPad(APP_DIR) + "By default, this will install into ${server.config.dir}/apps"
    print self.printHelpPad(APP_DIR) + "The path can be absolute or relative. Relative paths are"
    print self.printHelpPad(APP_DIR) + "relative to the ${server.config.dir}."
  
  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Used to install or uninstall an application on a cluster."
    print "This action will push the file to all cluster members, and modify"
    print "the server.xml of each cluster member to include the application"
    print "configuration. Ensure that the remote application directory is"
    print "configured to be writable by the filetransfer operations."
    print "    <remoteFileAccess>"
    print "        <writeDir>${server.config.dir}</writeDir>"
    print "    </remoteFileAccess>"
    print
    print "Actions:"
    print
    print INSTALL + " The path in the local file system to the application"
    print self.printHelpPad(INSTALL) + "to be installed within the cluster"
    print
    print UNINSTALL + " The name of the application to uninstall from the cluster"
    print
    MBeanArgs.printHelp(self)
    print
    print "Install example: jython manageAppOnCluster.py --install=/home/user/apps/myApplication.war --clusterName=cluster1 --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2"
    print
    print "Uninstall example: jython manageAppOnCluster.py --uninstall=myApplication.war --clusterName=cluster1 --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2"
    
  # Validate that the arguments are specified correctly.
  def validate(self):
    if MBeanArgs.validate(self): 
      if (INSTALL not in self and UNINSTALL not in self):
        print
        print "Please specify whether to install or uninstall an application"
        self.printUsage()
        return False
      elif (CLUSTER_NAME not in self):
        print
        print "The following required argument is missing: " + CLUSTER_NAME
        self.printUsage()
        return False
      else :
        return True
    else:
        return False

def uploadApp(trustStore, trustStorePassword, mconnection, localPathToApp, host, userdir, server, remoteAppDir, appFile) :

    # Decorate the mbean connection with the routing information for the
    # supplied server.
    jstring = "java.lang.String"
    routingCtxObjectName = ObjectName(ROUTING_CONTEXT_MBEAN_OBJECT_NAME)
    routingCtxObj = mconnection.invoke(routingCtxObjectName,
                                                "assignServerContext",
                                                [host, userdir, server],
                                                [jstring, jstring, jstring])
    if (routingCtxObj != True):
      raise EnvironmentError("Error creating routing context to target server.  The return value from invoke was: " + str(routingCtxObj))

    objectName = ObjectName(FILE_TRANSFER_MBEAN_OBJECT_NAME)
    mconnection.invoke(objectName, "uploadFile", 
                       [localPathToApp, remoteAppDir + "/" + appFile, False],
                       ["java.lang.String", "java.lang.String", "boolean"])
    
        
        
def removeApp(trustStore, trustStorePassword, mconnection, host, userdir, server, remoteAppDir, appFile) :

    # Decorate the mbean connection with the routing information for the
    # supplied server.
    jstring = "java.lang.String"
    routingCtxObjectName = ObjectName(ROUTING_CONTEXT_MBEAN_OBJECT_NAME)
    routingCtxObj = mconnection.invoke(routingCtxObjectName,
                                                "assignServerContext",
                                                [host, userdir, server],
                                                [jstring, jstring, jstring])
    if (routingCtxObj != True):
      raise EnvironmentError("Error creating routing context to target server.  The return value from invoke was: " + str(routingCtxObj))

    objectName = ObjectName(FILE_TRANSFER_MBEAN_OBJECT_NAME)
    mconnection.invoke(objectName, "deleteFile", 
                       [remoteAppDir + "/" + appFile],
                       ["java.lang.String"])

        
if __name__ == '__main__':
    argParser = manageAppOnClusterArgs()
    if (argParser.parse(sys.argv) == True):
      if ((INSTALL in argParser and ".war" not in argParser[INSTALL]) or (UNINSTALL in argParser and ".war" not in argParser[UNINSTALL])):
        print "The specified application type is not supported. Please specify a .war application"
      else:
        if (INSTALL in argParser):
          localAppPath = argParser[INSTALL]
        elif (UNINSTALL in argParser):
          localAppPath = argParser[UNINSTALL]
        appFile = os.path.basename(localAppPath)
        appName = os.path.splitext(appFile)[0]
        remoteAppDir = "${server.config.dir}/apps"
        if (APP_DIR in argParser):
          remoteAppDir = argParser[APP_DIR]
          if (os.path.dirname(remoteAppDir) == ""):
            remoteAppDir = "${server.config.dir}/"+str(remoteAppDir)

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
            # List of servers that had problems
            problemMembers = []
            configPath = os.getcwd()

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
                        host = str(serverInfo[0])
                        userDir = str(serverInfo[1])
                        serverName = str(serverInfo[2])
                        # Get a new connection to the MBean server for this member.
                        serverConnection = connector.getMBeanServerConnection()
                        serverConfig = server.config(mconnection, host,
                                           userDir, serverName)

                        # Create a directory for the member server's configuration.
                        pathToServerConfig = configPath + os.sep + "manageAppOnCluster_tmp" + os.sep + serverName
                            
                        if (os.path.exists(pathToServerConfig) == False):
                            os.makedirs(pathToServerConfig)
                        
                        serverConfig.get(pathToServerConfig)
                        f = open(pathToServerConfig + os.sep + "server.xml", 'r')
                        configLines = []
                        
                        if (INSTALL in argParser):
                            print "Uploading application " + str(appFile) + " to "+host+","+userDir+","+serverName
                            # INSTALL APPLICATION
                            # Get the app name for remote file naming purposes
                            uploadApp(argParser[arguments.TRUST_STORE], 
                                    argParser[arguments.TRUST_STORE_PASSWORD],
                                    mconnection,
                                    localAppPath,
                                    host,
                                    userDir,
                                    serverName,
                                    remoteAppDir,
                                    appFile)
                                    
                            print "Updating server config for "+host+","+userDir+","+serverName
                            line = f.readline()
                            applicationWritten = False
                            while line :
                                # Check if application has already been written to xml to avoid duplication
                                if("application" in line and "name=\""+appName+"\"" in line and "location=\""+remoteAppDir+"/"+appFile+"\"" in line):
                                    applicationWritten = True
                                if("</server>" in line and applicationWritten == False):
                                    configLines.append("\t<application name=\""+appName+"\" location=\""+remoteAppDir+"/"+appFile+"\"/>\n")
                                    
                                configLines.append(line)
                                line = f.readline()
                            
                             
                        elif (UNINSTALL in argParser):
                            # UNINSTALL APPLICATION 
                            
                            print "Removing application " + str(appFile) + " from "+host+","+userDir+","+serverName
                            removeApp(argParser[arguments.TRUST_STORE], 
                                      argParser[arguments.TRUST_STORE_PASSWORD],
                                      mconnection,
                                      host,
                                      userDir,
                                      serverName,
                                      remoteAppDir,
                                      appFile)
                                      
                            print "Updating server config for "+host+","+userDir+","+serverName
                            line = f.readline()
                            applicationWritten = False
                            while line :
                                if("\napplication" not in line and "name=\""+appName+"\"" not in line and "location=\""+remoteAppDir+"/"+appFile+"\"" not in line):
                                    configLines.append(line)
                                line = f.readline()
                             
                        f.close()
                        # Jython known problem using os.remove module on windows
                        # it will give error ==> unlink(): an unknown error occuredc:\wlp\bin\manageAppOnCluster_tmp\server.xml
                        # It only works for the first member, subsequent member will fail with error above
                        #os.remove(pathToServerConfig + os.sep + "server.xml")
                        
                        fw = open(pathToServerConfig + os.sep + "server.xml", 'w')
                        # Write the new file content
                        for line in configLines :
                            fw.write(line)
                        fw.close()
                        serverConfig.put(pathToServerConfig)
                        
                        print "Complete"
                       
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
                        problemMembers.append()
        
            shutil.rmtree(configPath + os.sep + "manageAppOnCluster_tmp", True)
            # Let the user know if there were problems.
            if (len(problemMembers) > 0):
                print ""
                print "The operation was not performed on the following members [host,userdir,name]:"
                for member in problemMembers:
                    print str(member) 
                    
                    
                    
