import pynetbox 
import yaml 
import os 

data_file = "server_initial.yaml"

with open(data_file) as f: 
    data = yaml.safe_load(f.read())

nb_url = os.getenv("NETBOX_URL")
nb_token = os.getenv("NETBOX_TOKEN")

nb = pynetbox.api(url=nb_url, token=nb_token)

# List of Interfaces Types
interface_type = {
    "1000BASE-T (1GE)": 1000,
    "10GBASE-T (10GE)": 1150,
    "Virtual": 0,
    "Link Aggregation Group (LAG)": 200,
}

# devices
for device in data["devices"]: 
    print(f"Creating or Updating device {device['name']}")
    nb_device = nb.dcim.devices.get(name=device["name"])
    if not nb_device: 
        nb_device = nb.dcim.devices.create(
            name=device["name"], 
            #manufacturer=nb.dcim.manufacturers.get(slug=device["manufacturer_slug"]).id, 
            site=nb.dcim.sites.get(slug=device["site_slug"]).id,
            device_role=nb.dcim.device_roles.get(slug=device["device_role_slug"]).id, 
            device_type=nb.dcim.device_types.get(slug=device["device_types_slug"]).id,
            #ansible_ssh_ip=nb.dcim.devices.filter(name=device["name"],custom_fields=device["ansible_ssh_ip"]) 
            )
    else:
        nb_device.update({
        "name": device["name"], 
        "site" : nb.dcim.sites.get(slug=device["site_slug"]).id,
        "device_role": nb.dcim.device_roles.get(slug=device["device_role_slug"]).id, 
        "device_type": nb.dcim.device_types.get(slug=device["device_types_slug"]).id, 
        })
    for interface in device["interfaces"]: 
        print(f"  Creating or updating interface {interface['name']}")
        nb_interface = nb.dcim.interfaces.get(
            device_id=nb_device.id, 
            name=interface["name"]
        )
        if not nb_interface: 
            nb_interface = nb.dcim.interfaces.create(
                device=nb_device.id, 
                name=interface["name"],
                type=interface_type[interface["type"]] 
            )
        else:
            nb_interface.update({
                "device": nb_device.id, 
                "name": interface["name"],
                "type": interface_type[interface["type"]] 
            })
        if "description" in interface.keys():
            nb_interface.description = interface["description"]
        if "mgmt_only" in interface.keys():
            nb_interface.mgmt_only = interface["mgmt_only"]
        if "enabled" in interface.keys():
            nb_interface.enabled = interface["enabled"]
        if "lag" in interface.keys():
            nb_interface.lag = nb.dcim.interfaces.get(name=interface["lag"],device=device["name"]).id
        if "ip_addresses" in interface.keys(): 
            for ip in interface["ip_addresses"]: 
                print(f"  Adding IP {ip['address']}")
                nb_ipadd = nb.ipam.ip_addresses.get(
                    address = ip["address"],
                    description=  ip["description"],
                )
                if not nb_ipadd: 
                    nb_ipadd = nb.ipam.ip_addresses.create(
                        address = ip["address"],
                        description=  ip["description"],
                    )
                # else:
                #     nb_ipadd.update({
                #         "address": ip["address"],
                #         "description":  ip["description"],
                #     })
                nb_ipadd.interface = nb_interface.id
                nb_ipadd.save()
                if "primary" in ip.keys(): 
                    nb_device.primary_ip4 = nb_ipadd.id
                    nb_device.save()
        
        nb_interface.save()

#interface_modes = nb.dcim.custom_choices()["interface:mode"]
# interface_mode = {
#     "Access": 100, 
#     "Tagged": 200, 
#     "Tagged All": 300,
# }

# interface_type = {
#     "1000BASE-T (1GE)": 1000,
#     "10GBASE-T (10GE)": 1150,
#     "Virtual": 0,
#     "Link Aggregation Group (LAG)": 200,
# }

