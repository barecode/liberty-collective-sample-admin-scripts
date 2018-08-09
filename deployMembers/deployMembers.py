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
# deployMembers.py
#
# Provides operations to upload, join and start members for a
# running collective controller.
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
# --zipFile= The fully qualified zip file path to upload to target machine.
# --installDir= The path where member will be installed on target machine.
# --installHost= The host name of the target machine.
# --rpcUser= The rpc user of the target machine.
# --rpcUserPassword= The rpc user password of the target machine.
#
# Optional parameters:
# --help= Displays help text.
# --debug= Displays additional details when an error occurs.
#
# Usage: jython deployMembers.py --zipFile=/home/user/wlp.zip --installDir=/opt/ --installHost=targetHostName --rpcUser=Administrator --rpcUserPassword=secret --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=controllerHostName --port=9443 --user=admin --password=secret2"
#

import sys
import time
import os
from os.path import basename
import shutil
import zipfile
import javax
import jarray
import traceback

from restConnector import JMXRESTConnector
import wlp_arguments as arguments
from wlp_arguments import MBeanArgs
import wlp_serverConfig as server

import java.net.URLEncoder
import java.lang.Throwable

import java.io.File as File
import java.util.ArrayList as ArrayList
import java.util.HashMap as HashMap
import java.lang.System as System

from javax.management import ObjectName
import javax.management.openmbean.CompositeData as CompositeData
import com.ibm.websphere.jmx.connector.rest.ConnectorSettings as ConnectorSettings
import javax.management.remote.JMXConnector as JMXConnector
import com.ibm.ws.jmx.connector.client.rest.ClientProvider as ClientProvider

# The JMX ObjectName of the routing context MBean
ROUTING_CONTEXT_MBEAN_OBJECT_NAME = "WebSphere:feature=collectiveController,type=RoutingContext,name=RoutingContext"

# The JMX ObjectName of the collective registration MBean
COLLECTIVE_REGISTRATION_MBEAN_OBJECT_NAME = "WebSphere:feature=collectiveController,type=CollectiveRegistration,name=CollectiveRegistration"

# The JMX ObjectName of the file transfer MBean
FILE_TRANSFER_MBEAN_OBJECT_NAME = "WebSphere:feature=restConnector,type=FileTransfer,name=FileTransfer"

# The JMX ObjectName of the server commands MBean
SERVER_COMMANDS_MBEAN_OBJECT_NAME = "WebSphere:feature=collectiveController,type=ServerCommands,name=ServerCommands"

# Properties to build certificate creation
COLLECTIVE_TRUST_KEYSTORE_PASSWORD = "collectiveTrustKeystorePassword"

# Properties to build hostAuthInfo 
RPC_USR = "rpcUser"
RPC_USR_PWD = "rpcUserPassword"
HOST_READ_LIST = "hostReadList"
HOST_WRITE_LIST = "hostWriteList"

jstring = "java.lang.String"
jmap = "java.util.Map"
                     
# ========================================================================
# The following arguments will be used for installing/uninstalling
# applications using the deployMembers script
# ========================================================================

# Argument specifying the fully qualified local path to the zip to install
# on a host
ZIP_FILE = '--zipFile'

# Argument specifying the location to install the zip file contents
INSTALL_DIR = '--installDir'

# Argument specifying the name of the host that will have the members installed
INSTALL_HOST = '--installHost'

# Argument specifying the rpc user of the host that will have the members installed
RPC_USER = '--rpcUser'

# Argument specifying the rpc user password of the host that will have the members installed
RPC_USER_PASSWORD = '--rpcUserPassword'


