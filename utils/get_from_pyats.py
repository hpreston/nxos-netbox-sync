import os
from genie.testbed import load
from genie.libs.conf.vlan import Vlan
from genie.libs.conf.interface import Interface

device_details = {"devices": {
    os.getenv("SWITCH_HOSTNAME"): {
        "protocol": "ssh", 
        "ip": os.getenv("SWITCH_MGMT_IP"), 
        "port": os.getenv("SWITCH_MGMT_PORT", default=22), 
        "username": os.getenv("SWITCH_USERNAME"),
        "password": os.getenv("SWITCH_PASSWORD"),
        "os":"nxos",
        "ssh_options": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null",
    }
}
}
testbed = load(device_details)
device = testbed.devices[os.getenv("SWITCH_HOSTNAME")]
# device.connect(learn_hostname=True)
device.connect(learn_hostname=True, log_stdout=False, ssh_options='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null')

def platform_info(): 
    return device.learn("platform")

def interfaces_current(): 
    interfaces = device.learn("interface")

    return interfaces.info


def vlans_current():
    vlans = device.learn("vlan").info["vlans"]
    # device_vlan_set = set([(int(vid), details["name"]) for vid, details in vlans.items()])
    return vlans


def vlans_configure(netbox_vlans): 
    results = []
    for vlan in netbox_vlans: 
        print(f"Creating {vlan.display_name}")
        new_vlan = Vlan(vlan_id=str(vlan.vid), name=vlan.name)
        device.add_feature(new_vlan)
        output = new_vlan.build_config()
        results.append({vlan.name: output})
    
    # output = testbed.build_config()
    # return output
    
    return results

def vlans_remove(netbox_vlans): 
    results = []
    for vlan in netbox_vlans: 
        print(f"Removing {vlan.display_name}")
        new_vlan = Vlan(vlan_id=vlan.vid, name=vlan.name)
        device.add_feature(new_vlan)
        output = new_vlan.build_unconfig()
        results.append({vlan.name: output})
    
    return results

def interface_enable_state_configure(netbox_interfaces): 
    results = []
    for interface in netbox_interfaces: 
        print(f"Setting Interface {interface.name} to enabled state {interface.enabled}")
        if interface.name in device.interfaces.keys(): 
            new_interface = device.interfaces[interface.name]
        else: 
            new_interface = Interface(name=interface.name, device = device)
        new_interface.enabled = interface.enabled
        output = new_interface.build_config() 
        results.append(output)
    
    return results

def interface_description_configure(netbox_interfaces): 
    results = []
    for interface in netbox_interfaces: 
        print(f"Setting Interface {interface.name} description")
        if interface.name in device.interfaces.keys(): 
            new_interface = device.interfaces[interface.name]
        else: 
            new_interface = Interface(name=interface.name, device = device)

        if interface.description in ["", " ", None]: 
            output = new_interface.build_unconfig(attributes={'description':None}, apply=False)
        elif interface.description: 
            new_interface.description = interface.description
            output = new_interface.build_config() 
        results.append(output)
    
    return results    


def interface_switchport_configure(netbox_interfaces): 
    results = []
    for interface in netbox_interfaces: 
        print(f"Updating Interface {interface.name} mode to {interface.mode}")

        if interface.mode.label in ["Tagged", "Tagged All"]: 
            # new_interface.switchport_mode = "trunk"
            new_interface=interface_trunk_configure(interface)

        elif interface.mode.label == "Access": 
            # new_interface.switchport_mode = "access"
            new_interface=interface_access_configure(interface)

        else: 
            print("  Problem configuring switchport mode to match netbox")

        output = new_interface.build_config() 
        results.append(output)
    
    return results

def interface_trunk_configure(netbox_interface): 
    if netbox_interface.mode.label in ["Tagged", "Tagged All"]:
        # Configure native and tagged vlans on a trunk 
        if netbox_interface.name in device.interfaces.keys(): 
            new_interface = device.interfaces[netbox_interface.name]
        else: 
            new_interface = Interface(name=netbox_interface.name, device = device)
        new_interface.switchport_enable = True 

        new_interface.switchport_mode = "trunk"

        if netbox_interface.untagged_vlan: 
            new_interface.native_vlan = str(netbox_interface.untagged_vlan.vid)
        
        if netbox_interface.tagged_vlans: 
            vlan_list = [str(vlan.vid) for vlan in netbox_interface.tagged_vlans]
            new_interface.trunk_vlans = ",".join(vlan_list)

        if netbox_interface.mode.label == "Tagged All": 
            new_interface.trunk_add_vlans = "1-4094"

        return new_interface

    else: 
        print(f"Interface {netbox_interface.name} is NOT a trunk interface.")
        return False

def interface_access_configure(netbox_interface): 
    if netbox_interface.mode.label == "Access":
        # Configure native and tagged vlans on a trunk 
        if netbox_interface.name in device.interfaces.keys(): 
            new_interface = device.interfaces[netbox_interface.name]
        else: 
            new_interface = Interface(name=netbox_interface.name, device = device)
        new_interface.switchport_enable = True 

        new_interface.switchport_mode = "access"
        new_interface.access_vlan = str(netbox_interface.untagged_vlan.vid)
        return new_interface
    else: 
        print(f"Interface {netbox_interface.name} is NOT an access interface.")
        return False