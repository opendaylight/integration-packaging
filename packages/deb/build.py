#!/usr/bin/env python
"""Build OpenDaylight's .debs using build description and Jinja2 templates."""

import os
import shutil
from string import Template
import subprocess

import cache.cache as cache
import templates.build_debianfiles as build_debfiles

# Common paths used in this script
# This file is assumed to be in the root of the .deb build logic's dir
# structure
project_root = os.path.dirname(os.path.abspath(__file__))

# Cache directory for OpenDaylight's release tarball
cache_dir = os.path.join(project_root, "cache")

# Debian templates directory
templates_dir = os.path.join(project_root, "templates")

# Specialized opendaylight directory for each build
odl_dir_template = Template("opendaylight/opendaylight-$version_major.$version_minor."
                            "$version_patch-$pkg_version/")
odl_deb_template = Template("opendaylight/opendaylight_$version_major.$version_minor."
                            "$version_patch-${pkg_version}_all.deb")


def build_deb(build):
    """Build the .deb described by the given build description.

    :param build: Description of a debian build
    :type build: dict

    """
    # Specialize a series of name templates for the given build
    odl_dir_name = odl_dir_template.substitute(build)
    odl_dir_path = os.path.join(templates_dir, os.pardir, odl_dir_name)
    odl_deb = odl_deb_template.substitute(build)

    # Call helper script to build the required debian files
    build_debfiles.build_debfiles(build)

    # Call a helper function to cache the artifacts required for each build
    odl_tarball_path = cache.cache_build(build)

    # Move ODL's tarball to the specialized OpenDaylight directory
    shutil.copy(odl_tarball_path, odl_dir_path)

    # Build debian package
    os.chdir(odl_dir_path)
    subprocess.call(["dpkg-buildpackage", "-us -uc -b",
                     odl_dir_path], shell=True)

    # Install opendaylight's dependencies
    control_file_path = os.path.join(odl_dir_path, "debian/control")
    subprocess.call(["sudo mk-build-deps -i " + control_file_path], shell=True)

    os.chdir(project_root)

    # Copy the .debs from their output dir to the cache dir
    shutil.copy(odl_deb, cache_dir)
