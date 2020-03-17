# Create a testbed for the DevNet Always On NX-OS Sandbox
from genie.testbed import load

device_details = {'devices': {'sbx-n9kv-ao': {
   'protocol': 'ssh',
   'ip': 'sbx-nxos-mgmt.cisco.com',
   'port': '8181',
   'username': 'admin',
   'password': 'Admin_1234!',
   'os': 'nxos'}
   }
}

testbed = load(device_details)

# Connect to the switch and create variable called device 
device = testbed.devices['sbx-n9kv-ao']
device.connect(learn_hostname=True)

# Review: Using genie.ops to "learn" operational and configuration details 
vlans = device.learn("vlan").info["vlans"]

vlans["101"]
vlans["101"]["interfaces"]

interfaces = device.learn("interface").info

interfaces["Ethernet1/3"]
interfaces["Ethernet1/3"]["enabled"]
interfaces["Ethernet1/3"]["oper_status"]
interfaces["Ethernet1/3"]["counters"]["out_errors"]
interfaces["Ethernet1/3"]["switchport_mode"]
interfaces["Ethernet1/3"]["access_vlan"]

# Demo: Using genie.conf to configure vlans and interfaces 
from genie.libs.conf.vlan import Vlan
from genie.libs.conf.interface import Interface

# Create new Vlan object 
new_vlan = Vlan(vlan_id = "3001", name = "GenieConfigured")

# Add new vlan to device as a feature 
device.add_feature(new_vlan)
new_vlan.devices

# Build the configuration for the vlan, but don't send to device
output = new_vlan.build_config(apply = False)
output 
print(output["sbx-n9kv-ao"])

# Build and send the configuration to devices 
output = new_vlan.build_config(apply = True)

# Build and print out the configuraiton to REMOVE the Vlan from the devices
output = new_vlan.build_unconfig(apply = False)
print(output["sbx-n9kv-ao"])

# Build and send the configuration to remove the Vlan from the device 
output = new_vlan.build_unconfig()

# Create a new Interface object for the device 
new_interface = Interface(name = "Ethernet1/10", device = device)

# Configure interface properties 
new_interface.description = "Genie set me!"
new_interface.enabled = False 
new_interface.switchport_enable = True 
new_interface.switchport_mode = "trunk"
new_interface.native_vlan = "101"
new_interface.trunk_vlans = "101-105"

# Build and print out the configuration 
output = new_interface.build_config(apply = False)
print(output)

# Build and send the configuration to the device 
output = new_interface.build_config()

# Build and print the configuration to UNCONFIG the interface 
output = new_interface.build_unconfig(apply = False)
print(output)

# Build and send the UNCONFIG 
output = new_interface.build_unconfig()

# Disconnect from the device 
device.disconnect()
