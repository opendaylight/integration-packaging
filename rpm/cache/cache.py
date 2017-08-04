#!/usr/bin/env python
"""Read YAML description of RPM builds and cache the required artifacts."""

import os
from string import Template
import sys
import tarfile
import urllib

try:
    import yaml
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv.\n")
    raise

# Path to the directory that contains this file is assumed to be the cache dir
cache_dir = os.path.dirname(os.path.abspath(__file__))

# Templates that can be specialized into artifact names/paths per-build
odl_template = Template("opendaylight-$version_major.$version_minor."
                        "$version_patch-$pkg_version.tar.gz")
unitfile_template = Template("opendaylight-$sysd_commit.service")
unitfile_url_template = Template("https://git.opendaylight.org/gerrit/"
                                 "gitweb?p=integration/packaging.git;a="
                                 "blob_plain;f=rpm/unitfiles/opendaylight."
                                 "service;hb=$sysd_commit")
unitfile_tb_template = Template("opendaylight-$sysd_commit.service.tar.gz")


def cache_build(build):
    """Cache the artifacts required for the given RPM build.

    :param build: Description of an RPM build, typically from build_vars.yaml
    :type build: dict

    """
    # Specialize a series of name/URL templates for the given build
    odl_tarball = odl_template.substitute(build)
    unitfile = unitfile_template.substitute(build)
    unitfile_url = unitfile_url_template.substitute(build)
    unitfile_tarball = unitfile_tb_template.substitute(build)

    # After building strings from the name templates, build their full path
    odl_tarball_path = os.path.join(cache_dir, odl_tarball)
    unitfile_path = os.path.join(cache_dir, unitfile)
    unitfile_tarball_path = os.path.join(cache_dir, unitfile_tarball)

    # Cache appropriate version of OpenDaylight's release tarball
    if not os.path.isfile(odl_tarball_path):
        print("Downloading: {}".format(build["download_url"]))
        urllib.urlretrieve(build["download_url"], odl_tarball_path)
        print("Cached: {}".format(odl_tarball))
    else:
        print("Already cached: {}".format(odl_tarball))

    # Cache appropriate version of OpenDaylight's systemd unitfile as a tarball
    if not os.path.isfile(unitfile_tarball_path):
        # Download ODL's systemd unitfile
        urllib.urlretrieve(unitfile_url, unitfile_path)

        # Using the full paths here creates those paths in the tarball, which
        # breaks the build. There's a way to change the working dir during a
        # single tar command using the system tar binary, but I don't see a
        # way to do that with Python.
        # TODO: Is there a good way to do this without changing directories?
        cwd = os.getcwd()
        os.chdir(cache_dir)
        # Create a .tar.gz archive containing ODL's systemd unitfile
        with tarfile.open(unitfile_tarball, "w:gz") as tb:
            tb.add(unitfile)
        os.chdir(cwd)

        # Remove the now-archived unitfile
        os.remove(unitfile_path)
        print("Cached: {}".format(unitfile_tarball))
    else:
        print("Already cached: {}".format(unitfile_tarball))


# If run as a script, cache artifacts required for all builds
if __name__ == "__main__":
    # Load RPM build variables from a YAML config file
    with open(os.path.join(cache_dir, os.pardir, "build_vars.yaml")) as var_fd:
        build_vars = yaml.load(var_fd)

    for build in build_vars["builds"]:
        cache_build(build)
