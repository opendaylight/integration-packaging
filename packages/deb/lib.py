#!/usr/bin/env python
"""Build OpenDaylight's .debs using build description and Jinja2 templates."""

import imp
import os
import shutil
from string import Template
import subprocess

import templates.build_debianfiles as build_debfiles

# This file is assumed to be in the root of the Deb build logic's dir structure
deb_root = os.path.dirname(os.path.abspath(__file__))

# FIXME: Surly there is a better way to do this
pkg_lib = imp.load_source("", os.path.join(deb_root, os.pardir, "lib.py"))

# Common paths used in this script
templates_dir = os.path.join(deb_root, "templates")

# Templates that can be specialized per-build
# NB: Templates can't be concatenated with other Templates or strings, or
# cast to strings for concatenation. If they could, we would do elegant
# refactoring like concatenating paths to templates here and only calling
# Template.substitute in the build_rpm function.
deb_template = Template("opendaylight/opendaylight_$version_major.$version_minor."
                        "$version_patch-${pkg_version}_all.deb")
src_in_dir_template = Template("opendaylight/opendaylight-$version_major."
                               "$version_minor.$version_patch-$pkg_version/")


def build_deb(build):
    """Build the .deb described by the given build description.

    :param build: Description of a Debian build
    :type build: dict

    """
    # Specialize templates for the given build
    control_file_path = os.path.join(
        deb_root,
        src_in_dir_template.substitute(build),
        "debian/control")
    deb = deb_template.substitute(build)
    distro_tar_path = os.path.join(
        pkg_lib.cache_dir,
        pkg_lib.distro_template.substitute(build)) + ".tar.gz"
    src_in_dir_path = os.path.join(
        deb_root,
        src_in_dir_template.substitute(build))

    # Call helper script to build the required Debian files
    build_debfiles.build_debfiles(build)

    # Move ODL tarball into src input directory
    shutil.copy(distro_tar_path, src_in_dir_path)

    # Build Debian package
    os.chdir(src_in_dir_path)
    subprocess.call(["dpkg-buildpackage", "-us -uc -b", src_in_dir_path],
                    shell=True)

    # Build package that includes build dependencies
    subprocess.call(["sudo mk-build-deps -i " + control_file_path], shell=True)
    os.chdir(deb_root)

    # Copy the .debs from their output dir to the cache dir
    shutil.copy(deb, pkg_lib.cache_dir)