# Subclass of command line arguments for startCluster
class DeployMembersArgs(MBeanArgs):

  # StartClusterArgs constructor 
  def __init__(self):
    valueParams = [ZIP_FILE, INSTALL_DIR, INSTALL_HOST, RPC_USER, RPC_USER_PASSWORD]
    valueParams += arguments.MBEAN_VALUE_PARMS
    MBeanArgs.__init__(self, 0, arguments.STANDARD_KEYWORD_PARMS, valueParams)

  # Obtains our usage string
  def getUsage(self):
    usageString = MBeanArgs.getUsage(self) + \
                  ZIP_FILE + "=path/to/zipFile " + \
                  INSTALL_DIR + "=path/to/install/on/target/machine " + \
                  INSTALL_HOST + "=targetMachineHostName " + \
                  RPC_USER + "=rpcUserOfTargetMachine " + \
                  RPC_USER_PASSWORD + "=rpcUserPasswordOfTargetMachine "
    return usageString
            
  # Print usage of this command
  def printUsage(self):
    print "Usage: jython deployMembers.py " + self.getUsage()

  # Print required options
  def printRequiredHelp(self):
    MBeanArgs.printRequiredHelp(self)
    print
    print ZIP_FILE + "= The fully qualified zip file path to upload to target machine"
    print
    print INSTALL_DIR + "= The path where member will be installed on target machine"
    print
    print INSTALL_HOST + "= The host name of the target machine"
    print
    print RPC_USER + "= The rpc user of the target machine"
    print
    print RPC_USER_PASSWORD + "= The rpc user password of the target machine"

  # Print help for this command
  def printHelp(self):
    self.printUsage()
    print ""
    print "Used to deploy a set of member servers from a zip file."
    print "The script will push the zip to the specified installHost, extract the"
    print "member servers and start them."
    print
    MBeanArgs.printHelp(self)
    print
    print "Example: jython deployMembers.py  --zipFile=/home/user/wlp.zip --installDir=/opt/ --installHost=targetHostName --rpcUser=Administrator --rpcUserPassword=secret --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=controllerHostName --port=9443 --user=admin --password=secret2"
    
  # Validate that the arguments are specified correctly.
  def validate(self):
    if MBeanArgs.validate(self): 
      if (ZIP_FILE not in self):
        print
        print "The following required argument is missing: " + ZIP_FILE
        self.printUsage()
        return False
      elif (INSTALL_DIR not in self):
        print
        print "The following required argument is missing: " + INSTALL_DIR
        self.printUsage()
        return False
      elif (INSTALL_HOST not in self):
        print
        print "The following required argument is missing: " + INSTALL_HOST
        self.printUsage()
        return False
      elif (RPC_USER not in self):
        print
        print "The following required argument is missing: " + RPC_USER
        self.printUsage()
        return False
      elif (RPC_USER_PASSWORD not in self):
        print
        print "The following required argument is missing: " + RPC_USER_PASSWORD
        self.printUsage()
        return False
      else :
        return True
    else:
        return False

                
def configureHostAccess(trustStore, trustStorePassword, mconnection, host, hostCredentialMap, newHost) :

    # Decorate the mbean connection with the routing information for the supplied server.
    routingCtxObjectName = ObjectName(ROUTING_CONTEXT_MBEAN_OBJECT_NAME)
    routingCtxObj = mconnection.invoke(routingCtxObjectName,
                                                "assignHostContext",
                                                [host],
                                                [jstring])
    if (routingCtxObj != True):
      raise EnvironmentError("Error creating routing context to target host.  The return value from invoke was: " + str(routingCtxObj))

    objectName = ObjectName(COLLECTIVE_REGISTRATION_MBEAN_OBJECT_NAME)

    methodName = "updateHost"
    if (newHost):
        methodName = "registerHost"

    mconnection.invoke(objectName, methodName, 
                       [host, hostCredentialMap],
                       [jstring, jmap])
               
    
def uploadAndExpandZip(trustStore, trustStorePassword, mconnection, host, remoteDir, localZipPath) :

    objectName = ObjectName(FILE_TRANSFER_MBEAN_OBJECT_NAME)
    mconnection.invoke(objectName, "uploadFile", 
                       [localZipPath, remoteDir + os.sep, True],
                       [jstring, jstring, "boolean"])
    
    
def isWlpZipRootDir(zipFile) :

    isWlpRoot = False
    zipFileObj = zipfile.ZipFile(zipFile,'r')

    for name in zipFileObj.namelist():
        if(name.startswith("wlp/")):
            isWlpRoot = True

    zipFileObj.close()
    return isWlpRoot

def getMembersFromZip(zipFile) :

    memberList = []
    zipFileObj = zipfile.ZipFile(zipFile,'r')
    for name in zipFileObj.namelist():
        index1 = name.find("servers/") + 8 # position after servers/
        index2 = name.find("server.xml")
        index3 = name.find("templates")
        if(index1 != -1 and index2 !=-1 and index3 == -1):
            memberList.append(name[index1:index2-1])

    zipFileObj.close()
    return memberList

            
