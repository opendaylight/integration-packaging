# SPDX-License-Identifier: EPL-1.0
##############################################################################
# Copyright (c) 2021 The Linux Foundation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
##############################################################################
#!/bin/bash -e

function setup_cluster(){
  if [ -z $ODL_REPLICAS ]; then
     echo "ODL_REPLICAS is not configured in Env field"
     exit
  fi

  hm=$(hostname)
  echo "Enable cluster for host: ${hm}"

  ## For hostname viz; odl-opendaylight-1,
  ## node_name will be 'odl-opendaylight' and node_index '1'
  node_name=${hm%-*};
  node_index=${hm##*-};
  node_list="${node_name}-0.{{ include "opendaylight.fullname" . }}.{{ .Release.Namespace }}";

  for ((i=1;i<${ODL_REPLICAS};i++));
  do
    node_list="${node_list} ${node_name}-$i.{{ include "opendaylight.fullname" . }}.{{ .Release.Namespace }}"
  done

  ${BASEDIR}/bin/configure_cluster.sh $((node_index+1)) ${node_list}
}

set -x

mountpath="{{ .Values.persistence.mountPath }}"
BASEDIR="{{ .Values.config.odl_basedir }}"
odl_prefix="/opt/opendaylight"

if [[ ! -d "$mountpath/snapshots" ]];then
  mkdir -p $mountpath/snapshots
fi

if [[ ! -d "$mountpath/data" ]];then
  mkdir -p $mountpath/data
fi

if [[ ! -d "$mountpath/segmented-journal" ]];then
  mkdir -p $mountpath/segmented-journal
fi

if [[ ! -d "$mountpath/daexim" ]];then
  mkdir -p $mountpath/daexim
fi

if [[ ! -L "$odl_prefix/snapshots" ]];then
  rm -rf $odl_prefix/snapshots && ln -s $mountpath/snapshots $odl_prefix/snapshots
fi

if [[ ! -L "$odl_prefix/data" ]];then
  rm -rf $odl_prefix/data && ln -s $mountpath/data $odl_prefix/data
fi

if [[ ! -L "$odl_prefix/segmented-journal" ]];then
  rm -rf $odl_prefix/segmented-journal && ln -s $mountpath/segmented-journal $odl_prefix/segmented-journal
fi

if [[ ! -L "$odl_prefix/daexim" ]];then
  rm -rf $odl_prefix/daexim && ln -s $mountpath/daexim $odl_prefix/daexim
fi

sed -i "s/\(featuresBoot= \|featuresBoot = \)/featuresBoot = ${FEATURES},/g" ${BASEDIR}/etc/org.apache.karaf.features.cfg
cat ${BASEDIR}/etc/org.apache.karaf.features.cfg

ODL_REPLICAS=${ODL_REPLICAS:-1}
IS_CLUSTER_ENABLED=${IS_CLUSTER_ENABLED:-false}
SLEEP_TIME=${SLEEP_TIME:-30}

if $IS_CLUSTER_ENABLED; then
  ${BASEDIR}/bin/start;
  echo "Waiting ${SLEEP_TIME} seconds for OpenDaylight to initialize";
  sleep ${SLEEP_TIME};
  setup_cluster;
  echo "Restart ODL after cluster configuration";
  ${BASEDIR}/bin/stop;
  sleep 20;
fi

echo "Starting OpenDaylight"
${BASEDIR}/bin/karaf run
