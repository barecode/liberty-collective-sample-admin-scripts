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
# This class is intended to assist jython scripts in processing command line
# arguments.  It can support positional parameters, as well as arguments
# in the form --argument and --argument=xxx.
#
# Scripts using this class should create a subclass, implementing the following
# methods:  printUsage(), printHelp(), validate().
#
# The constructor for the subclass should pass the number of positional 
# parameters, and two lists containing the names of the two types of arguments.
# The first list is keyword parms. The second list is value parms.
# The parse(args) method will parse the arguments and call your printUsage()
# method if the arguments are not well formed.  If they are well formed, it
# will call your validate() method, which can verify that the required
# arguments are provided, and that there are no conflicting arguments.  Your
# validate() method should call printUsage() and printHelp() as appropriate.
#
# Positional parameters must come immediately after the script name, followed
# by the other two types of parameters.
# Ex: jython startCluster.py positional1 positional2 --arg3 --arg4=xxx --etc
#
# Positional parameters can be retrieved from the parsed arguments by calling
# getPositional(index) where index 0 is the first argument.  The other two
# types of arguments can be retrieved by using jython dictionary notation
# on the arguments object.
#
# Ex:   argParser = StartClusterArgs(1, ["--arg1"], ["--arg2"])
#       if (argParser.parse(sys.argv) == True):
#         firstPositionalArg = argParser.getPositional(0)
#         isArg1specified = ("--arg1" in argParser)
#         arg2 = argParser["--arg2"]
#
# See startCluster.py and stopCluster.py for a more complete example.
#
# For those methods which require access to an MBean, the list
# MBEAN_VALUE_PARMS provides the common arguments that you should use
# to establish a connection to the MBean.  You can add this list to your own
# list if you have additional arguments to parse.
#

# ========================================================================
# The following arguments will be common among all scripts which require
# a connection to the MBean server
# ========================================================================
# Argument specifying where in the file system the trust store used by
# the JMXConnector is located.
TRUST_STORE = '--truststore'

# Argument specifying what the password is for the trust store specified
# by TRUST_STORE.
TRUST_STORE_PASSWORD = '--truststorePassword'

# Argument specifying the host name where the collective controller is
# installed.
HOSTNAME = '--host'

# Argument specifying the HTTPS port where the collective controller is 
# listening.
PORT = '--port'

# Argument specifying the user name to use when authenticating with the 
# collective controller.
USERNAME = '--user'

# Argument specifying the password to use when authenticating with the
# collective controller.
PASSWORD = '--password'

# Convenience list of all of the common MBean server arguments.
MBEAN_VALUE_PARMS = [TRUST_STORE ,
                     TRUST_STORE_PASSWORD ,
                     HOSTNAME ,
                     PORT ,
                     USERNAME ,
                     PASSWORD ]
# ========================================================================

# Argument specifying the user would like us to print the help text.
HELP = '--help'

# Argument specifying the user would like us to print debug info.
DEBUG = '--debug'

# Convenience list of common general flag type parameters
STANDARD_KEYWORD_PARMS = [HELP, DEBUG]

# ========================================================================

