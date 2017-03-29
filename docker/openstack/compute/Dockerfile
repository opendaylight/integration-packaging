FROM ubuntu:14.04

# Schema: https://github.com/projectatomic/ContainerApplicationGenericLabels
LABEL name="Int/Pack OpenStack Compute Node" \
      version="0.1" \
      vendor="OpenDaylight" \
      summary="OpenStack compute node for scale testing" \
      vcs-url="https://git.opendaylight.org/gerrit/p/integration/packaging.git"

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    DEBIAN_FRONTEND=noninteractive

# Install devstack dependencies
# Start ignoring DockerfileLintBear
RUN apt-get install -y --no-install-recommends \
    git \
    openssh-server \
    ca-certificates \
    openvswitch-common \
    openvswitch-switch \
    dbus && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Stop ignoring

# Add stack user
RUN groupadd stack && \
    useradd -g stack -s /bin/bash -m stack && \
    echo "stack ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Get devstack
USER stack
RUN git clone https://git.openstack.org/openstack-dev/devstack /home/stack/devstack

# Copy and chown local.conf to stack
COPY local.conf /home/stack/local.conf
RUN sudo chown stack:stack /home/stack/local.conf

# Copy start.sh and chown to stack
COPY start.sh /home/stack/start.sh
RUN sudo chown stack:stack /home/stack/start.sh && chmod 766 /home/stack/start.sh

# Open Horizon port
EXPOSE 80

CMD ["/home/stack/start.sh"]

# vim: set ft=dockerfile sw=4 ts=4 :
