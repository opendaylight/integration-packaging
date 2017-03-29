FROM debian:7

# Schema: https://github.com/projectatomic/ContainerApplicationGenericLabels
LABEL name="Int/Pack Debian Dockerfile" \
      version="5.2" \
      vendor="OpenDaylight" \
      summary="OpenDaylight Integration/Packaging example Debian Dockerfile" \
      vcs-url="https://git.opendaylight.org/gerrit/p/integration/packaging.git"

# Install OpenDaylight
RUN apt-get install -y http://download.opensuse.org/repositories/home:/akshitajha/xUbuntu_16.04/all/opendaylight_5.0.0-1_all.deb && apt-get clean

# Ports
# 8101 - Karaf SSH
# Installing additional ODL features may require opening additional ports.
# https://wiki.opendaylight.org/view/Ports
EXPOSE 8101

# Start OpenDaylight
CMD ["/opt/opendaylight/bin/karaf"]
