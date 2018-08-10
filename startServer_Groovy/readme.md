# Start Server (Groovy)

## Description

The startServer.groovy sample demonstrates how to call the ServerCommands MBean from a Groovy script to start a collective member server.

*   The ServerCommands MBean operation used:
    *   startServer

### startServer.groovy script

The startServer sample script demonstrates how to start a collective member with the given member host name, usr directory and member name. A connection is made to the collective controller located at the given host and https port, and the request to start the server is passed to the ServerCommands MBean.

Note that the server host name and collective controller host name do not need to be the same.

Server commands require remote execution and access (RXA). Before running this sample script, ensure each target system is configured for remote access. For more information on the remote execution and access requirements and setup, refer to [Requirements for using Remote Execution and Access (RXA)](http://www14.software.ibm.com/webapp/wsbroker/redirect?version=phil&product=was-nd-dist&topic=cins_cim_rxa_requirements) in the information center.

## Instructions

#### Required parameters

> <table border="1" cellpadding="5">
> 
> <tbody>
> 
> <tr>
> 
> <td>--serverName</td>
> 
> <td>The name of the member server to start.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--serverHost</td>
> 
> <td>The host name where the collective member is installed.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--serverUsrdir</td>
> 
> <td>The usr directory where the collective member is installed.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--truststore</td>
> 
> <td>The path to the truststore to be used when establishing a connection to the collective controller.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--truststorePassword</td>
> 
> <td>The password for the truststore specified by the --truststore parameter.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--host</td>
> 
> <td>The host name where the collective controller is running.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--port</td>
> 
> <td>The https port where the collective controller is listening.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--user</td>
> 
> <td>The user name to use when connecting to the collective controller.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--password</td>
> 
> <td>The password to use when connecting to the collective controller.</td>
> 
> </tr>
> 
> </tbody>
> 
> </table>

#### Optional parameters

> <table border="1" cellpadding="5">
> 
> <tbody>
> 
> <tr>
> 
> <td>--help</td>
> 
> <td>Displays help text.</td>
> 
> </tr>
> 
> </tbody>
> 
> </table>

#### Sample use and resulting messages

> groovy startServer.groovy --serverName=member1 --serverHost=host.com --serverUsrdir=C:\wlp\usr --truststore=C:\wlp\usr\servers\controller1\resources\security\trust.jks --truststorePassword=tsPassword --host=host.com --port=9443 --user=admin --password=password  
>   
> _Connecting to the server...  
> Successfully connected to the server "host.com:9443"  
> Server started successfully_

#### Example usage

<pre class="code">>> groovy startServer.groovy --serverName=member1
  --serverHost=host.com --serverUsrdir=C:\wlp\usr
  --truststore=C:\wlp\usr\servers\controller1\resources\security\trust.jks
  --truststorePassword=tsPassword --host=host.com --port=9443
  --user=admin --password=password Connecting to the server...

  Successfully connected to the server "host.com:9443" Server started successfully</pre>

## Notes

The following additional sample scripts provide shared code which is used by this sample:

*   MBeanArgsParser.groovy
*   ServerCommand.groovy


## Sample Structure

*   Copyright.txt
*   lib

*   MBeanArgsParser.groovy
*   ServerCommand.groovy

*   readme.html
*   startServer.groovy


## Support Information

For further information and resources for developers using IBM WebSphere Application Server, please visit [wasdev.net](http://wasdev.net).
