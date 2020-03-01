import os
from genie.testbed import load

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
