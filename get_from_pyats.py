from pyats.topology import Testbed, Device
import os
from genie.conf import Genie

# Create testbed from environment variables
build_testbed = Testbed(
    "testbed",
    alias="testbed",
    credentials={
        "default": {
            "username": os.getenv("SWITCH_USERNAME"),
            "password": os.getenv("SWITCH_PASSWORD"),
        }
    },
)
build_device = Device(
    os.getenv("SWITCH_HOSTNAME"),
    os="nxos",
    type="nxos",
    connections={"default": {"protocol": "ssh", "ip": os.getenv("SWITCH_MGMT_IP")}},
)
build_device.testbed = build_testbed
genie_testbed = Genie.init(build_testbed)

# Grab the device and connect
device = genie_testbed.devices[os.getenv("SWITCH_HOSTNAME")]
device.connect(learn_hostname=True, log_stdout=False)

def platform_info(): 
    return device.learn("platform")

def interfaces_current(): 
    interfaces = device.learn("interface")

    return interfaces.info


def vlans_current():
    vlans = device.learn("vlan").info["vlans"]
    # device_vlan_set = set([(int(vid), details["name"]) for vid, details in vlans.items()])
    return vlans
