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
# 		This script uses the FileTransfer MBean to upload the file, hence the remoteFileAccess element must be specified in the server.xml.
# 		Without this you will get a file permission error when using the script.
#
#		Here is an example of a remoteFileAccess element:
#		<remoteFileAccess>
#			<writeDir>${server.config.dir}</writeDir>
#		</remoteFileAccess>
#
# 		For further information and examples for remoteFileAccess, please visit the Information Center for "WebSphere Application Server V8.5 Liberty profile" 
#		and search for "List of provided MBean" or "remoteFileAccess"
#
#

import os
import sys

import javax.management.ObjectName

from restConnector import JMXRESTConnector

# The JMX ObjectName of the routing context MBean
ROUTING_CONTEXT_MBEAN_OBJECT_NAME = "WebSphere:feature=collectiveController,type=RoutingContext,name=RoutingContext"

# The JMX ObjectName of the file transfer MBean
FILE_TRANSFER_MBEAN_OBJECT_NAME = "WebSphere:feature=restConnector,type=FileTransfer,name=FileTransfer"

# Class representing the server.xml file for the server
class config(object):
  mbeanConnection = None
  host = ""
  userdir = ""
  server = ""

  # Initialization routine
  #
  # mbeanConnection is an instance of an MBeanServer connection to the
  #   collective controller, obtained by calling the getMBeanServerConnection() 
  #   function of the JMXRESTConnector class.
  # host is the host name where the server to be operated on is located
  # userdir is the user directory where the server to be operated on is located,
  #   on the host machine described by the host parameter.
  # server is the name of the server to be operated on.  The server is located
  #   on the host machine described by the host parameter, and in the user
  #   directory described by the userdir parameter.
  def __init__(self, mbeanConnection, host, userdir, server):
    self.mbeanConnection = mbeanConnection
    self.host = host
    self.userdir = userdir
    self.server = server

    # Decorate the mbean connection with the routing information for the
    # supplied server.
    jstring = "java.lang.String"
    routingCtxObjectName = javax.management.ObjectName(ROUTING_CONTEXT_MBEAN_OBJECT_NAME)
    routingCtxObj = self.mbeanConnection.invoke(routingCtxObjectName,
                                                "assignServerContext",
                                                [host, userdir, server],
                                                [jstring, jstring, jstring])
    if (routingCtxObj != True):
      raise EnvironmentError("Error creating routing context to target server.  The return value from invoke was: " + str(routingCtxObj))

  # Obtain the server.xml for this server.
  # localFilePath is the path to a directory on the local machine where the
  #   server.xml will be downloaded to.
  def get(self, localFilePath):
    # Make sure the target directory exists
    if ((os.path.exists(localFilePath) == False) or (os.path.isdir(localFilePath) == False)):
      raise IOError("Cannot store server.xml to the supplied path: " + str(localFilePath))

    # Retrieve the server.xml, storing it in the local file system at the
    # specified location.
    jstring = "java.lang.String"
    objectName = javax.management.ObjectName(FILE_TRANSFER_MBEAN_OBJECT_NAME)
    self.mbeanConnection.invoke(objectName, "downloadFile",
                                ["${server.config.dir}/server.xml", str(localFilePath) + os.sep + "server.xml"],
                                [jstring, jstring])

  # Update the server.xml for this server.
  # localFilePath is the path to a directory on the local machine where the
  #   updated server.xml is located.  The server.xml will be uploaded to the
  #   remote server, and the server will now use this copy of the server.xml.
  def put(self, localFilePath):
    # Make sure that server.xml exists in the target location.
    if (os.path.exists(localFilePath + "/server.xml") == False):
      raise IOError("There is no server.xml in the supplied path: " + str(localFilePath))

    # Store the server.xml on the remote system.
    jstring = "java.lang.String"
    objectName = javax.management.ObjectName(FILE_TRANSFER_MBEAN_OBJECT_NAME)
    self.mbeanConnection.invoke(objectName, "uploadFile",
                                [str(localFilePath) + os.sep + "server.xml", "${server.config.dir}/server.xml", False],
                                [jstring, jstring, "boolean"])

  # Update the server.xml for this server.
  # localFilePath is the path to a directory on the local machine where the
  #   updated server.xml is located.  The server.xml will be uploaded to the
  #   remote server, and the server will now use this copy of the server.xml.
  def pushConfig(self, localFilePath):
    # Make sure that server.xml exists in the target location.
    if (os.path.exists(localFilePath) == False):
      raise IOError("There is no server.xml in the supplied path: " + str(localFilePath))

    # Store the server.xml on the remote system.
    jstring = "java.lang.String"
    objectName = javax.management.ObjectName(FILE_TRANSFER_MBEAN_OBJECT_NAME)
    self.mbeanConnection.invoke(objectName, "uploadFile",
                                [str(localFilePath), "${server.config.dir}/server.xml", False],
                                [jstring, jstring, "boolean"])

  # Push an application to this server.
  # localAppPath is the path to the local copy of the application file.
  #   The application will be uploaded to the remote server's apps directory.
  def pushApp(self, localAppPath):
    # Make sure that server.xml exists in the target location.
    if (os.path.exists(localAppPath) == False):
      raise IOError("The specified application path does not exist: " + str(localAppPath))

    appName = os.path.basename(localAppPath)
    if (appName == ""):
      raise IOError("The specified application path does not end in a file name: " + str(localAppPath))

    # Store the server.xml on the remote system.
    jstring = "java.lang.String"
    objectName = javax.management.ObjectName(FILE_TRANSFER_MBEAN_OBJECT_NAME)
    self.mbeanConnection.invoke(objectName, "uploadFile",
                                [str(localAppPath), "${server.config.dir}/apps/"+str(appName), False],
                                [jstring, jstring, "boolean"])
