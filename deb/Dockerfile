# Dockerfile
FROM debian:jessie-backports

# Schema: https://github.com/projectatomic/ContainerApplicationGenericLabels
LABEL name="Int/Pack deb-building container" \
      version="0.1" \
      vendor="OpenDaylight" \
      summary="ODL Integration/Packaging container for building .debs" \
      vcs-url="https://git.opendaylight.org/gerrit/p/integration/packaging.git"

ENV DEBIAN_FRONTEND noninteractive

# Install system-level requirements
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    sudo \
    devscripts \
    equivs \
    dh-systemd \
    python-yaml \
    python-jinja2 && \
    apt-get clean

# ODL Karaf SSH port
EXPOSE 8101

RUN mkdir -p /build
ENTRYPOINT ["/build/build.py"]
CMD ["-h"]
