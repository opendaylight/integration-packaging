#!/bin/bash
# On docker run, Env Variables "STACK_PASS & SERVICE_HOST" should be set using -e
#  example 'docker run -e "STACK_PASS=stack" -e "SERVICE_HOST=192.168.0.5" compute'
set -o nounset # throw an error if a variable is unset to prevent unexpected behaviors
# the following variables should be overridden at runtime with docker run -e "..."
# ODL_NETWORK, SERVICE_HOST
ODL_NETWORK=${ODL_NETWORK:-True}
SERVICE_HOST=${SERVICE_HOST:-"192.168.1.2"}
STACK_PASS=stack
DEVSTACK_HOME="/home/stack/devstack"
CONF_PATH=$DEVSTACK_HOME/local.conf
BRANCH_NAME=stable/newton
TAG_NAME="origin/${BRANCH_NAME}"

#Set Nameserver to google
[ -z "$(grep "8.8.8.8" /etc/resolv.conf )" ] && echo nameserver 8.8.8.8 | sudo tee -a /etc/resolv.conf

# change the stack user password
echo "stack:$STACK_PASS" | sudo chpasswd

# get container IP for mgmt network interface
ip=`/sbin/ip -o -4 addr list ethphys01 | awk '{print $4}' | cut -d/ -f1`

# remove OVS db (for case of restacking a node to regenerate UUID)
sudo /usr/share/openvswitch/scripts/ovs-ctl stop
sudo rm -rf /etc/openvswitch/conf.db
# remove any dead screen sessions from previous stacking
screen -wipe

# set the correct branch in devstack
cd $DEVSTACK_HOME || exit
# shellcheck disable=SC2063
[ -z "$(git branch -a | grep "* ${BRANCH_NAME}")" ] && \
        git fetch && \
        git checkout -b ${BRANCH_NAME} -t ${TAG_NAME}

# copy local.conf into devstack and customize, based on environment including:
# ODL_NETWORK, ip, DEVSTACK_HOME, SERVICE_HOST
cp /home/stack/local.conf $CONF_PATH

# Configure local.conf
# update the ip of this host & SERVICE_HOST
sed -i "s/HOST_IP=.*/HOST_IP=${ip}/" $CONF_PATH
sed -i "s/SERVICE_HOST=.*/SERVICE_HOST=$SERVICE_HOST/" $CONF_PATH

$DEVSTACK_HOME/stack.sh

# write a marker file to indicate successful stacking
if [ $? = 0 ] ; then
    echo "$(hostname) stacking successful at $(date)" >> stacking.status
    /home/stack/devstack/tools/info.sh >> stacking.status
    # set devstack to OFFLINE mode after a successful stack
    sed -i "s/^#.*\(OFFLINE=True\)/\1/g" /home/stack/$SRC_CONF
    sed -i "s/^#.*\(RECLONE=False\)/\1/g" /home/stack/$SRC_CONF
fi

# vim set et ts=4 sw=4 :
