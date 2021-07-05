# SPDX-License-Identifier: EPL-1.0
##############################################################################
# Copyright (c) 2021 The Linux Foundation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
##############################################################################

FROM openjdk:11

WORKDIR /opt/opendaylight

ADD opendaylight .

RUN groupadd -r karaf --gid=8181 && \
    useradd -rm -g karaf --uid=8181 karaf && \
    chown -R karaf:karaf .

USER karaf
EXPOSE 8101 8181
CMD ["bin/karaf", "run"]
