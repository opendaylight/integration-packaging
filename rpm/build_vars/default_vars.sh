#!/usr/bin/env sh
# Variables to define an OpenDaylight RPM build
# `build.sh` reads these and passes them to opendaylight.spec
# To define a new ODL RPM build, copy one of these and adjust as-needed

# Version fields for the ODL release
version_patch=0

# Override disttag from .el7.centos to .el7 per best-practices/expected norms
#   See: https://bugs.centos.org/view.php?id=9098
rpm_disttag="el7"

# Java versions supported by this ODL release
java_version=">= 1:1.7.0"

# Version of ODL systemd unitfile to download and package in ODL RPM
# Update this commit if systemd unit file is updated
sysd_commit="4a872270893f0daeebcbbcc0ff0014978e3c5f68"

# Directory used for caching build artifacts
# Being able to customize this is useful for some offline builds
cache_dir="/vagrant"

# ODL version translation
# Note that the RPM is shifting ODL's version to the left by one value
#   to be consistent with the major.minor.patch scheme used universally
#   by RPMs. ODL's version is currently prefixed with a static, useless
#   leading 0, which is widely ignored in practice. For now the version
#   translation happens here. This will likely be fixed as ODL moves to
#   a continuous release model.
odl_version="0.$version_major.$version_minor"
rpm_version="$version_major.$version_minor.$version_patch"
