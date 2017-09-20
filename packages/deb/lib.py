#!/usr/bin/env python
"""Build OpenDaylight's .debs using build description and Jinja2 templates."""

import os
import shutil
from string import Template
import subprocess

import cache.cache as cache
import templates.build_debianfiles as build_debfiles

from .. import lib as pkg_lib

# This file is assumed to be in the root of the Deb build logic's dir structure
deb_root = os.path.dirname(os.path.abspath(__file__))

# Common paths used in this script
templates_dir = os.path.join(deb_root, "templates")

# Templates that can be specialized per-build
src_in_dir_template = Template("opendaylight/opendaylight-$version_major."
                               "$version_minor.$version_patch-$pkg_version/")
src_in_dir_path_template = os.path.join(deb_root, src_in_dir_template)
control_file_path_template = os.path.join(src_in_dir_path_template,
                                          "debian/control")
deb_template = Template("opendaylight/opendaylight_$version_major.$version_minor."
                        "$version_patch-${pkg_version}_all.deb")


def build_deb(build):
    """Build the .deb described by the given build description.

    :param build: Description of a Debian build
    :type build: dict

    """
    # Specialize a series of templates for the given build
    distro_tar_path = pkg_lib.distro_tar_path_template.substitute(build)
    src_in_dir = src_in_dir_template.substitute(build)
    src_in_dir_path = src_in_dir_path_template.substitute(build)
    control_file_path = control_file_path_template.substitute(build)
    deb = deb_template.substitute(build)

    # Call helper script to build the required Debian files
    build_debfiles.build_debfiles(build)

    # Move ODL tarball to package into src input directory
    shutil.copy(distro_tar_path, src_in_dir)

    # Build Debian package
    os.chdir(src_in_dir_path)
    subprocess.call(["dpkg-buildpackage", "-us -uc -b", src_in_dir_path],
                    shell=True)

    # Build package that includes build dependencies
    subprocess.call(["sudo mk-build-deps -i " + control_file_path], shell=True)
    os.chdir(deb_root)

    # Copy the .debs from their output dir to the cache dir
    shutil.copy(deb, pkg_lib.cache_dir)
