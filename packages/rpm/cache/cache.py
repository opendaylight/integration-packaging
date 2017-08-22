#!/usr/bin/env python
"""Cache the required artifacts for building RPM packages."""

import glob
import os
from string import Template
import tarfile
import urllib
import zipfile

# Path to the directory that contains this file is assumed to be the cache dir
cache_dir = os.path.dirname(os.path.abspath(__file__))

# Templates that can be specialized into artifact names/paths per-build
odl_template = Template("opendaylight-$version_major.$version_minor."
                        "$version_patch-$pkg_version.tar.gz")
unitfile_template = Template("opendaylight-$sysd_commit.service")
unitfile_url_template = Template("https://git.opendaylight.org/gerrit/"
                                 "gitweb?p=integration/packaging.git;a="
                                 "blob_plain;f=packages/rpm/unitfiles/"
                                 "opendaylight.service;hb=$sysd_commit")
unitfile_tb_template = Template("opendaylight-$sysd_commit.service.tar.gz")


def cache_build(build):
    """Cache the artifacts required for the given RPM build.

    :param build: Description of an RPM build
    :type build: dict

    """
    # Specialize a series of name/URL templates for the given build
    odl_tarball = odl_template.substitute(build)
    unitfile = unitfile_template.substitute(build)
    unitfile_url = unitfile_url_template.substitute(build)
    unitfile_tarball = unitfile_tb_template.substitute(build)

    # After building strings from the name templates, build their full path
    odl_tarball_path = os.path.join(cache_dir, odl_tarball)
    odl_zip_path = odl_tarball_path.replace("tar.gz", "zip")
    unitfile_path = os.path.join(cache_dir, unitfile)
    unitfile_tarball_path = os.path.join(cache_dir, unitfile_tarball)

    # Cache OpenDaylight tarball to be packaged
    if not os.path.isfile(odl_tarball_path):
        if build["download_url"].endswith(".tar.gz"):
            print("Downloading: {}".format(build["download_url"]))
            urllib.urlretrieve(build["download_url"], odl_tarball_path)
            print("Cached: {}".format(odl_tarball))
        # If download_url points at a zip, repackage as a tarball
        elif build["download_url"].endswith(".zip"):
            if not os.path.isfile(odl_zip_path):
                print("URL is to a zip, will download and convert to tar.gz")
                print("Downloading: {}".format(build["download_url"]))
                urllib.urlretrieve(build["download_url"], odl_zip_path)
                print("Downloaded {}".format(odl_zip_path))
            else:
                print("Already cached: {}".format(odl_zip_path))
            # Extract zip archive
            with zipfile.ZipFile(odl_zip_path) as zip_ref:
                zip_ref.extractall(cache_dir)
            # Get files in cache dir
            cache_dir_ls_all = glob.glob(os.path.join(cache_dir, "*"))
            # Remove pyc files that may be newer than just-extracted zip
            cache_dir_ls = filter(lambda f: '.pyc' not in f, cache_dir_ls_all)
            # Get the most recent file in cache dir, hopefully unzipped archive
            unzipped_distro_full_path = max(cache_dir_ls, key=os.path.getctime)
            print("Extracted: {}".format(unzipped_distro_full_path))
            # Remove path from unzipped distro filename, as will cd to dir below
            unzipped_distro = os.path.basename(unzipped_distro_full_path)
            # Using the full paths here creates those paths in the tarball, which
            # breaks the build. There's a way to change the working dir during a
            # single tar command using the system tar binary, but I don't see a
            # way to do that with Python.
            # TODO: Is there a good way to do this without changing directories?
            # TODO: Try https://goo.gl/XMx5gb
            cwd = os.getcwd()
            os.chdir(cache_dir)
            with tarfile.open(odl_tarball, "w:gz") as tb:
                tb.add(unzipped_distro)
                print("Taring {} into {}".format(unzipped_distro, odl_tarball))
            os.chdir(cwd)
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
        # TODO: Try https://goo.gl/XMx5gb
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
