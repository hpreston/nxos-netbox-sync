

def verify_vlans_exist(netbox_vlans, pyats_vlans): 
    results = {
        "status": False, 
        "PASS": [], 
        "FAIL": [],
    }
    for vlan in netbox_vlans: 
        if str(vlan.vid) in pyats_vlans.keys(): 
            # print(f"✅ {vlan.vid} exists on switch")
            if vlan.name == pyats_vlans[str(vlan.vid)]["name"]: 
                print(f"✅ {vlan.display_name} exists with correct name on switch")
                results["PASS"].append(vlan)
            else: 
                print(f"❌ {vlan.display_name} exists but with WRONG name on switch")
                results["FAIL"].append(vlan)
        else: 
            print(f"❌ {vlan.vid} MISSING from switch")
            results["FAIL"].append(vlan)

    return results

def verify_interface_enabled(netbox_interfaces, pyats_interfaces):
    results = {
        "status": False, 
        "PASS": [], 
        "FAIL": [],
        "VERIFY_DISABLED": []
    }

    for interface in netbox_interfaces: 
        if interface.enabled: 
            interface_status = "Enabled"
        else: 
            interface_status = "Disabled"

        # NOTE: Current bug in Genie model reports an interface as "enabled": False even if 
        #       the interface is "no shut". Reported to team.. will need to skip tests for 
        #       interfaces that are Enabled on the device, when they should be disabled.
        if interface.name in pyats_interfaces.keys(): 
            # print(f"✅ {interface.name} found on switch")
            if interface.enabled:
                if pyats_interfaces[interface.name]["enabled"]:
                    # Test 1: NB Enabled - pyATS enabled and oper_status up
                    if pyats_interfaces[interface.name]["oper_status"] == "up": 
                        print(f"✅ {interface.name} was correctly found to be UP/UP on switch")
                        results["PASS"].append(interface)
                    # Test 2: NB Enabled - pyATS enabled and oper_status down
                    elif pyats_interfaces[interface.name]["oper_status"] == "down": 
                        print(f"❌ {interface.name} was incorrectly found to be UP/DOWN on switch")
                        results["PASS"].append(interface)
                # Test 3: NB Enabled - pyATS disabled
                elif not pyats_interfaces[interface.name]["enabled"]:
                    print(f"❌ {interface.name} was incorrectly found to be DOWN/DOWN on switch")
                    results["PASS"].append(interface)
            # See note above.. skipping these tests for now as they are inaccurate
            elif not interface.enabled: 
                if pyats_interfaces[interface.name]["enabled"]:
                    # Test 4: NB DISABLED - pyATS enabled and oper_status up
                    if pyats_interfaces[interface.name]["oper_status"] == "up": 
                        print(f"❌ {interface.name} was incorrectly found to be UP/UP on switch")
                        results["FAIL"].append(interface)
                    # See note above.. skipping these tests for now as they are inaccurate
                    # Test 5: NB DISABLED - pyATS enabled and oper_status down
                    # elif pyats_interfaces[interface.name]["oper_status"] == "down": 
                    #     print(f"❌ {interface.name} was incorrectly found to be UP/DOWN on switch")
                # See note above.. skipping these tests for now as they are inaccurate
                # Test 6: NB DISABLED - pyATS disabled
                # elif not pyats_interfaces[interface.name]["enabled"]:
                #     print(f"✅ {interface.name} was correctly found to be DOWN/DOWN on switch")
                results["VERIFY_DISABLED"].append(interface)

        else: 
            print(f"❌ {interface.name} MISSING from switch")
            results["FAIL"].append(interface)

    return results

def verify_interface_descriptions(netbox_interfaces, pyats_interfaces):
    results = {
        "status": False, 
        "PASS": [], 
        "FAIL": [],
    }

    for interface in netbox_interfaces: 
        if interface.name in pyats_interfaces.keys(): 
            # If there is a description configured in Netbox 
            if len(interface.description) > 0: 
                if "description" in pyats_interfaces[interface.name].keys():
                    if interface.description == pyats_interfaces[interface.name]: 
                        print(f"✅ {interface.name} has the correct description configured on switch")
                        results["PASS"].append(interface)
                    else: 
                        print(f"""❌ {interface.name} incorrectly has the description '{pyats_interfaces[interface.name]["description"]}' on switch. It should be '{interface.description}'""")
                        results["FAIL"].append(interface)
                else: 
                    print(f"""❌ {interface.name} incorrectly has NO description configured on switch. It should be '{interface.description}'""")
                    results["FAIL"].append(interface)


            # No description on Netbox 
            else: 
                if "description" not in pyats_interfaces[interface.name].keys(): 
                    print(f"✅ {interface.name} correctly has NO description on switch")
                    results["PASS"].append(interface)
                else: 
                    print(f"""❌ {interface.name} incorrectly has the description '{pyats_interfaces[interface.name]["description"]}' on switch""")
                    results["PASS"].append(interface)

        else: 
            print(f"❌ {interface.name} MISSING from switch")
            results["FAIL"].append(interface)

    return results


def verify_interface_mode(netbox_interfaces, pyats_interfaces):
    results = {
        "status": False, 
        "PASS": [], 
        "FAIL": [],
        "SKIPPED": [],
    }

    for interface in netbox_interfaces: 
        if interface.name in pyats_interfaces.keys(): 
            # Checking Layer 2 Interfaces: ie interface.mode != None
            if interface.mode: 
                # Check Trunk Status: Tagged or Tagged All
                if interface.mode.label in ["Tagged", "Tagged All"]: 
                    if "switchport_enable" in pyats_interfaces[interface.name].keys() and pyats_interfaces[interface.name]["switchport_enable"]: 
                        if pyats_interfaces[interface.name]["switchport_mode"] == "trunk": 
                            print(f"✅ {interface.name} is correctly configured as a trunk")
                            results["PASS"].append(interface)
                        elif pyats_interfaces[interface.name]["switchport_mode"] == "access": 
                            print(f"❌ {interface.name} is incorrectly configured as an access port")
                            results["FAIL"].append(interface)
                # Check Access Status: Access
                elif interface.mode.label == "Access": 
                    if "switchport_enable" in pyats_interfaces[interface.name].keys() and pyats_interfaces[interface.name]["switchport_enable"]: 
                        if pyats_interfaces[interface.name]["switchport_mode"] == "access": 
                            print(f"✅ {interface.name} is correctly configured as an access port")
                            results["PASS"].append(interface)
                        elif pyats_interfaces[interface.name]["switchport_mode"] == "trunk": 
                            print(f"❌ {interface.name} is incorrectly configured as a trunk")
                            results["FAIL"].append(interface)
            # TODO: Update to check for an IP address on interface and verify L3 status
            else: 
                results["SKIPPED"].append(interface)
        else: 
            print(f"❌ {interface.name} MISSING from switch")
            results["FAIL"].append(interface)

    return results    