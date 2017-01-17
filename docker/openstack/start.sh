#!/bin/sh
# On docker run, Env Variables "STACK_PASS & SERV_HOST" should be set using -e
#  example 'docker run -e "STACK_PASS=stack" -e "SERV_HOST=192.168.0.5" compute'
# or overided below by uncommenting:
#STACK_PASS="stack"
SERV_HOST="192.168.0.5"
# ODL_NETWORK should be set in the 'docker run' script
set -o nounset # throw an error if a variable is unset to prevent unexpected behaviors
ODL_NETWORK=${ODL_NETWORK}
DEVSTACK_HOME="/home/stack/devstack"
CONF_PATH=$DEVSTACK_HOME/local.conf

#Set Nameserver to google
echo nameserver 8.8.8.8 | sudo tee -a /etc/resolv.conf

# Start SSH Service
sudo service ssh start

# Start openvswitch
sudo service openvswitch-switch start

# START HERE: the following line throws an error
echo "stack:$STACK_PASS" | sudo chpasswd

# Add/Configure local.conf.compute - TODO: requires use of 'docker run -v :/home/stack/mnt
# modify the local.conf.compute according to ODL_NETWORK value
echo "Preparing $CONF_PATH for ODL=$ODL_NETWORK"
echo
if [ "$ODL_NETWORK" == "false" ] ; then
    # prepare local.conf.compute to NOT use ODL networking (default to Neutron)
    sed -i "s:^\(enable_plugin networking-odl\):#\1:g" $CONF_PATH
    sed -i "s:^\(ODL_MODE=compute\):#\1:g" $CONF_PATH
    sed -i "s:^\(ENABLED_SERVICES=\).*:\1n-cpu,q-agt:g" $CONF_PATH
else
    # prepare local.conf.compute to use ODL networking
    sed -i "s:^#\(enable_plugin networking-odl\):\1:g" $CONF_PATH
    sed -i "s:^#\(ODL_MODE=compute\):\1:g" $CONF_PATH
    sed -i "s:^\(ENABLED_SERVICES=\).*:\1n-cpu:g" $CONF_PATH
fi

sed -i "s/SERVICE_HOST=.*/SERVICE_HOST=$SERV_HOST/" $CONF_PATH

ip=`/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1`;  echo "HOST_IP=$ip" >> $CONF_PATH

$DEVSTACK_HOME/stack.sh

