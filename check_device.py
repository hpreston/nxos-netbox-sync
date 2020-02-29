
import utils.get_from_pyats as pyats
import utils.get_from_netbox as netbox
import utils.tests as tests
from utils.webex_teams import notify_team, fail_notification
from utils.message_templates import message_vlan_exist_template, message_interface_enabled_template, message_interface_description_template, message_interface_mode_template, message_interface_vlan_template

my_name = pyats.device.hostname
my_info = pyats.platform_info()

# Say hello to room
m = notify_team(f"Device {my_name} checking in.")

print("Retrieving current status from device with pyATS")
pyats_interfaces = pyats.interfaces_current()
pyats_vlans = pyats.vlans_current()

print("Looking up intended state for device from Netbox")
netbox_interfaces = netbox.interfaces_sot()
netbox_vlans = netbox.vlans_sot()

# TEST: VLANs Exist on Switch
print("Running tests to see if VLANs from Netbox are configured")
vlan_exist_test = tests.verify_vlans_exist(netbox_vlans, pyats_vlans)
m = fail_notification(vlan_exist_test["FAIL"], message_vlan_exist_template)

# TEST: Interface Enabled Status 
print("Running interface enabled test")
interface_enabled_test = tests.verify_interface_enabled(netbox_interfaces, pyats_interfaces)
m = fail_notification(interface_enabled_test["FAIL"], message_interface_enabled_template, verify_disabled = interface_enabled_test["VERIFY_DISABLED"])

# TEST: Interface Descriptions 
print("Running interface description test")
interface_description_test = tests.verify_interface_descriptions(netbox_interfaces, pyats_interfaces)
m = fail_notification(interface_description_test["FAIL"], message_interface_description_template)

# TEST: Interface Modes 
print("Running interface mode test")
interface_mode_test = tests.verify_interface_mode(netbox_interfaces, pyats_interfaces)
m = fail_notification(interface_mode_test["FAIL"], message_interface_mode_template)

# TEST: Interface Modes 
print("Running interface vlan test")
interface_vlan_test = tests.verify_interface_vlans(netbox_interfaces, pyats_interfaces, pyats_vlans)
m = fail_notification(interface_vlan_test["FAIL"], message_interface_vlan_template)