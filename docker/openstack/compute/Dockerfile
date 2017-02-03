FROM 		ubuntu:14.04
MAINTAINER	OpenDaylight Int/Test Project Team <integration-dev@lists.opendaylight.org>

ENV		PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Add stack user
RUN		groupadd stack && \
		useradd -g stack -s /bin/bash -m stack && \
		echo "stack ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Install git and sshd
RUN 		apt-get update && \
		apt-get install -y --no-install-recommends git \
		openssh-server ca-certificates openvswitch-common \
		openvswitch-switch dbus && \
		rm -rf /var/lib/apt/lists/*

# Get devstack
USER		stack
RUN		git clone https://git.openstack.org/openstack-dev/devstack \
		/home/stack/devstack
# Copy and chown local.conf to stack
COPY 		local.conf /home/stack/devstack/
RUN 		sudo chown stack:stack /home/stack/devstack/local.conf

# Copy start.sh and chown to stack
COPY		start.sh /home/stack/
RUN		sudo chown stack:stack /home/stack/start.sh && chmod 766 /home/stack/start.sh

CMD		["/home/stack/start.sh"]

# vim: set ft=dockerfile noet sw=4 ts=4 :
