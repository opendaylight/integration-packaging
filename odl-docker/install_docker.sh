#!/bin/bash
# SPDX-License-Identifier: EPL-1.0
##############################################################################
# Copyright (c) 2021 The Linux Foundation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
##############################################################################

set -x

VERSION="14.2.0"
BASEDIR=$(dirname "$0")

wget --progress=dot:mega -P /tmp https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/opendaylight/${VERSION}/opendaylight-${VERSION}.tar.gz
tar xzf /tmp/opendaylight-${VERSION}.tar.gz --directory ${BASEDIR}
rm /tmp/opendaylight-${VERSION}.tar.gz
mv ${BASEDIR}/opendaylight-${VERSION} ${BASEDIR}/opendaylight
cp ${BASEDIR}/start_docker.sh ${BASEDIR}/opendaylight
