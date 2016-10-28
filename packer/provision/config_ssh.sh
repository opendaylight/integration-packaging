#!/usr/bin/env bash
# Recent versions of OpenSSH don't support ssh-dss as an auth protocol
# ODL seems offers ssh-dss by default. To SSH to the Karaf shell, tell
# SSH to accept ssh-dss. Alternatively, tell SSH to accept ssh-dss via
# the HostKeyAlgorithms option at invocation.
#   ssh -p 8101 -oHostKeyAlgorithms=+ssh-dss karaf@localhost

# Options:
#   -x: Echo commands
#   -e: Fail on errors
set -ex

# Accept ssh-dss as an SSH algorithm by appending config to end of file
sudo sed -i -e "\$aHostKeyAlgorithms=+ssh-dss" /etc/ssh/ssh_config
