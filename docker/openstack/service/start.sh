#!/bin/sh
# On docker run, Env Variables "STACK_PASS & SERV_HOST" should be set using -e
#  example 'docker run -e "STACK_PASS=stack" -e "SERV_HOST=192.168.0.5" compute'
# or overided below by uncommenting:
STACK_PASS="stack"
SERV_HOST="192.168.0.5"
# ODL_NETWORK should be set in the 'docker run' script
set -o nounset # throw an error if a variable is unset to prevent unexpected behaviors
ODL_NETWORK=${ODL_NETWORK}
DEVSTACK_HOME="/home/stack/devstack"
CONF_PATH=$DEVSTACK_HOME/local.conf
BRANCH_NAME=stable/newton
TAG_NAME="origin/stable/${BRANCH_NAME}"

#Set Nameserver to google
echo nameserver 8.8.8.8 | sudo tee -a /etc/resolv.conf

# change the stack user password
echo "stack:$STACK_PASS" | sudo chpasswd

# get container IP
ip=`/sbin/ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1`
# fix address binding issue in mysql
sudo sed -i 's:^bind-address.*:#&:' /etc/mysql/my.cnf

# allow services to start
sudo sed -i 's:^exit .*:exit 0:' /usr/sbin/policy-rc.d

# set the correct branch in devstack
cd $DEVSTACK_HOME
git checkout -b ${BRANCH_NAME} -t ${TAG_NAME}

# copy local.conf into devstack and customize, based on environment including:
# ODL_NETWORK, ip, DEVSTACK_HOME, SERV_HOST
cp /home/stack/local.conf $CONF_PATH

# Configure local.conf
# update the ip of this host
sed -i "s:\(HOST_IP=\).*:\1${ip}:" $CONF_PATH
sed -i "s:\(SERVICE_HOST=\).*:\1${ip}:" $CONF_PATH
# modify the local.conf according to ODL_NETWORK value
echo "Preparing $CONF_PATH for ODL=$ODL_NETWORK"
echo
if [ "$ODL_NETWORK" = "false" ] ; then
    # prepare local.conf to NOT use ODL networking (default to Neutron)
    sed -i "s:^#\(enable_service q-agt\).*:\1:g" $CONF_PATH
    sed -i "s:^\(enable_plugin networking-odl\):#\1:g" $CONF_PATH
    sed -i "s:^\(Q_ML2_PLUGIN_MECHANISM_DRIVERS=opendaylight\).*:#\1:g" $CONF_PATH
else
    # prepare local.conf to use ODL networking
    sed -i "s:^\(enable_service q-agt\):#\1:g" $CONF_PATH
    sed -i "s:^#\(enable_plugin networking-odl\):\1:g" $CONF_PATH
    sed -i "s:^#\(Q_ML2_PLUGIN_MECHANISM_DRIVERS=opendaylight\).*:\1:g" $CONF_PATH
fi

# begin stacking
$DEVSTACK_HOME/stack.sh

