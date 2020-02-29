from jinja2 import Template

with open("templates/notification_vlan_exist_test.j2") as f: 
    message_vlan_exist_template = Template(f.read())

with open("templates/notification_interface_enabled_test.j2") as f: 
    message_interface_enabled_template = Template(f.read())

with open("templates/notification_interface_description_test.j2") as f: 
    message_interface_description_template = Template(f.read())

with open("templates/notification_interface_mode_test.j2") as f: 
    message_interface_mode_template = Template(f.read())

with open("templates/notification_interface_vlan_test.j2") as f: 
    message_interface_vlan_template = Template(f.read())