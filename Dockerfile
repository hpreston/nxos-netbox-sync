FROM ciscotestautomation/pyats:20.2-alpine 
LABEL maintainer="hapresto@cisco.com"

# Make directories for project 
WORKDIR /nxos-netbox-sync 
RUN mkdir utils 
RUN mkdir templates

# Copy in requirements and install 
COPY requirements.txt requirements.txt 
RUN source /pyats/bin/activate && pip install -r requirements.txt 

# Copy in /root/.ssh/config file to accept keys 
# Due to pyats stalling at accept key at connect 
COPY container_ssh.config /root/.ssh/config 

# Copy in code files 
COPY utils utils
COPY templates templates 
COPY check_device.py .

# Copy in entrypoint code 
COPY docker-start.sh docker-start.sh

# Start Command
CMD ["/nxos-netbox-sync/docker-start.sh"]
