# Transfer server configuration to a member server

## Description

The transferConfigToServer.py sample demonstrates how to call the FileTransfer MBean from a Jython script to transfer a server.xml file to a member server managed by a collective controller.

*   The FileTransfer MBean operation used:
    *   uploadFile

### transferConfigToServer.py script

This sample script demonstrates how to transfer a server configuration file to a member server with given server name, server host name and server usr directory. A connection is made to the collective controller located at the given host and port, and the request to upload the server configuration file is passed to the FileTransfer MBean.

Because this script uses the FileTransfer MBean to upload one or more files, the remoteFileAccess element must be specified in the server.xml of the server that will receive the file(s). Without this you will get a file permission error when using the script. Here is an example of a remoteFileAccess element:

> <remoteFileAccess>  
>        <writeDir>${server.config.dir}</writeDir>  
> </remoteFileAccess>

For further information and examples for remoteFileAccess, please visit the Information Center for "WebSphere Application Server V8.5 Liberty profile" and search for "List of provided MBean", "remoteFileAccess" or "Configuration elements in the server.xml" information center topics.

File transfer requires remote execution and access (RXA). Before running this sample script, ensure the target system(s) are configured for remote access. For more information on the remote execution and access requirements and setup, refer to [Requirements for using Remote Execution and Access (RXA)](http://www14.software.ibm.com/webapp/wsbroker/redirect?version=philproduct=was-nd-disttopic=cins_cim_rxa_requirements) in the information center.

## Instructions

#### Required parameters

> <table border="1" cellpadding="5">
> 
> <tbody>
> 
> <tr>
> 
> <td>First parameter</td>
> 
> <td>The path to the server.xml to transfer.</td>
> 
> </tr>
> 
> <tr>
> 
> <td>--serverName</td>
> 
> <td>The name of the member server to transfer the configuration.</td>
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

<pre class="code">>> jython transferConfigToServer.py path/to/server.xml --serverName=member1 --serverHost=host1 --serverUsrdir=c:\Liberty\usr --host=localhost --port=9443 --user=admin --password=password --truststorePassword=tsPassword --truststore=c:\Liberty\usr\servers\controller1\resources\security\trust.jks 

Connecting to the server...
Successfully connected to the server "localhost:9443"
Pushing the server.xml to server host1,C:\Liberty\usr,member1
   </pre>

## Notes

The following additional sample scripts provide shared code which is used by this sample:

*   wlp_arguments.py
*   wlp_serverConfig.py


## Support Information

For further information and resources for developers using IBM WebSphere Application Server, please visit [wasdev.net](http://wasdev.net).
