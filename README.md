# Liberty Collective Sample Admin Scripts

This is a collection of sample scripts for managing Liberty collectives.

## Background 
Since IBM WebSphere Application Server Network Deployment Version 8.5.5, Liberty can be managed via the [Liberty collective](https://www.ibmdw.net/wasdev/docs/article_introducingcollectives/). Refer to information about [collectives](http://www14.software.ibm.com/webapp/wsbroker/redirect?version=phil&product=was-nd-mp&topic=tagt_wlp_server_management) in the IBM WebSphere Application Server Version knowledge center for more specifics.


## Sample Scripts

Sample | Description
------------ | -------------
deployMembers | Deploy collective members via the Collective Controller
genClusterPlugin | Generate a plugin-cfg.xml for a cluster
getClusterStatus | Get the status of a cluster
listClusterMembers | List the members of a cluster
listClusterNames | List the clusters defined in the collective
manageAppOnCluster | Install or uninstall an application to cluster
manageAppOnServer | Install or uninstall an application to a member server 
startCluster | Start all members of a cluster
startServer | Start a server in a collective (jython)
startServer_Groovy | Start a server in a collective (groovy)
startServer_JRuby | Start a server in a collective (jruby)
stopCluster | Stop all members of a cluster
stopServer | Stop a server in a collective (jython)
stopServer_Groovy | Stop a server in a collective (groovy)
stopServer_JRuby | Stop a server in a collective (jruby)
transferAppToCluster | Transfer an application to all members of a cluster
transferAppToServer | Transfer an application to a member server
transferConfigToCluster | Transfer server configuration to all members of a cluster
transferConfigToServer | Transfer server configuration to a server
updateClusterConfig | Update server configuration to all members of a cluster
updateServerConfig | Update server configuration to a server





This is a fork from the samples on [wasdev.net](https://developer.ibm.com/wasdev/downloads/#filter/sortby=relevance;q=script;viewmode=list)