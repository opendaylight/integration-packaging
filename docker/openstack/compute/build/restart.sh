#!/bin/bash
# file: restart.sh
# Restart/restack in a container that has already run DEVstack and start.sh
# restart.sh can safely be used instead of start.sh

# unstack first
echo "[$(date)] S3P::${0}:: unstacking..."
/home/stack/devstack/unstack.sh
rm -rf /home/stack/stacking.status

if [[ "$1" == "clean" ]] ; then
    /home/stack/devstack/clean.sh
    rm -rf /opt/stack/*
fi

# restart
echo "[$(date)] ${0} :: stacking..."
/home/stack/start.sh
