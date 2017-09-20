#!/usr/bin/env python

##############################################################################
# Copyright (c) 2016 Daniel Farrell and Others.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

"""Build OpenDaylight's RPMs using build description and Jinja2 templates."""

import os
import shutil
from string import Template
import subprocess

import specs.build_specs as build_specs

from .. import lib as pkg_lib

# This file is assumed to be in the root of the RPM build logic's dir structure
rpm_root = os.path.dirname(os.path.abspath(__file__))

# Common paths used in this script
rpmbuild_dir = os.path.join(os.path.expanduser("~"), "rpmbuild")
src_in_dir = os.path.join(rpmbuild_dir, "SOURCES")
spec_in_dir = os.path.join(rpmbuild_dir, "SPECS")

# Templates that can be specialized per-build
spec_template = Template("opendaylight-$version_major.$version_minor."
                         "$version_patch-$pkg_version.spec")
spec_in_path_template = os.path.join(rpmbuild_dir, "SPECS", spec_template)
spec_path_template = os.path.join(rpm_root, "specs", spec_template)
rpm_template = Template("opendaylight-$version_major.$version_minor."
                        "$version_patch-$pkg_version.el7.noarch.rpm")
rpm_out_path_template = os.path.join(rpmbuild_dir, "RPMS", "noarch",
                                     rpm_template)
srpm_template = Template("opendaylight-$version_major.$version_minor."
                         "$version_patch-$pkg_version.el7.src.rpm")
srpm_out_path_template = os.path.join(rpmbuild_dir, "SRPMS", srpm_template)


def build_rpm(build):
    """Build the RPMs described by the given build description

    :param build: Description of an RPM build
    :type build: dict

    """
    # Specialize a series of templates for the given build
    distro_tar_path = pkg_lib.distro_tar_path_template.substitute(build)
    unitfile_tar_path = pkg_lib.unitfile_tar_path_template.substitute(build)
    spec_path = spec_path_template.substitute(build)
    spec_in_path = spec_in_path_template.substitute(build)
    rpm_out_path = rpm_out_path_template.substitute(build)
    srpm_out_path = srpm_out_path_template.substitute(build)

    # Call helper script to build the required RPM .spec files
    build_specs.build_spec(build)

    # Clean up old rpmbuild dir structure if it exists
    if os.path.isdir(rpmbuild_dir):
        shutil.rmtree(rpmbuild_dir)

    # Create rpmbuild dir structure
    subprocess.call("rpmdev-setuptree")

    # Move unit file, tarball and specfile to correct rpmbuild dirs
    shutil.copy(distro_tar_path, src_in_dir)
    shutil.copy(unitfile_tar_path, src_in_dir)
    shutil.copy(spec_path, spec_in_dir)

    # Call rpmbuild, build both SRPMs/RPMs
    subprocess.call(["rpmbuild", "-ba", spec_in_path])

    # Copy the RPMs/SRPMs from their output dir to the cache dir
    shutil.copy(rpm_out_path, pkg_lib.cache_dir)
    shutil.copy(srpm_out_path, pkg_lib.cache_dir)
