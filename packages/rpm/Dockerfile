FROM centos:7

# Schema: https://github.com/projectatomic/ContainerApplicationGenericLabels
LABEL name="Int/Pack deb-building container" \
      version="0.1" \
      vendor="OpenDaylight" \
      summary="ODL Integration/Packaging container for building .debs" \
      vcs-url="https://git.opendaylight.org/gerrit/p/integration/packaging.git"

# Install system-level requirements
RUN yum install -y epel-release && yum clean all
RUN yum install -y fedora-packager \
    python-pip \
    && yum clean all

# Create user to do the build, add them to mock group
RUN useradd builder
RUN usermod -a -G mock builder

# Install requirements managed by pip
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# ODL Karaf SSH port
EXPOSE 8101

RUN mkdir -p /build
ENTRYPOINT ["/build/build.py"]
CMD ["-h"]
