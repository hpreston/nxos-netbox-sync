> This is a work in progress project.  A more detailed README will come soon!

# Cisco NX-OS Netbox Sync

![](resources/project_image.jpg)

I built this application as a demonstration of how a Source of Truth can drive network configuration by not only verifing that a network devices configuration matches the Source of Truth, but also implement changes when deviations are found.  

The technologies used in this demonstration are: 

* [Netbox]() - A modern IPAM and DCIM tool, written in Python and providing robust programmability support through APIs and SDKs
* [pyATS]() - An Open Source* network verification and configuration tool used to gather operational and configuration details from a live network, as well as make configuration changes.  
* [Docker]() - A container technologies used to "package" up the application into a portable image that can be run nearly anywhere 
* [Cisco NX-OS]() - A programmable network operating system providing many features, including running containers on the switch. 
* [Webex Teams]() - An collaboration platform offering rich communication and programmability features allowing for robust ChatOps use cases.

Here are some videos that show the application in action:  

* <a href='https://youtu.be/iD5VrL82j6E' target="blank">Cisco NX-OS Netbox Sync Demo1: In Action</a>

## Project Goals 

1. Netbox Sync 
    * Interface enable status 
    * Interface descriptions 
    * VLANs 
    * Interface L2 Configuration - mode and vlans 
1. Teams Report 
    * When a sync issue is detected 
    * When system starts up 
    * When an update is made (same as sync issue)
