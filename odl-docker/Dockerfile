# SPDX-License-Identifier: EPL-1.0
##############################################################################
# Copyright (c) 2021 The Linux Foundation and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
##############################################################################

FROM openjdk:11-jdk-slim AS stage0

USER root

RUN set -eux \
    && cd $HOME \
    && apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /opt/opendaylight \
    && jlink --add-modules java.base,java.compiler,java.desktop,java.logging,java.management,java.naming,java.rmi,java.security.sasl,java.sql,java.xml,jdk.jfr,jdk.naming.rmi,jdk.xml.dom,jdk.unsupported --output /opt/openjdk-11 \
    && rm -rf /usr/local/openjdk-11 

COPY start_docker.sh /opt/opendaylight

FROM scratch as stage1

ENV JAVA_HOME /opt/openjdk-11
ENV PATH $PATH:$JAVA_HOME/bin
ENV FEATURES odl-restconf-all

WORKDIR /opt/opendaylight

COPY --from=stage0 / /

RUN set -eux \
    && curl https://nexus.opendaylight.org/content/repositories/opendaylight.release/org/opendaylight/integration/opendaylight/15.2.0/opendaylight-15.2.0.tar.gz | tar zxf - -C /opt/opendaylight/ --strip-components 1 \
    && groupadd -r karaf --gid=8181 \
    && useradd -rm -g karaf --uid=8181 karaf \
    && chown -R karaf:karaf /opt/opendaylight 

USER karaf

EXPOSE 8101
EXPOSE 8181

CMD ./start_docker.sh
