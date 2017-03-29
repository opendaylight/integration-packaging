##############################################################################
# Copyright (c) 2017 Alexis de Talhouët.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

FROM ubuntu:trusty

# Schema: https://github.com/projectatomic/ContainerApplicationGenericLabels
LABEL name="OpenDaylght Clustering Tutorial" \
      version="0.1" \
      vendor="OpenDaylight" \
      summary="Integration/Packaging cluster deployment tutorial" \
      vcs-url="https://git.opendaylight.org/gerrit/p/integration/packaging.git"

# As we can't mount folders through docker-compose without
# having them in sync with the host, we're using a
# Dockerfile to bypass this limitation

# ODL Karaf SSH port
EXPOSE 8101

COPY opendaylight /root/opendaylight
COPY scripts /root/scripts

CMD ["bash"]
