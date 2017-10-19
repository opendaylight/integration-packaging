FROM centos:7

# Schema: https://github.com/projectatomic/ContainerApplicationGenericLabels
LABEL name="Int/Pack CentOS Dockerfile" \
      version="7.0" \
      vendor="OpenDaylight" \
      summary="OpenDaylight Integration/Packaging example CentOS Dockerfile" \
      vcs-url="https://git.opendaylight.org/gerrit/p/integration/packaging.git"

# Install OpenDaylight
RUN yum install -y http://cbs.centos.org/repos/nfv7-opendaylight-70-release/x86_64/os/Packages/opendaylight-7.0.0-1.el7.noarch.rpm && yum clean all

# Ports
# 8101 - Karaf SSH
# Installing additional ODL features may require opening additional ports.
# https://wiki.opendaylight.org/view/Ports
EXPOSE 8101

# Start OpenDaylight
CMD ["/opt/opendaylight/bin/karaf"]
