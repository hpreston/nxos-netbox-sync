

docker-build: 
	docker build -t hpreston/nxos-netbox-sync:latest .

docker-shell: 
	source src_env && \
	docker run --rm -it \
	-e NETBOX_URL="${NETBOX_URL}" \
	-e NETBOX_TOKEN="${NETBOX_TOKEN}" \
	-e SWITCH_HOSTNAME="${SWITCH_HOSTNAME}" \
	-e SWITCH_MGMT_IP="${SWITCH_MGMT_IP}" \
	-e SWITCH_USERNAME="${SWITCH_USERNAME}" \
	-e SWITCH_PASSWORD="${SWITCH_PASSWORD}" \
	-e TEAMS_TOKEN="${TEAMS_TOKEN}" \
	-e TEAMS_ROOMID="${TEAMS_ROOMID}" \
	hpreston/nxos-netbox-sync:latest /bin/sh

docker-run: 
	source src_env && \
	docker run --rm -it \
	-e NETBOX_URL="${NETBOX_URL}" \
	-e NETBOX_TOKEN="${NETBOX_TOKEN}" \
	-e SWITCH_HOSTNAME="${SWITCH_HOSTNAME}" \
	-e SWITCH_MGMT_IP="${SWITCH_MGMT_IP}" \
	-e SWITCH_USERNAME="${SWITCH_USERNAME}" \
	-e SWITCH_PASSWORD="${SWITCH_PASSWORD}" \
	-e TEAMS_TOKEN="${TEAMS_TOKEN}" \
	-e TEAMS_ROOMID="${TEAMS_ROOMID}" \
	hpreston/nxos-netbox-sync:latest 