# Argument parsing class
class arguments(dict):
  numPos = 0
  noValueArgs = []
  valueArgs = []
  optionalValueArgs = []
  posArgs = []
  positionalArgsLeft = 0

  # Initialization routine.  Parameters:
  # numPos - the number of positional parameters
  # noValueArgs - a list of the no-value argument names (--x)
  # valueArgs - a list of the arguments that take a value (--x=y)
  # optionalValueArgs - a list of the arguments that take a value (--x=y) but are optional 
  def __init__(self, numPos, noValueArgs, valueArgs, optionalValueArgs=[]):
    dict.__init__(self)
    self.numPos = numPos
    self.noValueArgs = noValueArgs
    self.valueArgs = valueArgs
    self.optionalValueArgs = optionalValueArgs

  # Default printUsage function is a no-op.
  def printUsage(self):
    pass

  # Default printOptionalUsage function is a no-op.
  # Prints usage information for optionalValueArgs.
  def printOptionalUsage(self):
    pass

  # Default printHelp function is a no-op.
  def printHelp(self):
    pass

  # Default printOptionalHelp function is a no-op.
  # Prints help information for optionalValueArgs.
  def printOptionalHelp(self):
    print HELP + " Prints this help text."
    print
    print DEBUG + " Prints extra information if an error is encountered."

  # Default validate function ensures the correct number
  # of positional parms were given. 
  def validate(self):
    # If there are still positional args left, that's a problem.
    if (self.positionalArgsLeft > 0):
      print "Not all positional arguments were specified"
      self.printUsage()
      return False
    else:
      return True

  # Returns the positional argument at the given index.  Index 0 is the
  # first positional argument.
  def getPositional(self, index):
    if ((index >= 0) and (index < self.numPos)):
      return self.posArgs[index]
    else:
      return None

  # Parse the arguments as supplied by the init routine.  This routine will
  # call the printUsage, printHelp, and validate functions if you provided
  # implementations in a subclass.  Parameters:
  # args - The arguments as supplied by the caller.
  # returns True if parsed successfully, False if not.
  def parse(self, args):
    self.clear()

    if ((args == None) or (len(args) < 2)):
      self.printUsage()
      return False

    currentArgumentIndex = 1
    self.positionalArgsLeft = self.numPos
      
    # Iterate over the arguments.
    while (currentArgumentIndex < len(args)):
      indexOfEquals = args[currentArgumentIndex].find('=')
      # Positional arguments
      self.posArgs.append(args[currentArgumentIndex])
      if (self.positionalArgsLeft > 0 and (indexOfEquals == -1)):
        self.positionalArgsLeft -= 1
      # Arguments that don't require a value (flags)
      elif (args[currentArgumentIndex] in self.noValueArgs):
        curArgName = args[currentArgumentIndex]
        self[curArgName] = True
      # Argument which should have required a value
      elif (args[currentArgumentIndex] in self.valueArgs):
        print "No value was specified for the following argument: " + \
              args[currentArgumentIndex]
        self.printUsage()
        return False
      # Arguments which require a value
      elif ((indexOfEquals != -1) and 
            (args[currentArgumentIndex][0:indexOfEquals] in self.valueArgs)):
        curArgName = args[currentArgumentIndex][0:indexOfEquals]
        curArgValue = args[currentArgumentIndex][indexOfEquals+1:]
        if ((curArgValue == None) or (len(curArgValue) == 0)) :
          print "No value was specified for the following argument: " + \
                curArgName
          self.printUsage()
          return False
        else:
          self[curArgName] = curArgValue
      #############
      # Optional argument which should have required a value
      elif (args[currentArgumentIndex] in self.optionalValueArgs):
        print "No value was specified for the following argument: " + \
              args[currentArgumentIndex]
        self.printUsage()
        return False
      # Optinal arguments which require a value
      elif ((indexOfEquals != -1) and 
            (args[currentArgumentIndex][0:indexOfEquals] in self.optionalValueArgs)):
        curArgName = args[currentArgumentIndex][0:indexOfEquals]
        curArgValue = args[currentArgumentIndex][indexOfEquals+1:]
        if ((curArgValue == None) or (len(curArgValue) == 0)) :
          print "No value was specified for the following argument: " + \
                curArgName
          self.printUsage()
          return False
        else:
          self[curArgName] = curArgValue      
      #############
      # Everything else (error)
      else:
        print "The following argument name was not recognized: " + \
              args[currentArgumentIndex]
        self.printUsage()
        return False

      currentArgumentIndex += 1


    return self.validate()
    

# Subclass of command line arguments for mbean type scripts
class MBeanArgs(arguments):
  # Gets the usage string for optional arguments.  This is useful when you want to append
  # the optional arguments to some other string (like the regular usage string).
  def getOptionalUsage(self, optionalString):
    return optionalString

  # Gets the usage string for MBeanArgs.  This is useful when you want to append this
  # usage to some other usage on the same line.
  def getUsage(self):
    return "[" + HELP + "] [" + DEBUG + "] " + \
          TRUST_STORE + "=truststorePath " + \
          TRUST_STORE_PASSWORD + "=truststorePassword " + \
          HOSTNAME + "=hostname " + \
          PORT + "=port " + \
          USERNAME + "=adminUsername " + \
          PASSWORD + "=adminPassword "

  # Print usage of this command.  This implementation will only print the parameters
  # accepted by the MBeanArgs.  The caller must over-ride this method, printing the name of
  # the script and the names of the positional parameters.  It is then recommended that
  # the caller call getUsage on this class, to append the usage to their usage string.
  def printUsage(self):
    print self.getUsage()
  
  def printHelpPad(self, padString):
    pad = " "
    for x in range(len(padString)):
      pad += " "
    return pad

  def printRequiredHelp(self):
    print TRUST_STORE + "= The path in the file system to the trust store used to communicate"
    print self.printHelpPad(TRUST_STORE) + "with the collective controller"
    print
    print TRUST_STORE_PASSWORD + "= The password used to open the trust store specified by"
    print self.printHelpPad(TRUST_STORE_PASSWORD) + TRUST_STORE 
    print
    print HOSTNAME + "= The host name of the collective controller process"
    print
    print PORT + "= The https port used by the collective controller process"
    print
    print USERNAME + "= The user name to use when connecting to the collective controller"
    print self.printHelpPad(USERNAME) + "process"
    print
    print PASSWORD + "= The password for the user specified by " + USERNAME

  # Print help for this command
  def printHelp(self):
    print "The following options are required:"
    print ""
    self.printRequiredHelp()
    print ""
    print "The following options are not required: "
    print ""
    self.printOptionalHelp()
    print ""
    
  # Validate that the arguments are specified correctly.
  def validate(self):
    if (HELP in self or self.getPositional(0) == HELP):
      self.printHelp()
      return False

    if (arguments.validate(self)):
      missingArg = None

      if (TRUST_STORE not in self):
        missingArg = TRUST_STORE
      elif (TRUST_STORE_PASSWORD not in self):
        missingArg = TRUST_STORE_PASSWORD
      elif (HOSTNAME not in self):
        missingArg = HOSTNAME
      elif (PORT not in self):
        missingArg = PORT
      elif (USERNAME not in self):
        missingArg = USERNAME
      elif (PASSWORD not in self):
        missingArg = PASSWORD

      if (missingArg != None):
        print "The following required argument is missing: " + missingArg
        self.printUsage()

      return (missingArg == None)
    else:
      return False 
