#!/bin/bash
set -x

VERSION="0.14.1"
FEATURES="odl-restconf,odl-netconf-topology"
BASEDIR=$(dirname "$0")

wget --progress=dot:mega -P /tmp https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/onap-karaf/${VERSION}/onap-karaf-${VERSION}.tar.gz
tar xzf /tmp/onap-karaf-${VERSION}.tar.gz --directory ${BASEDIR}
mv ${BASEDIR}/onap-karaf-${VERSION} ${BASEDIR}/opendaylight
sed -i "s/\(featuresBoot= \|featuresBoot = \)/featuresBoot = ${FEATURES},/g" ${BASEDIR}/opendaylight/etc/org.apache.karaf.features.cfg
cat ${BASEDIR}/opendaylight/etc/org.apache.karaf.features.cfg
