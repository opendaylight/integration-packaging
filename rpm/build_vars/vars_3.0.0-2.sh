#!/usr/bin/env sh
# Variables to define an OpenDaylight RPM build
# `build.sh` reads these and passes them to `opendaylight.spec`
# To define a new ODL RPM build, copy one of these and adjust as-needed

# Directory used for caching build artifacts
# Customizing this is useful for some offline builds
cache_dir="/vagrant"

# Version fields for the ODL release
version_major=3
version_minor=0

# Include variable defaults that are common to many builds
# NB: To use vars in default_vars.sh, define them before this source cmd
#     Example: version_[major,minor,patch] is used for [odl,rpm]_version
# NB: To override vars things defined in default_vars, define them after
source $cache_dir/build_vars/default_vars.sh

# Elemental codename for the ODL release, including SR if applicable
codename="Lithium"

# RPM version for the given ODL major.minor.patch
rpm_release=2
