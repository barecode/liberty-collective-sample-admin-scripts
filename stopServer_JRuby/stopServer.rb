# Licensed Materials - Property of IBM  
# "Restricted Materials of IBM"
# 5724-H88, 5724-J08, 5724-I63, 5655-W65, 5724-H89, 5722-WE2   Copyright IBM Corp., 2013
# All Rights Reserved * Licensed Materials - Property of IBM
# US Government Users Restricted Rights - Use, duplication or disclosure
# restricted by GSA ADP Schedule Contract with IBM Corp.

#
# stopServer.rb
#
# Stops a server with the given host name, user directory, and server name.  
# A connection is made to the collective controller located at the given host 
# and port, and the request to start the server is passed to the ServerCommandMBean.
# Note the server host name and collective controller host name are specified
# separately so they can be different from one another.
# 
# Required parameters:
# --truststore= The path to the trust store to be used when establishing
#               a connection to the collective controller.
# --truststorePassword= The password for the truststore specified by 
#                       --truststore
# --host= The host name where the collective controller is running.
# --port= The https port where the collective controller is listening.
# --user= The user name to use when connecting to the collective controller.
# --password= The password to use when connecting to the collective controller.
# 
# Optional parameter for help:
# --help Displays help text
#
# ex. jython stopServer.py serverHost /usr/wlp/usr serverName --truststore=/home/user/key.jks --trustStorePassword=secret --host=host.com --port=9443 --user=Administrator --password=secret2

require "wlp_mbean_args_parser"
require "wlp_server_command"

class StopServerArgsParser < MBeanArgsParser
	OPTIONS="--options"
	def initialize
		@options=[OPTIONS]
	end

	def parse(argv)
		return parseArgs(argv,3,@options) 
	end

	def printUsage()
		puts ""
		print "Usage: jruby stopServer.rb [--debug] serverHost serverUserDir serverName"
		print getBaseUsage
		puts " [--options=\"options list\"]"
		puts ""
		puts "For HELP: jruby stopServer.rb --help"
	end

	def printHelp
		printUsage()
		puts ""
		puts "Used to stop a server specified by the serverHost, serverUserDir, and serverName."
		puts ""
		printBaseHelp()
		puts ""
    		puts "Example: jython stopServer.py serverHost serverUserDir serverName --truststore=/home/user/key.jks --trustStorePassword=secret --host=host.com --port=9443 --user=Administrator --password=secret2 --options=\"--clean --include=someValue\""
	end

	def printOptionalHelp
    		puts "--options A space-delimited list of Liberty server command options.  The list must be enclosed in double quotes."
	end

end

class StopServer

	def initialize(parser)
		@pos_args = parser.get_pos_args()
		@no_value_args = parser.get_no_value_args()
		@value_args = parser.get_value_args 
		@optional_value_args = parser.get_optional_value_args()
	end

	def execute()
		trustStore = @value_args[MBeanArgsParser::TRUST_STORE]
		trustStorePassword = @value_args[MBeanArgsParser::TRUST_STORE_PASSWORD]
		controller = @value_args[MBeanArgsParser::HOSTNAME]
		port = @value_args[MBeanArgsParser::PORT].to_i
		user = @value_args[MBeanArgsParser::USERNAME]
		password = @value_args[MBeanArgsParser::PASSWORD]

		host = @pos_args[0]
		userdir = @pos_args[1]
		server = @pos_args[2]

		options = @optional_value_args[StopServerArgsParser::OPTIONS]

		connector = JMXRESTConnector.new
		connector.setTrustStore(trustStore)
		connector.setTrustStorePassword(trustStorePassword)
		connector.connect(controller,port,user,password)
		mconnection = connector.getMBeanServerConnection()
		serverCommand = ServerCommand.new(mconnection)
		result = serverCommand.stop(host,userdir,server,options)
		return result
	end
end

# main begins here
parser = StopServerArgsParser.new()
if(parser.parse(ARGV) == false)
	exit()
end

stopServer = StopServer.new(parser)
result = stopServer.execute()
if parser.debug?
      puts "stdErr="+result.get("stdErr")
      puts "stdOut="+result.get("stdOut")
      puts "returnCode="+result.get("returnCode")
end
returnCode = result.get("returnCode").to_i
if returnCode == 0
	puts "Server stopped successfully"
elsif returnCode == 1
    print "Server already stopped"
elsif returnCode == 2
    puts "Server could not be found. Check your --serverHost, --serverUsrdir and --serverName values."
    puts "The server host must match the value of the defaultHostName set in the server.xml"
else
    puts "Server did not stop: return code = " + returnCode.to_s
    exit(returnCode)
end


