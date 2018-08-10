# Licensed Materials - Property of IBM  
# "Restricted Materials of IBM"
# 5724-H88, 5724-J08, 5724-I63, 5655-W65, 5724-H89, 5722-WE2   Copyright IBM Corp., 2013
# All Rights Reserved * Licensed Materials - Property of IBM
# US Government Users Restricted Rights - Use, duplication or disclosure
# restricted by GSA ADP Schedule Contract with IBM Corp.

# See startServer.rb and stopServer.rb for a complete example.

class MBeanArgsParser

	# Constants
	#
	TRUST_STORE = "--truststore"
	TRUST_STORE_PASSWORD = "--truststorePassword"
	HOSTNAME = "--host"
	PORT = "--port"
	USERNAME = "--user"
	PASSWORD = "--password"
	
	MBEAN_VALUE_PARAMS=[TRUST_STORE,TRUST_STORE_PASSWORD,HOSTNAME,PORT,USERNAME,PASSWORD]

	HELP = "--help"
	DEBUG = "--debug"

	def initialize()
		# @num_pos = 0
		# @pos_args = []
		# @value_args = Hash.new 
		# @optional_value_args = {} 
		@debug=false
	end

	def parseArgs(argv,num_pos,optional_value_args)
		@value_args = {} 
		@optional_value_args = {} 
		inc = 0
		if argv[0].eql?(HELP)
			printHelp()
			return false
		elsif argv[0].eql?(DEBUG)
			@debug=true
			inc = inc +1
		end

		if argv.size < num_pos + inc + 1
			printUsage()
			return false
		end

		@num_pos = num_pos
		@pos_args=Array.new(@num_pos)
		if @debug==true
			@num_pos=@num_pos+1
		end
		inc.upto(@num_pos-1) do |n|
			arg = argv[n]
			@pos_args[n] = arg
		end

		@num_pos.upto(argv.length-1) do |n|
			arg = argv[n]
			name,value = arg.split(/\s*=\s*/)
			# Arguments which should have required a value
			if value==nil and MBEAN_VALUE_PARAMS.include?(name)
				puts "No value was specified for the following argument: " + name
				printUsage()
				return false
			# Arguments which require a value
			elsif MBEAN_VALUE_PARAMS.include?(name)
				@value_args[name] = value
			# Optional arguments which should have required a value
			elsif value==nil and optional_value_args.include?(name)
				puts "No value was specified for the following argument: " + name
				printUsage()
				return false
			# Optional arguments which require a value
			elsif optional_value_args.include?(name)
				@optional_value_args[name] = value
			# Everything else (error)
			else
				puts "The following argument name was not recognized: " + argv[n]
				printUsage()
				return false
			end
		end
		return validate()
	end #parse

	# TBD: Arguments validation
	#
	def validate
		pos_args=@pos_args.compact
		if pos_args.size < @pos_args.size
			puts "Not all positional arguments were specified"
			printUsage
			return false
		end

		missingArg = nil
		if @value_args[TRUST_STORE] == nil
			missingArg = TRUST_STORE
		elsif @value_args[TRUST_STORE_PASSWORD] == nil
			missingArg = TRUST_STORE_PASSWORD
		elsif @value_args[HOSTNAME] == nil
			missingArg = HOSTNAME
		elsif @value_args[PORT] == nil
			missingArg = PORT
		elsif @value_args[USERNAME] == nil
			missingArg = USERNAME
		elsif @value_args[PASSWORD] == nil
			missingArg = PASSWORD
		end
		if missingArg == nil
			return true
		else
			puts "The following required argument is missing: " + missingArg
			printUsage()
			return false
		end

	end

	# Accessors
	#
	def get_pos_args
		return @pos_args
	end

	def get_value_args
		return @value_args
	end

	def get_no_value_args
		return @no_value_args
	end

	def get_optional_value_args
		return @optional_value_args
	end

	def debug?
		return @debug
	end

	# Help message
	#
	def printBaseHelp
		puts "The following options are required:"
		puts ""
		printRequiredHelp()
		puts ""
		puts "The following options are not required:"
		puts ""
		printOptionalHelp()
		puts ""
	end

	def printRequiredHelp
    		puts TRUST_STORE + " The path in the file system to the trust store used to communicate"
    		puts printHelpPad(TRUST_STORE) + "with the collective controller"
    		puts ""
    		puts TRUST_STORE_PASSWORD + " The password used to open the trust store specified by"
    		puts printHelpPad(TRUST_STORE_PASSWORD) + TRUST_STORE
    		puts ""
    		puts HOSTNAME + " The host name of the collective controller process"
    		puts ""
    		puts PORT + " The https port used by the collective controller process"
    		puts ""
    		puts USERNAME + " The user name to use when connecting to the collective controller"
    		puts printHelpPad(USERNAME) + "process."
    		puts ""
    		puts PASSWORD + " The password for the user specified by " + USERNAME
	end

	def printHelpPad(padString)
		pad = " "
		for i in 1..padString.length
			pad += " "
		end
		return pad
	end

	# Usage
	#
	def getBaseUsage
		return " --truststore=truststoreName --truststorePassword=truststorePassword --host=hostname --port=port --user=username --password=password " 
	end

	# May override this method
	#
	def printOptionalHelp
		puts HELP + " Prints this help text."
		puts ""
		puts DEBUG + " Prints extra information if an error is encountered."
	end

	# Override the following two methods
	#
	def printUsage
		# override this method
	end

	def printHelp
		printBaseHelp()
	end

end
