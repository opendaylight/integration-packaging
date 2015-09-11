#!/usr/bin/env sh
# Build the ODL SRPM and noarch RPM described in opendaylight.spec
# This is designed to be run in the included Vagrant environment.

# Echo commands as they are run
set -x

build()
{
    # Common names used in this script
    odl_version="0.$version_major.$version_minor"
    rpm_version="$version_major.$version_minor.$version_patch"
    odl_srpm="opendaylight-$rpm_version-$rpm_release.$rpm_disttag.src.rpm"
    odl_rpm="opendaylight-$rpm_version-$rpm_release.$rpm_disttag.noarch.rpm"
    odl_tarball="distribution-karaf-$odl_version-$codename.tar.gz"
    unitfile_tarball="opendaylight-systemd-$sysd_commit.tar.gz"

    # Common paths used in this script
    odl_tb_cache_path="$cache_dir/$odl_tarball"
    unitfile_cache_path="$cache_dir/$unitfile_tarball"
    specfile_path="$cache_dir/opendaylight.spec"
    srpm_out_path="$HOME/rpmbuild/SRPMS/$odl_srpm"
    rpm_out_path="$HOME/rpmbuild/RPMS/noarch/$odl_rpm"
    odl_tb_url="https://nexus.opendaylight.org/content/groups/public/org/opendaylight/integration/distribution-karaf/$odl_version-$codename/$odl_tarball"
    unitfile_url="https://github.com/dfarrell07/opendaylight-systemd/archive/$sysd_commit/$unitfile_tarball"
    rpmbuild_src_dir="$HOME/rpmbuild/SOURCES/"
    rpmbuild_spec_dir="$HOME/rpmbuild/SPECS/"

    # Install required RPM building software and the repo that serves it
    sudo yum install -y epel-release
    sudo yum install -y fedora-packager

    # Add user to mock group for rpmbuild
    sudo usermod -a -G mock $USER

    # Configure rpmbuild dir
    rpmdev-setuptree

    # Download ODL release tarball if it's not cached locally already
    if [ ! -f  $odl_tb_cache_path ]; then
        echo "No cached ODL found, downloading from Nexus..."
        curl -o $odl_tb_cache_path $odl_tb_url
    else
        echo "Using cached version of ODL at $odl_tb_cache_path"
    fi

    # Put ODL release tarball in the location required by rpmbuild
    cp $odl_tb_cache_path $rpmbuild_src_dir

    # Download ODL systemd unitfile if it's not cached locally already
    if [ ! -f  $unitfile_cache_path ]; then
        echo "No cached ODL systemd unitfile found, downloading..."
        # Need `-L` to follow redirects
        curl -L -o $unitfile_cache_path $unitfile_url
    else
        echo "Using cached version of ODL systemd unitfile at $unitfile_cache_path"
    fi

    # Put systemd unitfile archive in rpmbuild's SOURCES dir
    cp $unitfile_cache_path $rpmbuild_src_dir

    # Put ODL RPM .spec file in rpmbuild's SPECS dir
    cp $specfile_path $rpmbuild_spec_dir

    # Build ODL SRPM and noarch RPM
    # Override disttag from .el7.centos to .el7 per best-practices/expected norms
    #   See: https://bugs.centos.org/view.php?id=9098
    cd $rpmbuild_spec_dir
    rpmbuild -ba --define "dist .$rpm_disttag" opendaylight.spec

    # Confirm SRPM found in expected location
    if [ -f  $srpm_out_path ]; then
        echo "SRPM built!"
        echo "Location: $srpm_out_path"
        if [ -d  $cache_dir ]; then
            echo "Assuming you want to cache the SRPM"
            cp $srpm_out_path $cache_dir
        fi
    else
        echo "SRPM seems to have failed. :(" >&2
    fi

    # Confirm RPM found in expected location
    if [ -f  $rpm_out_path ]; then
        echo "RPM built!"
        echo "Location: $rpm_out_path"
        if [ -d  $cache_dir ]; then
            echo "Assuming you want to cache the RPM"
            cp $rpm_out_path $cache_dir
        fi
    else
        echo "RPM seems to have failed. :(" >&2
    fi
}

# Accept path to build vars file as a param, build all if absent
if [[ $# -eq 0 ]]; then
  # If no build vars file passed, do all builds described in build_vars dir
  for vars_file in /vagrant/build_vars/*; do
    source $vars_file
    build
  done
elif [[ $# -eq 1 ]]; then
  # If build vars file passed, only do that build
  vars_file=$1
  source $vars_file
  build
else
  echo "Usage: $0 [vars_file]" >&2
  exit 1
fi
