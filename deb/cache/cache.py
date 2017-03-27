#!/usr/bin/env python
"""Read YAML description of ODL builds and cache the required artifacts."""

import os
import sys
import urllib

try:
    import yaml
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, install the Python libs it installs.\n")
    raise

# Path to the directory that contains this file is assumed to be the cache dir
cache_dir = os.path.dirname(os.path.abspath(__file__))


def cache_build(build):
    """Cache the artifacts required for the given debian build.

    :param build: Description of an ODL build, typically from build_vars.yaml
    :type build: dict

    """
    # OpenDaylight's tarball release name for the given build
    odl_tarball = build["download_url"].split('/')[-1]

    # After getting the string, build the tarball's full path
    odl_tarball_path = os.path.join(cache_dir, odl_tarball)

    # Cache appropriate version of OpenDaylight's release tarball
    if not os.path.isfile(odl_tarball_path):
        print("Downloading: {}".format(build["download_url"]))
        urllib.urlretrieve(build["download_url"], odl_tarball_path)
        print("Cached: {}".format(odl_tarball))
    else:
        print("Already cached: {}".format(odl_tarball))

    return odl_tarball_path


# If run as a script, cache artifacts required for all builds
if __name__ == "__main__":
    # Load debian build variables from a YAML config file
    with open(os.path.join(cache_dir, os.pardir, "build_vars.yaml")) as var_fd:
        build_vars = yaml.load(var_fd)
    for build in build_vars["builds"]:
        odl_tarball_path = cache_build(build)
