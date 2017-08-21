#!/usr/bin/env python
"""Cache the required artifacts for building DEB packages."""

import os
import urllib

# Path to the directory that contains this file is assumed to be the cache dir
cache_dir = os.path.dirname(os.path.abspath(__file__))


def cache_build(build):
    """Cache the artifacts required for the given debian build.

    :param build: Description of an ODL build
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
