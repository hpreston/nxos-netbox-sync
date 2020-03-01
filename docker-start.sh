#! /bin/sh 
set -e

echo "[CMD] Starting NX-OS Netbox Sync ..."

# activate workspace
# ------------------
echo "[CMD] Activating pyATS virtualenv"
source /pyats/bin/activate



# Run program 
echo "[CMD] Running check_device.py"
cd /nxos-netbox-sync
python check_device.py 
