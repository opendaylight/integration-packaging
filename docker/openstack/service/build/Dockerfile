FROM odl-registry:4000/s3p/systemd:v0.1

# Schema: https://github.com/projectatomic/ContainerApplicationGenericLabels
LABEL name="Int/Pack OpenStack Control Node" \
      version="0.1" \
      vendor="OpenDaylight" \
      summary="OpenStack control node for scale testing" \
      vcs-url="https://git.opendaylight.org/gerrit/p/integration/packaging.git"

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
    DEBIAN_FRONTEND=noninteractive \
    container=docker

# Install devstack dependencies
# Start ignoring DockerfileLintBear
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    git \
    iproute2 \
    iptables \
    lsb-release \
    net-tools \
    sudo \
    vim && \
    rm -rf /var/lib/apt/lists/*
# Stop ignoring

# remove nologin to allow ssh
RUN     rm -rf /var/run/nologin

# Add stack user
RUN groupadd stack && \
    useradd -g stack -s /bin/bash -m stack && \
    echo "stack ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    echo "stack:stack" | chpasswd

# Get devstack
RUN git clone https://git.openstack.org/openstack-dev/devstack /home/stack/devstack

# copy local.conf & scripts
COPY local.conf /home/stack/local.conf
COPY start.sh /home/stack/start.sh
COPY restart.sh /home/stack/restart.sh
RUN chown -R stack:stack /home/stack && \
    chmod 766 /home/stack/start.sh && \
    chmod 766 /home/stack/restart.sh

WORKDIR /home/stack

CMD ["/home/stack/start.sh"]

# vim: set ft=dockerfile sw=4 ts=4 :