def joinMemberServer(mconnection, host, memberUsrDir, memberName, wlpDir, trustStorePassword, hostAuthInfo) :
    
    # build credential Map
    certProps = HashMap()
    certProps.put(COLLECTIVE_TRUST_KEYSTORE_PASSWORD, trustStorePassword)

    objectName = ObjectName(COLLECTIVE_REGISTRATION_MBEAN_OBJECT_NAME)

    mconnection.invoke(objectName, "join", 
                    [host, memberUsrDir, memberName, wlpDir, trustStorePassword, certProps, hostAuthInfo],
                    [jstring, jstring, jstring, jstring, jstring, jmap, jmap])
 
    
def putNecessaryFilesToMember(mconnection, trustStorePath) :
    
    truststoreFile = File(trustStorePath)
    securityPath = truststoreFile.getParent()
    securityFile = File(securityPath)
    resourcesPath = securityFile.getParent()
    
    objectName = ObjectName(FILE_TRANSFER_MBEAN_OBJECT_NAME)
    mconnection.invoke(objectName, "uploadFile",
                      [trustStorePath, memberUsrDir + os.sep + "servers" + os.sep + member + os.sep + "resources" + os.sep + "security" + os.sep + "trust.jks", False],
                      [jstring, jstring, "boolean"])
           
    mconnection.invoke(objectName, "uploadFile",
                      [resourcesPath + os.sep + "collective" + os.sep + "collectiveTrust.jks", memberUsrDir + os.sep + "servers" + os.sep + member + os.sep + "resources" + os.sep + "collective" + os.sep + "collectiveTrust.jks", False],
                      [jstring, jstring, "boolean"])
                      
    mconnection.invoke(objectName, "uploadFile",
                      [resourcesPath + os.sep + "collective" + os.sep + "serverIdentity.jks", memberUsrDir + os.sep + "servers" + os.sep + member + os.sep + "resources" + os.sep + "collective" + os.sep + "serverIdentity.jks", False],
                      [jstring, jstring, "boolean"])
                    
def startMemberServer(trustStore, trustStorePassword, mconnection, host, memberUsrDir, serverName) :

    
    print "Starting member: host=" + host + " usrDir=" + memberUsrDir + " serverName=" + serverName 
    objectName = ObjectName(SERVER_COMMANDS_MBEAN_OBJECT_NAME)
    result = mconnection.invoke(objectName, "startServer", 
                       [host, memberUsrDir, serverName, ""],
                       [jstring, jstring, jstring, jstring])
    return result


    
