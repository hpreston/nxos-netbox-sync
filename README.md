> This is a work in progress project.  A more detailed README will come soon!

# Cisco NX-OS Netbox Sync

![](resources/project_image.jpg)

I built this application as a demonstration of how a Source of Truth can drive network configuration by not only verifying that a network devices configuration matches the Source of Truth, but also implement changes when deviations are found.  

```text
Retrieving current status from device with pyATS
Looking up intended state for device from Netbox
Running tests to see if VLANs from Netbox are configured
❌ 11 MISSING from switch
❌ 12 MISSING from switch
❌ 13 MISSING from switch
✅ 21 (test-web) exists with correct name on switch
✅ 22 (test-app) exists with correct name on switch
✅ 23 (test-data) exists with correct name on switch

Running interface enabled test
✅ Ethernet1/1 was correctly found to be UP/UP on switch
✅ Ethernet1/2 was correctly found to be UP/UP on switch
✅ Ethernet1/3 was correctly found to be UP/UP on switch
✅ Ethernet1/4 was correctly found to be UP/UP on switch
✅ Ethernet1/5 was correctly found to be UP/UP on switch
✅ Mgmt0 was correctly found to be UP/UP on switch

Running interface description test
✅ Ethernet1/1 has the correct description configured on switch
✅ Ethernet1/2 has the correct description configured on switch
✅ Ethernet1/3 has the correct description configured on switch
✅ Ethernet1/4 has the correct description configured on switch
✅ Mgmt0 has the correct description configured on switch

Running interface mode test
✅ Ethernet1/2 is correctly configured as a trunk
✅ Ethernet1/3 is correctly configured as a trunk
✅ Ethernet1/4 is correctly configured as a trunk
✅ Ethernet1/5 is correctly configured as a trunk

Running interface vlan test
✅ Ethernet1/2 correctly is trunking ALL vlan ids.
❌❌ Vlan 11 is NOT configured on the switch.
❌❌ Vlan 12 is NOT configured on the switch.
❌❌ Vlan 13 is NOT configured on the switch.
✅ Ethernet1/6 correctly has 13 configured as the access vlan id

Creating 11 (production-web)
Creating 12 (production-app)
Creating 13 (production-data)
Updating Interface Ethernet1/4 mode to Tagged
Updating Interface Ethernet1/5 mode to Tagged
Updating Interface Ethernet1/3 mode to Tagged
```

The technologies used in this demonstration are: 

* [Netbox](http://netbox.readthedocs.io) - A modern IPAM and DCIM tool, written in Python and providing robust programmability support through APIs and SDKs
* [pyATS](http://developer.cisco.com/pyats/) - A network verification and configuration tool used to gather operational and configuration details from a live network, as well as make configuration changes.  
* [Docker](https://www.docker.com/resources/what-container) - A container technologies used to "package" up the application into a portable image that can be run nearly anywhere 
* [Cisco NX-OS](http://developer.cisco.com/nx-os) - A programmable network operating system providing many features, including running containers on the switch. 
* [Webex Teams](https://www.webex.com/team-collaboration.html) - An collaboration platform offering rich communication and programmability features allowing for robust ChatOps use cases.

Here are some videos that show the application in action:  

* <a href='https://youtu.be/iD5VrL82j6E' target="_blank">Cisco NX-OS Netbox Sync Demo1: In Action</a>

## Project Goals 
This project is not intended to cover every aspect of the network configuration, at least not the initial version. Rather my goal was to tackle a few of the common areas I see from my own network and discussions with others that would be hugely valuable for a solution like this.  Specifically this application tackles the following.  

* Ensure all VLANs identified in Netbox for the switches "site" are present on the the device with the correct name 
* Ensure interface enabled status from Netbox matches the `shut / no shut` state on the switch 
* Ensure interface descriptions from Netbox are configured on the switch 
* Ensure interface switchport configuration from Netbox are accurately deployed to the switch. Includes `access / trunk` configuration as well as access, native, and trunked VLANs. 

If a deviation is found between Netbox and the device a ChatOps message is sent to a designated room within Webex Teams. 

![](resources/chatops-example1.jpg)

> NOTE: Before using this code in your own environment, see the [Caveats / Known Issues / Later Updates](#caveats--known-issues--later-updates) Section at the end of this README. 




## Caveats / Known Issues / Later Updates
A few things to be aware of should you look to leverage this code for something within your own environment. 

* Determining which VLANs from Netbox should be configured on a specific device isn't a uniformly clear linkage within Netbox.  The code in this demonstration uses the **Site** as the connecting link.  This means that every VLAN, from all VLAN Groups, configured to be at the same Site as the switch will be installed.  If a Netbox implementation uses multiple VLAN Groups within a Site, and each device should only be tied to a particular VLAN Group you will need to update the code to support this setup.
* Currently the code only does VLAN verification in one direction, that Netbox VLANs are configured on the Switch.  If extra VLANs exist on the switch that are **NOT** in Netbox they are ignored.  