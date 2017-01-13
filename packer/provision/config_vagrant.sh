#!/usr/bin/env bash
# Called by Packer to config a CentOS 7 machine for use as a Vagrant base box

# Options:
#   -x: Echo commands
#   -e: Fail on errors
set -ex

# Install SSH key used by Vagrant for all interactions that connect to the box
install -v -o vagrant -g vagrant -m 0700 -d /home/vagrant/.ssh
curl -o /home/vagrant/.ssh/authorized_keys -kL "https://raw.github.com/mitchellh/vagrant/master/keys/vagrant.pub"
chmod 600 /home/vagrant/.ssh/authorized_keys
chown -R vagrant:vagrant /home/vagrant/.ssh
