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

import sys

import javax.management.ObjectName
from restConnector import JMXRESTConnector

# The JMX ObjectName of the server command MBean
MBEAN_OBJECT_NAME = "WebSphere:feature=collectiveController,type=ServerCommands,name=ServerCommands"

# Class representing the server commands.
class serverCommand(object):
  mbeanConnection = None
  
  # Initialization routine
  #
  # mbeanConnection is an instance of an MBeanServer connection, obtained by
  # calling the getMBeanServerConnection() function of the
  # JMXRESTConnector class.
  def __init__(self, mbeanConnection):
    self.mbeanConnection = mbeanConnection

  # Start the server
  def start(self,host,userdir,serverName,options):
    objectName = javax.management.ObjectName(MBEAN_OBJECT_NAME)
    startServerResults= self.mbeanConnection.invoke(objectName, "startServer", [host,userdir,serverName,options], ["java.lang.String","java.lang.String","java.lang.String","java.lang.String"])    
    return startServerResults

  # Stop the server
  def stop(self, host,userdir,serverName,options):
    objectName = javax.management.ObjectName(MBEAN_OBJECT_NAME)   
    stopServerResults = self.mbeanConnection.invoke(objectName, "stopServer", [host,userdir,serverName,options], ["java.lang.String","java.lang.String","java.lang.String","java.lang.String"])   
    return stopServerResults

