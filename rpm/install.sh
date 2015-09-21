#!/usr/bin/env sh
# Simple helper script for installing ODL from its noarch RPM
# Installs version described by a build_vars file param or the latest version
# As with all RPMs, an ODL RPM can be installed with `sudo rpm -i <path>`

# Echo commands as they are run
set -x

# Accept path to build vars file as a param, install latest RPM if absent
if [[ $# -eq 0 ]]; then
    # If no arguments are passed, install the latest RPM in the cache_dir
    # Default to /vagrant as the cache directory
    cache_dir="/vagrant"
    rpm_path=`ls -rc $cache_dir/opendaylight-*noarch.rpm | tail -n 1`
elif [[ $# -eq 1 ]]; then
    # If a build vars file is passed, install the RPM it describes
    vars_file=$1
    source $vars_file
    # cache_dir and odl_rpm are defied by the vars_* file
    rpm_path="$cache_dir/$odl_rpm"
else
    echo "Usage: $0 [vars_file]" >&2
    exit 1
fi

# Install Java, required by ODL
sudo yum install -y java

# Install ODL
echo "Installing ODL from $rpm_path"
sudo rpm -i $rpm_path
