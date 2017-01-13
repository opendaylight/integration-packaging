#!/bin/bash -eux

sudo yum -y remove gcc cpp kernel-devel kernel-headers perl
sudo yum -y clean all

sudo rm -f /etc/udev/rules.d/70-persistent-net.rules
if [ -r /etc/sysconfig/network-scripts/ifcfg-eth0 ]; then
  sudo sed -i 's/^HWADDR.*$//' /etc/sysconfig/network-scripts/ifcfg-eth0
  sudo sed -i 's/^UUID.*$//' /etc/sysconfig/network-scripts/ifcfg-eth0
fi
