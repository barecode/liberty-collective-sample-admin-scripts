// COPYRIGHT LICENSE: This information contains sample code provided in source code form. You may copy, modify, 
// and distribute these sample programs in any form without payment to IBM for the purposes of developing, using, marketing or 
// distributing application programs conforming to the application programming interface for the operating platform for which the sample code is written. 
// Notwithstanding anything to the contrary, IBM PROVIDES THE SAMPLE SOURCE CODE ON AN "AS IS" BASIS AND IBM DISCLAIMS ALL WARRANTIES, 
// EXPRESS OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, 
// FITNESS FOR A PARTICULAR PURPOSE, TITLE, AND ANY WARRANTY OR CONDITION OF NON-INFRINGEMENT. IBM SHALL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, 
// INCIDENTAL, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR OPERATION OF THE SAMPLE SOURCE CODE. IBM HAS NO OBLIGATION TO PROVIDE MAINTENANCE, 
// SUPPORT, UPDATES, ENHANCEMENTS OR MODIFICATIONS TO THE SAMPLE SOURCE CODE.
//
// Copyright IBM Corp. 2013.
// All Rights Reserved. Licensed Materials - Property of IBM.
//
import JMXRESTConnector
import javax.management.ObjectName

class ServerCommand {
	def MBEAN_OBJECT_NAME="WebSphere:feature=collectiveController,type=ServerCommands,name=ServerCommands"
	def objectName=new ObjectName(MBEAN_OBJECT_NAME)
	def mbeanConnection

	def ServerCommand(mbeanConnection) {
		this.mbeanConnection=mbeanConnection
	}

	def start(host,userdir,serverName,options) {
		def params = new String[4]
		params[0]=host
		params[1]=userdir
		params[2]=serverName
		params[3]=options
		def typeParams = new String[4]
		typeParams[0]="java.lang.String"
		typeParams[1]="java.lang.String"
		typeParams[2]="java.lang.String"
		typeParams[3]="java.lang.String"
		def result=mbeanConnection.invoke(objectName,"startServer",params,typeParams) 
		return result
	}

	def stop(host,userdir,serverName,options) {
		def params = new String[4]
		params[0]=host
		params[1]=userdir
		params[2]=serverName
		params[3]=options
		def typeParams = new String[4]
		typeParams[0]="java.lang.String"
		typeParams[1]="java.lang.String"
		typeParams[2]="java.lang.String"
		typeParams[3]="java.lang.String"
		def result=mbeanConnection.invoke(objectName,"stopServer",params,typeParams) 
		return result
	}
}

