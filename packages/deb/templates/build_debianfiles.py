#!/usr/bin/env python
"""Build debian files from build descriptionand Jinja2 debian templates."""

import os
import re
import shutil
from string import Template
import sys

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, install the Python libs it installs.\n")
    raise

debian_files_dynamic = ["changelog", "rules", "control"]
debian_files_static = ["compat", "karaf", "opendaylight.install",
                       "opendaylight.postrm", "opendaylight.postinst",
                       "opendaylight.upstart"]

# Path to the directory that contains this file is assumed to be the
# debian templates dir
templates_dir = os.path.dirname(os.path.abspath(__file__))

# Create the Jinja2 Environment
env = Environment(loader=FileSystemLoader(templates_dir))

# Python string Template, specialized into an Opendaylight directory name
# per-build
odl_dir_template = Template("opendaylight/opendaylight-$version_major.$version_minor."
                            "$version_patch-$pkg_version/")
odl_deb_template = Template("opendaylight/opendaylight_$version_major.$version_minor."
                            "$version_patch-${pkg_version}_all.deb")
odl_files_template = Template("opendaylight_$version_major.$version_minor."
                              "$version_patch-${pkg_version}*")


def build_debfiles(build):
    """Builds Debian files from templates for the given build description.

    Creates a debian dir for the build, copies static build files into it,
    specializes templates with build-spicific vars to create dynamic files,
    downloads build-specific systemd unitfile based on commit hash.

    :param build: Description of a debian build
    :type build: dict

    """
    # Specialize a series of name templates for the given build
    odl_dir_name = odl_dir_template.substitute(build)
    odl_dir_path = os.path.join(templates_dir, os.pardir, odl_dir_name)

    # Clean up opendaylight dir structure if it exists
    if os.path.isdir(odl_dir_path):
        shutil.rmtree(odl_dir_path)

    # Delete old .deb file if it exists
    odl_deb_name = odl_deb_template.substitute(build)
    odl_deb_path = os.path.join(templates_dir, os.pardir, odl_deb_name)
    if os.path.isfile(odl_deb_path):
        os.remove(odl_deb_path)

    # Delete old .changes, .dsc, .tar.gz files if they exist
    odl_files_regex = odl_files_template.substitute(build)
    odl_par_dir = os.path.join(templates_dir, os.pardir, "opendaylight")
    if os.path.isdir(odl_par_dir):
        for f in os.listdir(odl_par_dir):
            if re.search(odl_files_regex, f):
                os.remove(os.path.join(odl_par_dir, f))

    # Create debian directory
    debian_dir_path = os.path.join(odl_dir_path, "debian")
    os.makedirs(debian_dir_path)

    # Copy files common to all .debs to the specific debian dir
    for file_name in debian_files_static:
        file_path = os.path.join(templates_dir, file_name)
        shutil.copy(file_path, debian_dir_path)

    # Copy templated files to debian build dir, specialize templates
    for file_name in debian_files_dynamic:
        # Load OpenDaylight debian files Jinja2 template
        template = env.get_template(file_name + "_template")
        file_path = os.path.join(debian_dir_path, file_name)
        with open(file_path, "w") as debian_file:
            debian_file.write(template.render(build))
