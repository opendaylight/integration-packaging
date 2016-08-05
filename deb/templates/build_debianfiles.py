#!/usr/bin/env python
"""Build debian files from YAML debian config and Jinja2 debian templates."""

import os
import sys
import shutil
import urllib
from string import Template

try:
    import yaml
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv.\n")
    raise

debian_files_dynamic = ["changelog", "rules", "control"]
debian_files_static = ["compat", "karaf", "opendaylight.install",
                       "opendaylight.postrm", "opendaylight.postinst",
                       "opendaylight.upstart"]

# Path to the directory that contains this file is assumed to be the debian templates dir
templates_dir = os.path.dirname(os.path.abspath(__file__))

# Create the Jinja2 Environment
env = Environment(loader=FileSystemLoader(templates_dir))

# Python string Template, specialized into an Opendaylight directory name per-build
odl_dir_template = Template("opendaylight/opendaylight-$version_major.$version_minor."
                            "$version_patch-$pkg_version/")
odl_deb_template = Template("opendaylight/opendaylight_$version_major.$version_minor."
                            "$version_patch-${pkg_version}_all.deb")
odl_changes_template = Template("opendaylight/opendaylight_$version_major.$version_minor."
                                "$version_patch-${pkg_version}_all.changes")


def build_deb(build):
    """Build the debian files from a template for the given build description.

    :param build: Description of a debian build, typically from build_vars.yaml
    :type build: dict

    """
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

    # Delete old .changes file if it exists
    odl_changes_name = odl_changes_template.substitute(build)
    odl_changes_path = os.path.join(templates_dir, os.pardir, odl_changes_name)
    if os.path.isfile(odl_changes_path):
        os.remove(odl_changes_path)

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

    # Use specific systemd unitfile for each build
    unitfile = "opendaylight.service"
    unitfile_url_template = Template("https://git.opendaylight.org/gerrit/"
                                     "gitweb?p=integration/packaging.git;a="
                                     "blob_plain;f=rpm/unitfiles/opendaylight."
                                     "service;hb=$sysd_commit")
    unitfile_url = unitfile_url_template.substitute(build)

    # Build the full path for unitfile
    unitfile_path = os.path.join(debian_dir_path, unitfile)

    # Download ODL's systemd unitfile
    if not os.path.isfile(unitfile_path):
        urllib.urlretrieve(unitfile_url, unitfile_path)


# If run as a script, build .spec files for all builds
if __name__ == "__main__":
    # Load debian build variables from a YAML config file
    with open(os.path.join(templates_dir, os.pardir, "build_vars.yaml")) as var_fd:
        build_vars = yaml.load(var_fd)

    for build in build_vars["builds"]:
        build_deb(build)
