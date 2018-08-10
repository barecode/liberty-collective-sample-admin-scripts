# Deploy Collective Members

## Description

The deployMembers.py sample demonstrates how to call the RoutingContext MBean, CollectiveRegistration MBean, ServerCommands MBean and FileTransfer MBean from a Jython script to deploy, join and start members.

* The RoutingContext MBean operation used:
    * assignHostContext
* The CollectiveRegistration MBean operations used:
    * registerHost
    * updateHost
    * join

* The FileTransfer MBean operation used:
    * uploadFile
* The ServerCommands MBean operation used:
    * startServer
    
### deployMembers.py script
This sample script demonstrates how to install a liberty profile with collective members and join the members to the collective controller, remotely. It performs the following operations:
* Connects to the collective controller located at the specified host and port.
* The archive (.zip) file is uploaded to the target computer, which was registered before the transfer.
* The archive is expanded at the specified installation directory on the target computer.
* Each member is joined to the collective and started.

The members in the archive file have an expected format and contents as described in the section **Building the archive file**. For simplicity, this sample propagates the truststore files of the controller to each member. Therefore, the passwords in the member for truststores can be copied into the server.xml of each member from the server.xml of the controller.

File transfer and server commands require remote execution and access (RXA). Before running this sample script, ensure the target system(s) are configured for remote access. For more information on the remote execution and access requirements and setup, refer to [Requirements for using Remote Execution and Access (RXA)](http://www14.software.ibm.com/webapp/wsbroker/redirect?version=phil&product=was-nd-dist&topic=cins_cim_rxa_requirements) in the IBM knowledge center.

## Instructions

#### Required parameters

<table border="1">

<tbody>

<tr>

<td>--zipFile</td>

<td>The fully qualified archive (.zip) file path to upload to target machine.</td>

</tr>

<tr>

<td>--installDir</td>

<td>The path where the member will be installed on the target machine.</td>

</tr>

<tr>

<td>--installHost</td>

<td>The host name of the target machine.</td>

</tr>

<tr>

<td>--rpcUser</td>

<td>The rpc user of the target computer.</td>

</tr>

<tr>

<td>--rpcUserPassword</td>

<td>The rpc user password of the target computer.</td>

</tr>

<tr>

<td>--truststore</td>

<td>The path to the truststore to be used when establishing a connection to the collective controller.</td>

</tr>

<tr>

<td>--truststorePassword</td>

<td>The password for the truststore specified by the --truststore parameter.</td>

</tr>

<tr>

<td>--host</td>

<td>The host name where the collective controller is running.</td>

</tr>

<tr>

<td>--port</td>

<td>The https port where the collective controller is listening.</td>

</tr>

<tr>

<td>--user</td>

<td>The user name to use when connecting to the collective controller.</td>

</tr>

<tr>

<td>--password</td>

<td>The password to use when connecting to the collective controller.</td>

</tr>

</tbody>

</table>

#### Optional parameters

<table border="1">

<tbody>

<tr>

<td>--help</td>

<td>Displays help text.</td>

</tr>

<tr>

<td>--debug</td>

<td>Displays additional details when an error occurs.</td>

</tr>

</tbody>

</table>

#### Sample use and resulting messages
For this example, the zip file contains 4 members, named: member1; member2; member3; and member4.

<pre class="code">>> jython deployMembers.py --zipFile=C:/Liberty/wlp.zip --installDir=c:/Liberty/wlp --installHost=target-server.ibm.com --rpcUser=administrator --rpcUserPassword=secret --truststore=C:/Liberty/wlp/usr/servers/controller1/resources/security/trust.jks --truststorePassword=password --host=controller-server.ibm.com --port=9443 --user=admin --password=adminpwd

Connecting to the server...
Successfully connected to the server "controller-server.ibm.com:9443"
Assigning host context for: target-server.ibm.com
The host has already been registered, calling updateHost instead.
The host target-server.ibm.com connection information is configured.
Loading and expanding wlp.zip on target computer location c:/Liberty/wlp

Member member1 join the collective
Uploading needed security files to member1
Starting member member1
Server member1 started successfully

Member member2 join the collective
Uploading needed security files to member2
Starting member member2
Server member2 started successfully

Member member3 join the collective
Uploading needed security files to member3
Starting member member3
Server member3 started successfully

Member member4 join the collective
Uploading needed security files to member4
Starting member member4
Server member4 started successfully
</pre>


## Notes

The following additional sample scripts provide shared code which is used by this sample:
* wlp_arguments.py
* wlp_serverConfig.py

### Building the archive file

#### Member directories

From a Liberty installation, you will zip up all the directories under the Liberty install folder such as: bin, clients, dev, usr. All file permissions under the bin directory must be set to executable before zipping. In the usr directory, only include the directories for the members(s) that you want to deploy on the target computer.

#### Member configuration

The script assumes that you have create a collective controller. For more information on how to complete the configuration, see the [Configuring a Liberty collective](http://www14.software.ibm.com/webapp/wsbroker/redirect?version=phil&product=was-nd-mp&topic=tagt_wlp_configure_collective) topic in the information center. The topic contains instructions for modifying the server's server.xml of a member for use with join the collective controller.

The steps to complete for the member configuration include:
* Add collectiveMember feature tag below to all member's server.xml <featuremanager><feature>collectiveMember-1.0</feature></featuremanager>
* Add Http end point tag to all member's server.xml. **Note:** You can modify the ports to match with your environment to make sure no port conflict. <httpendpoint id="defaultHttpEndpoint" host="*" httpport="9081" httpsport="9444">


## Support Information

For further information and resources for developers using IBM WebSphere Application Server, please visit [wasdev.net](http://wasdev.net).
