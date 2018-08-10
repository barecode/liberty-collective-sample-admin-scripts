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
class MBeanArgsParser {
	def cli // CLIBuilder

	def MBeanArgsParser() {
		cli = new CliBuilder(posix: false)
	}

	def setUsage(s) {
		cli.setUsage(s)
	}

	def setHeader(s) {
		cli.setHeader(s)
	}

	def setFooter(s) {
		cli.setFooter(s)
	}

	def addArg(name,desc,req) {
		cli._(longOpt:name,args:1,argName:'',desc,required:req)
	}

	def parse(args) {
		cli._(longOpt:'truststore',args:1, argName:'','The path in the file system to the trust store used to communicate with the collective controller',required:true)
		cli._(longOpt:'truststorePassword',args:1, argName:'','The password used to open the trust store specified by --truststore',required:true)
		cli._(longOpt:'host',args:1,argName:'','The host name of the collective controller process',required:true)
		cli._(longOpt:'port',args:1,argName:'','The https port used by the collective controller process',required:true)
		cli._(longOpt:'user',args:1,argName:'','The user name to use when connecting to the collective controller',required:true)
		cli._(longOpt:'password',args:1,argName:'','The password for the user specified by --user',required:true)
		if(args.length==0 || args[0]=='--help') {
			cli.usage()
			return false
		}
		def options=cli.parse(args)
		return options
	}

	def usage() {
		cli.usage()
	}
}
