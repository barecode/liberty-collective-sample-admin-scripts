# Licensed Materials - Property of IBM  
# "Restricted Materials of IBM"
# 5724-H88, 5724-J08, 5724-I63, 5655-W65, 5724-H89, 5722-WE2   Copyright IBM Corp., 2013
# All Rights Reserved * Licensed Materials - Property of IBM
# US Government Users Restricted Rights - Use, duplication or disclosure
# restricted by GSA ADP Schedule Contract with IBM Corp.
#
require "java"
require "restConnector.rb"

class ServerCommand

	# The JMX ObjectName of the server command MBean
	MBEAN_OBJECT_NAME = "WebSphere:feature=collectiveController,type=ServerCommands,name=ServerCommands"

	# mbeanConnection is an instance of an MBeanServer connection, obtained
	# by calling the getMBeanServerConnection() method of the 
	# JMXRestConnector class. 
	def initialize(mbeanConnection)
		@mconnection = mbeanConnection
	end

	# Start the server
	def start(host,userdir,servername,options)
		objname=javax.management.ObjectName.new(MBEAN_OBJECT_NAME)
		result=@mconnection.invoke(objname,"startServer",[host,userdir,servername,options],["java.lang.String","java.lang.String","java.lang.String","java.lang.String"])
		return result
	end

	# Stop the server
	def stop(host,userdir,servername,options)
		objname=javax.management.ObjectName.new(MBEAN_OBJECT_NAME)
		result=@mconnection.invoke(objname,"stopServer",[host,userdir,servername,options],["java.lang.String","java.lang.String","java.lang.String","java.lang.String"])
		return result
	end
end