if __name__ == '__main__':
    argParser = DeployMembersArgs()
    if (argParser.parse(sys.argv) == True):
        print ""
        JMXRESTConnector.trustStore = argParser[arguments.TRUST_STORE]
        JMXRESTConnector.trustStorePassword = argParser[arguments.TRUST_STORE_PASSWORD]
        installHost = argParser[INSTALL_HOST]
        
        # Connect to the collective controller
        # Using a timeout of 20 minutes for the zip file to upload and extract
        map = HashMap()
        map.put(ClientProvider.READ_TIMEOUT,20*60*1000)
        map.put(JMXConnector.CREDENTIALS,jarray.array([argParser[arguments.USERNAME],argParser[arguments.PASSWORD]],java.lang.String))
        map.put("jmx.remote.provider.pkgs","com.ibm.ws.jmx.connector.client")
        map.put(ConnectorSettings.DISABLE_HOSTNAME_VERIFICATION, True) 

        connector = JMXRESTConnector()
        connector.connect(argParser[arguments.HOSTNAME], 
                          int(argParser[arguments.PORT]), 
                          map)
        mconnection = connector.getMBeanServerConnection()

        # build hostAuthInfo Map
        installDir = argParser[INSTALL_DIR]  
        localZipPath = argParser[ZIP_FILE]
        zipFile = os.path.basename(localZipPath)
        zipName = os.path.splitext(zipFile)[0]          

        
        wlpDir = installDir
        if (isWlpZipRootDir(localZipPath)):
            wlpDir = installDir + os.sep + "wlp"

        print "The wlp dir for this deployment will be: " + wlpDir
        memberUsrDir = wlpDir + os.sep + "usr"

        memberList = getMembersFromZip(localZipPath)
     
        hostDirList = ArrayList();
        hostDirList.add(installDir)
        for member in memberList:
            hostDirList.add(installDir + os.sep + "servers" + os.sep + member + os.sep + "resources" + os.sep + "security")
            hostDirList.add(installDir + os.sep + "servers" + os.sep + member + os.sep + "resources" + os.sep + "collective")

        # Update the host with authentication credentials and file permission
        hostAuthInfo = HashMap()
        hostAuthInfo.put(RPC_USR, argParser[RPC_USER]);
        hostAuthInfo.put(RPC_USR_PWD, argParser[RPC_USER_PASSWORD]);
        hostAuthInfo.put(HOST_READ_LIST, hostDirList);
        hostAuthInfo.put(HOST_WRITE_LIST, hostDirList);

        # Register/update the host
        print "Assigning host context for: " + installHost
        try:       
            configureHostAccess(JMXRESTConnector.trustStore, 
                              JMXRESTConnector.trustStorePassword,
                              mconnection,
                              installHost,
                              hostAuthInfo,
                              True)
        except java.lang.Throwable, t:
            if (t.toString().find("has already been registered") != -1):
                print "The host has already been registered, calling updateHost instead."
                # Is a registered host, try to update it
                configureHostAccess(JMXRESTConnector.trustStore, 
                                JMXRESTConnector.trustStorePassword,
                                mconnection,
                                installHost,
                                hostAuthInfo,
                                False)
            else:
                print "An exception was caught while processing configureHostAccess."

        print "The host " + installHost + " connection information is configured."


        # Upload and expand zip file on target
        # Disable to stop duplicate uploads
        print "Loading and expanding " + zipFile + " on target machine location " + installDir
        uploadAndExpandZip(JMXRESTConnector.trustStore, 
                           JMXRESTConnector.trustStorePassword,
                           mconnection,
                           installHost,
                           installDir,
                           localZipPath)
                         
        # Start the member servers
        if ((memberList == None) or (len(memberList) == 0)):
          print "The host " + installHost + " directory " + memberDir + " did not contain any members"
        else:
          # List of servers that had problems
          problemMembers = []
                  
          print ""    
          for member in memberList:
            try:
              # Join the collective
              joinMemberServer(mconnection, 
                           installHost,
                           memberUsrDir,
                           member,
                           wlpDir,
                           JMXRESTConnector.trustStorePassword,
                           hostAuthInfo) 
              print "Member " + member + " join the collective"
              
            except java.lang.Throwable, t:          
              if (t.toString().find("has already been registered") == -1):
                print "An exception was caught while processing join member " + member
                problemMembers.append(member)
                if (arguments.DEBUG not in argParser):
                    print t.toString()
                else:
                    t.printStackTrace()
              else:
                print "Skip join operation, server " + member + " has already been registered."
                
            except Exception, e:
              print "A python exception was caught while processing member " + member
              problemMembers.append(member)
              if (arguments.DEBUG not in argParser):
                print str(e)
              else:
                print traceback.format_exc()
                         
            try:
              # Upload controller's trust.jks, collectiveTrust.jks and serverIdentity.jks files to the member
              print "Uploading needed security files to " + member
              putNecessaryFilesToMember(mconnection, JMXRESTConnector.trustStore)
                                
            except java.lang.Throwable, t:
              print "An exception was caught while processing uploadFile " + member
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
              
            try:
              # Start member
              startResult = startMemberServer(JMXRESTConnector.trustStore, 
                                JMXRESTConnector.trustStorePassword,
                                mconnection,
                                installHost,
                                memberUsrDir,
                                member)
              
              if (arguments.DEBUG in argParser):
                  print "stdErr= %s" % startResult.get("stdErr")
                  print "stdOut= %s" % startResult.get("stdOut")
                  print "returnCode= %s" % startResult.get("returnCode")
                  
              returnCode = int(startResult.get("returnCode"))
              if (returnCode == 0):
                  print "Server " + member + " started successfully"
              elif (returnCode == 1):
                  print "Server " + member + " already started"
              else:
                  print "Server did not start: return code = "+str(returnCode)
                                
            except java.lang.Throwable, t:
              print "An exception was caught while processing start member " + member
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
            for member in problemMembers:                
                print "The operation failed on the following members [" + installHost + "," + memberUsrDir + "," + member + "]"
            