# sites: 
# for site in data["sites"]: 
#     print(f"Creating or Updating Site {site['name']}")
#     nb_data = nb.dcim.sites.get(slug=site["slug"])
#     if not nb_data: 
#         nb_data = nb.dcim.sites.create(name=site["name"], slug=site["slug"])

# manufacturers 
# for manufacturer in data["manufacturers"]: 
#     print(f"Creating or Updating Manufacture {manufacturer['name']}")
#     nb_data = nb.dcim.manufacturers.get(slug=manufacturer["slug"])
#     if not nb_data: 
#         nb_data = nb.dcim.manufacturers.create(name=manufacturer["name"], slug=manufacturer["slug"])

# device_types
# for device_type in data["device_types"]: 
#     print(f"Creating or Updating device_type {device_type['model']}")
#     nb_data = nb.dcim.device_types.get(slug=device_type["slug"])
#     if not nb_data: 
#         nb_data = nb.dcim.device_types.create(
#             model=device_type["model"], 
#             slug=device_type["slug"], 
#             manufacturer=nb.dcim.manufacturers.get(slug=device_type["manufacturer_slug"]).id, 
#             height=device_type["height"]
#             )

# device_roles
# for device_role in data["device_roles"]: 
#     print(f"Creating or Updating device_role {device_role['name']}")
#     nb_data = nb.dcim.device_roles.get(slug=device_role["slug"])
#     if not nb_data: 
#         nb_data = nb.dcim.device_roles.create(
#             name=device_role["name"], 
#             slug=device_role["slug"], 
#             color=device_role["color"]
#             )

# # platforms
# for platform in data["platforms"]: 
#     print(f"Creating or Updating platform {platform['name']}")
#     nb_data = nb.dcim.platforms.get(slug=platform["slug"])
#     if not nb_data: 
#         nb_data = nb.dcim.platforms.create(
#             name=platform["name"], 
#             slug=platform["slug"], 
#             manufacturer=nb.dcim.manufacturers.get(slug=platform["manufacturer_slug"]).id, 
#             )

# # vrfs 
# for vrf in data["vrfs"]: 
#     print(f"Creating or Updating vrf {vrf['name']}")
#     nb_data = nb.ipam.vrfs.get(rd=vrf["rd"])
#     if not nb_data: 
#         nb_data = nb.ipam.vrfs.create(name=vrf["name"], rd=vrf["rd"])

# # vlan-groups 
# for group in data["vlan_groups"]: 
#     print(f"Creating or updating vlan-group {group['name']}")
#     nb_group = nb.ipam.vlan_groups.get(slug=group["slug"])
#     if not nb_group: 
#         nb_group = nb.ipam.vlan_groups.create(
#             name = group["name"], 
#             slug = group["slug"], 
#             site=nb.dcim.sites.get(slug=group["site_slug"]).id,
#         )
#     # vlans
#     for vlan in group["vlans"]: 
#         print(f"Creating or updating vlan {vlan['name']}")
#         nb_vlan = nb.ipam.vlans.get(
#             group_id=nb_group.id, 
#             vid=vlan["vid"],
#             )
#         if not nb_vlan: 
#             nb_vlan = nb.ipam.vlans.create(
#                 group=nb_group.id, 
#                 site=nb_group.site.id, 
#                 name=vlan["name"], 
#                 vid=vlan["vid"], 
#                 description=vlan["description"], 
#             )
#         if "prefix" in vlan.keys(): 
#             print(f"Configuring prefix {vlan['prefix']}")
#             nb_prefix = nb.ipam.prefixes.get(
#                 vrf_id = nb.ipam.vrfs.get(rd=vlan["vrf"]).id, 
#                 site_id=nb_group.site.id, 
#                 vlan_vid=nb_vlan.vid, 
#             )
#             if not nb_prefix: 
#                 # print("  Creating new prefix")
#                 nb_prefix = nb.ipam.prefixes.create(
#                     prefix=vlan["prefix"], 
#                     vrf=nb.ipam.vrfs.get(rd=vlan["vrf"]).id,
#                     description=vlan["description"],
#                     site=nb_group.site.id, 
#                     vlan=nb_vlan.id
#                 )

        