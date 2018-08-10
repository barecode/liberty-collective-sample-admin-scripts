# Get Cluster Status

## Description

The getClusterStatus.py sample demonstrates how to call the ClusterManager MBean from a Jython script to get the status of a cluster.

*   The ClusterManager MBean operation used:
    *   getStatus

### getClusterStatus.py script

The getClusterStatus sample script demonstrates how to obtain the status of a given cluster. A connection is made to the collective controller located at the given host and port, and the request to get the cluster status is passed to the ClusterManager MBean.

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
> <td>The cluster name.</td>
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

<pre class="code">>> jython genClusterStatus.py defaultCluster --host=localhost --port=9443 --user=admin --password=password --truststore=c:\wlp\usr\servers\controller1\resources\security\trust.jks --truststorePassword=tsPassword
Connecting to the server...
Successfully connected to the server "localhost:9443"
Status for cluster cluster1: STARTED.
</pre>

## Notes

<div id="ibm-wasdev-sample-notes-content">The following additional sample scripts provide shared code which is used by this sample:

*   wlp_arguments.py
*   wlp_cluster.py

</div>

## Support Information

For further information and resources for developers using IBM WebSphere Application Server, please visit [wasdev.net](http://wasdev.net).
