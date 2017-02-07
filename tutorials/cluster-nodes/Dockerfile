##############################################################################
# Copyright (c) 2017 Alexis de Talhouët.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

FROM ubuntu:trusty

# As we can't mount folders through docker-compose without
# having them in sync with the host, we're using a
# Dockerfile to bypass this limitation

COPY opendaylight /root/opendaylight
COPY scripts /root/scripts