# Install or uninstall an application to a member server

## Description

The manageAppOnServer.py sample demonstrates how to call the RoutingContext MBean and FileTransfer MBean from a Jython script to install or uninstall a simple application to a member server.

*   The RoutingContext MBean operation used:
    *   assignServerContext
*   The FileTransfer MBean operation used:
    *   uploadFile
    *   deleteFile

### manageAppOnServer.py script

This sample script demonstrates how to install a simple application to a member server with the given server name, server host and server usr directory. This script can only be used to install or uninstall a WAR application file. A connection is made to the collective controller located at the given host and port and the request to upload or delete the application file is passed to the FileTransfer MBean. The script also adds the application element to, or removes the application element from, the server.xml of the member server. By default, this script installs WAR files into ${server.config.dir}/apps unless the --appDir option is used.

Because this script uses the FileTransfer MBean to upload one or more files, the remoteFileAccess element must be specified in the server.xml of the server that will receive the file(s). Without this you will get a file permission error when using the script. Here is an example of a remoteFileAccess element:

> <remoteFileAccess>  
> <writeDir>${server.config.dir}</writeDir>  
> </remoteFileAccess>

For further information and examples for remoteFileAccess, please visit the Information Center for "WebSphere Application Server V8.5 Liberty profile" and search for "List of provided MBean," "remoteFileAccess" or "Configuration elements in the server.xml" information center topics.

File transfer and server commands require remote execution and access (RXA). Before running this sample script, ensure the target system(s) are configured for remote access. For more information on the remote execution and access requirements and setup, refer to [Requirements for using Remote Execution and Access (RXA)](http://www14.software.ibm.com/webapp/wsbroker/redirect?version=phil&product=was-nd-dist&topic=cins_cim_rxa_requirements) in the information center.

Running the script pushes the application file to the apps directory of the member server and adds the application element to the member server. The script can be used to install a simple application which does not require more configuration in the server.xml. For applications that require additional configuration of the server.xml, see the transferAppToServer.py and updateClusterConfig.py sample scripts.

## Instructions

#### Required parameters

> <table border="1" cellpadding="5">
> 
> <tbody>
> 
> <tr>
> 
> <td>--install or --uninstall</td>
> 
> <td>The path to the application WAR file to be installed.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--serverName</td>
> 
> <td>The name of the member server to install the application.</td>
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
> <td>--appDir</td>
> 
> <td>The directory where the application is to be installed. If not specified, it will be installed to the default location, the ${server.config.dir}/apps directory.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--help</td>
> 
> <td>Displays help text.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--debug</td>
> 
> <td>Displays additional details when an error occurs.</td>
> 
> </tr>
> 
> </tbody>
> 
> </table>

#### Sample use and resulting messages

<pre class="code">>>jython manageAppOnServer.py --install=c:/Liberty/applications/snoop.war --serverName=member1 --serverHost=host1 --serverUsrdir=c:/Liberty/usr --truststore=C:/Liberty/usr/servers/controller1/resources/security/trust.jks --truststorePassword=password --host=localhost --port=9443 --user=admin --password=adminpwd 

Connecting to the server...
Successfully connected to the server "localhost:9443"
Uploading application snoop.war to host1,C:\Liberty\usr,member1
Updating server config for host1,C:\Liberty\usr,member1
Complete
    </pre>

<pre class="code">>>jython manageAppOnServer.py --uninstall=snoop.war --serverName=member1 --serverHost=host1 --serverUsrdir=c:/Liberty/usr --truststore=C:/Liberty/usr/servers/controller1/resources/security/trust.jks --truststorePassword=password --host=localhost --port=9443 --user=admin --password=adminpwd

Connecting to the server...
Successfully connected to the server "localhost:9443"
Removing application snoop.war from host1,C:\Liberty\usr,member1
Updating server config for host1,C:\Liberty\usr,member1
Complete
    </pre>

## Notes

The following additional sample scripts provide shared code which is used by this sample:

*   wlp_arguments.py
*   wlp_serverConfig.py

## Support Information

For further information and resources for developers using IBM WebSphere Application Server, please visit [wasdev.net](http://wasdev.net).
