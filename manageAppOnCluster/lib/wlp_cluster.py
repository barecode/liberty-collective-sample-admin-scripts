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

# The JMX ObjectName of the cluster manager MBean
MBEAN_OBJECT_NAME = "WebSphere:feature=collectiveController,type=ClusterManager,name=ClusterManager"

# Class representing the cluster manager.
class manager(object):
  mbeanConnection = None
  
  # Initialization routine
  #
  # mbeanConnection is an instance of an MBeanServer connection, obtained by
  # calling the getMBeanServerConnection() function of the
  # JMXRESTConnector class.
  def __init__(self, mbeanConnection):
    self.mbeanConnection = mbeanConnection

  # Start the cluster
  def start(self, clusterName, options):
    objectName = javax.management.ObjectName(MBEAN_OBJECT_NAME)
    
    startClusterResults = self.mbeanConnection.invoke(
      objectName, "startCluster", [clusterName, options], ["java.lang.String", "java.lang.String"])
    
    return startClusterResults

  # Stop the cluster
  def stop(self, clusterName, options):
    objectName = javax.management.ObjectName(MBEAN_OBJECT_NAME)
    
    stopClusterResults = self.mbeanConnection.invoke(
      objectName, "stopCluster", [clusterName, options], ["java.lang.String", "java.lang.String"])
    
    return stopClusterResults

  # Get a member listing
  def listMembers(self, clusterName):
    objectName = javax.management.ObjectName(MBEAN_OBJECT_NAME)
    
    members = self.mbeanConnection.invoke(
      objectName, "listMembers", [clusterName], ["java.lang.String"])
    
    return members

  # List the cluster names
  def listClusterNames(self):
    objectName = javax.management.ObjectName(MBEAN_OBJECT_NAME)
    
    clusters = self.mbeanConnection.invoke(
      objectName, "listClusterNames", [], [])
    
    return clusters

  # Get the status of a cluster
  def getStatus(self, clusterName):
    objectName = javax.management.ObjectName(MBEAN_OBJECT_NAME)
    
    status = self.mbeanConnection.invoke(
      objectName, "getStatus", [clusterName], ["java.lang.String"])
    
    return status
    
  # Gets the cluster name for a server.
  def getClusterName(self, host, userdir, serverName):
    objectName = javax.management.ObjectName(MBEAN_OBJECT_NAME)
    
    clusterName = self.mbeanConnection.invoke(
      objectName, "getClusterName", [host, userdir, serverName], 
         ["java.lang.String", "java.lang.String", "java.lang.String"])
    
    return clusterName
    
  # Generate Cluster plugin-cfg.xml
  def genPlugin(self, clusterName):
    objectName = javax.management.ObjectName(MBEAN_OBJECT_NAME)
    
    pluginFile = self.mbeanConnection.invoke(
    objectName, "generateClusterPluginConfig", [clusterName], ["java.lang.String"])
    
    return pluginFile
