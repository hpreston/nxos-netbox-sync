import os
from genie.testbed import load
from genie.libs.conf.vlan import Vlan
from genie.libs.conf.interface import Interface

device_details = {"devices": {
    os.getenv("SWITCH_HOSTNAME"): {
        "protocol": "ssh", 
        "ip": os.getenv("SWITCH_MGMT_IP"), 
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
        new_vlan = Vlan(vlan_id=vlan.vid, name=vlan.name)
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
        new_interface.description = interface.description
        output = new_interface.build_config() 
        results.append(output)
    
    return results    