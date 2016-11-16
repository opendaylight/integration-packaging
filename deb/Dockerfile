# Dockerfile
FROM debian:jessie-backports

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y \
        build-essential \
        sudo \
        devscripts \
        equivs \
        dh-systemd \
        python-yaml \
        python-jinja2
RUN mkdir -p /build
ENTRYPOINT ["/build/build.py"]
CMD ["-h"]
