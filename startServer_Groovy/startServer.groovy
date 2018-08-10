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
import MBeanArgsParser

def parse(args) {
	def parser=new MBeanArgsParser() 
	parser.setUsage('groovy startServer.groovy [--help] --serverHost=serverHost --serverUsrDir=serverUserDir --serverName=serverName --truststore=truststoreName --truststorePassword=truststorePassword --host=hostname --port=port --user=username --password=password [--options=options]')
	parser.setHeader('\nUsed to start a server specified by the serverHost, serverUserDir, and serverName. \nThe following options are available:\n') 
	parser.setFooter('\nExample: groovy startServer.groovy --serverName=member1 --serverHost=localhost --serverUsrdir=/wlp/usr --truststore=/wlp/usr/servers/<servername>/resources/security/trust.jks --truststorePassword=secret --host=localhost --port=9443 --user=Administrator --password=secret2 --options=\"--clean --include=someValue\"')
	parser.addArg('serverHost','A space delimited list of Liberty server command options. The list must be enclosed in double quotes',true)
	parser.addArg('serverUsrDir','A space delimited list of Liberty server command options. The list must be enclosed in double quotes',true)
	parser.addArg('serverName','A space delimited list of Liberty server command options. The list must be enclosed in double quotes',true)
	parser.addArg('options','A space delimited list of Liberty server command options. The list must be enclosed in double quotes',false)
	def options=parser.parse(args)
	if(options==null || !options) {
		System.exit(-1)
	}
	if(options.arguments().size()!=0) {
		println '\nUnknown argument(s): ' + options.arguments()
		println ""
		System.exit(-1)
	}
	return options
}

options=parse(args)
connector = new JMXRESTConnector()
connector.trustStore = options.truststore 
connector.trustStorePassword = options.truststorePassword 
connector.connect(options.host,Integer.parseInt(options.port),options.user,options.password)
mconnection = connector.getMBeanServerConnection()

command=new ServerCommand(mconnection)
startServerOption=options.options
if (!startServerOption)
	startServerOption=""
result=command.start(options.serverHost,options.serverUsrDir,options.serverName,startServerOption)

returnCode=Integer.parseInt(result.get("returnCode"))
if (returnCode==0)
	println "Server started successfully"
else if (returnCode==1)
	println "Server alrady started"
else {
	println "Server did not start: return code = " + returnCode
	println "stdErr=" + result.get("stdErr")
}

System.exit(returnCode)

