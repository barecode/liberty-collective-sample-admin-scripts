# Update server config

## Description

The updateServerConfig.py sample demonstrates how to call the FileTransfer MBean from a Jython script to invoke the FileTransfer MBean to retrieve and update the server.xml file for a Liberty collective member server that is managed by a collective controller.

*   The FileTransfer MBean operations used:
    *   downloadFile
    *   uploadFile

### updateServerConfig.py script

The updateServerConfig sample script demonstrates how to download and upload server configuration file with the given operation ("get" or "put"). A connection is made to the collective controller located at the given host and port and the request to download or upload the file is passed to the FileTransfer MBean.

The first positional parameter is either "get" or "put". When the parameter is "get", the server.xml for the target member server is retrieved into the local file system. When the parameter is "put", the server.xml is pushed to the server from the local file server. The typical usage of this script is to retrieve the server.xml using "get", update it using a text editor, and replace it using the "put" parameter.

Because this script uses the FileTransfer MBean to upload one or more files, the remoteFileAccess element must be specified in the server.xml of the server that will receive the file(s). Without this you will get a file permission error when using the script. Here is an example of a remoteFileAccess element:

> <remoteFileAccess>  
>        <writeDir>${server.config.dir}</writeDir>  
> </remoteFileAccess>

For further information and examples for remoteFileAccess, please visit the Information Center for "WebSphere Application Server V8.5 Liberty profile" and search for "List of provided MBean", "remoteFileAccess" or "Configuration elements in the server.xml" information center topics.

File transfer requires remote execution and access (RXA). Before running this sample script, ensure the target system(s) are configured for remote access. For more information on the remote execution and access requirements and setup, refer to [Requirements for using Remote Execution and Access (RXA)](http://www14.software.ibm.com/webapp/wsbroker/redirect?version=phil&product=was-nd-dist&topic=cins_cim_rxa_requirements) in the information center.


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
> <td>get or put.</td>
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
> <tr>
> 
> <td>--serverHost</td>
> 
> <td>The host name where the collectiveMember is installed.</td>
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
> <td>--serverName</td>
> 
> <td>The name of the server which is installed on the host and usr directory described by serverHost and serverUsrdir, and whose server.xml is to be modified.</td>
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
> <tr>
> 
> <td>--localDir</td>
> 
> <td>The name of a directory on the local machine where the server.xml can be stored. If this parameter is not supplied, the current directory is used.</td>
> 
> </tr>
> 
> </tbody>
> 
> </table>

#### Sample use and resulting messages

<pre class="code">>> jython updateServerConfig.py get --serverName=member1 --serverHost=myhost.austin.ibm.com --serverUsrdir=C:\Liberty\usr --truststore=C:\Liberty\usr\servers\controller1\resources\security\trust.jks 
--truststorePassword=controller1 --host=localhost --port=9443 --user=admin --password=adminpwd --localDir=C:\temp\user\config\member1

Connecting to the server...
Successfully connected to the server "localhost:9443"
</pre>

<pre class="code">>> jython updateServerConfig.py put --serverName=member1 --serverHost=myhost.austin.ibm.com --serverUserdir=C:\Liberty\usr --truststore=C:\Liberty\usr\servers\controller1\resources\security\trust.jks 
--truststorePassword=controller1 --host=localhost --port=9443 --user=admin --password=adminpwd --localDir=C:\temp\user\config\member1

Connecting to the server...
Successfully connected to the server "localhost:9443"
</pre>

## Notes

The following additional sample scripts provide shared code which is used by this sample:

*   wlp_arguments.py
*   wlp_serverConfig.py

## Support Information

For further information and resources for developers using IBM WebSphere Application Server, please visit [wasdev.net](http://wasdev.net).
