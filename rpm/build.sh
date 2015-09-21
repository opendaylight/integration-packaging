#!/usr/bin/env sh
# Reads build info from build_vars files to build ODL RPMs and SRPMs
# This is designed to be run in the included Vagrant environment

# Echo commands as they are run
set -x

# Common paths used in this script
rpmbuild_src_dir="$HOME/rpmbuild/SOURCES/"
rpmbuild_spec_dir="$HOME/rpmbuild/SPECS/"

# Install required RPM building software and the repo that serves it
sudo yum install -y epel-release
sudo yum install -y fedora-packager

# Add user to mock group for rpmbuild
sudo usermod -a -G mock $USER

# Configure rpmbuild dir
rpmdev-setuptree

# Put ODL release tarballs in rpmbuild's SOURCES dir
cp /vagrant/cache/distribution-karaf-*.tar.gz $rpmbuild_src_dir

# Put systemd unitfiles in rpmbuild's SOURCES dir
# The RPM expects sources to be in tar archives, so package it as one
tar -C /vagrant/unitfiles/ -cz opendaylight.service -f $rpmbuild_src_dir/opendaylight.service.tar.gz

# Put ODL RPM .spec files in rpmbuild's SPECS dir
cp /vagrant/specs/opendaylight-*.spec $rpmbuild_spec_dir

build()
{
  # OpenDaylight RPM .spec file to build
  specfile=$1

  # Build ODL SRPM and noarch RPM
  cd $rpmbuild_spec_dir
  rpmbuild -ba $specfile
}

# Accept path to specfile as a param, build all if absent
if [[ $# -eq 0 ]]; then
  # If no specfile passed, build all specfiles
  for specfile in /vagrant/specs/opendaylight-*.spec; do
    build $specfile
  done
elif [[ $# -eq 1 ]]; then
  # If build vars file passed, only do that build
  build $1
else
  echo "Usage: $0 [specfile]" >&2
  exit 1
fi
