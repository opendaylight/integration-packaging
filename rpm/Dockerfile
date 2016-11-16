FROM centos:centos7

RUN yum -y update && yum -y install epel-release
RUN yum -y install fedora-packager \
    python-pip \
    && yum clean all
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt
RUN useradd builder
RUN usermod -a -G mock builder
RUN mkdir -p /build
USER builder
ENTRYPOINT ["/build/build.py"]
CMD ["-h"]
