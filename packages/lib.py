#!/usr/bin/env python

##############################################################################
# Copyright (c) 2016 Daniel Farrell and Others.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

import datetime
import glob
import os
import re
from string import Template
import subprocess
import sys
import tarfile
import urllib
from urllib2 import urlopen

try:
    from bs4 import BeautifulSoup
    import requests
    from requests.exceptions import HTTPError
    import tzlocal
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv.\n")
    raise

# Path to directory for cache artifacts
cache_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

# Templates that can be specialized into common artifact names per-build
# NB: Templates can't be concatenated with other Templates or strings, or
# cast to strings for concatenation. If they could, we would do elegant
# refactoring like concatenating paths to templates here and only calling
# Template.substitute in the build_rpm function.
distro_template = Template("opendaylight-$version_major.$version_minor."
                           "$version_patch-$pkg_version")
unitfile_template = Template("opendaylight-$sysd_commit.service")
unitfile_url_template = Template("https://git.opendaylight.org/gerrit/"
                                 "gitweb?p=integration/packaging.git;a="
                                 "blob_plain;f=packages/unitfiles/"
                                 "opendaylight.service;hb=$sysd_commit")


def extract_version(url):
    """Determine ODL version information from the ODL tarball build URL

    :arg str url: URL of the ODL tarball build for building RPMs

    """
    # Version components will be added below. Patch version is always 0.
    version = {"version_patch": "0"}

    # Parse URL to find major and minor versions. Eg:
    # https://nexus.opendaylight.org/content/repositories/public/org/
    #  opendaylight/integration/distribution-karaf/0.3.4-Lithium-SR4/
    #  distribution-karaf-0.3.4-Lithium-SR4.tar.gz
    # major_version = 3
    # minor_version = 4
    re_out = re.search(r'\d\.(\d+)\.(\d)', url)
    version["version_major"] = re_out.group(1)
    version["version_minor"] = re_out.group(2)

    # Add version components that need to be extracted based on type of build
    if "autorelease" in url:
        version = extract_autorelease_version(url, version)
    elif "snapshot" in url:
        version = extract_snapshot_version(url, version)
    elif "public" or "opendaylight.release" in url:
        version = extract_release_version(url, version)
    else:
        raise ValueError("Unrecognized URL {}".format(url))

    return version


def extract_release_version(url, version):
    """Extract package version components from release build URL

    :arg str url: URL to release tarball
    :arg dict version: Package version components for given distro
    :return dict version: Version components, with additions
    """
    # If this version of ODL has a codename, parse it from URL. Eg:
    # https://nexus.opendaylight.org/content/repositories/public/org/
    #  opendaylight/integration/distribution-karaf/0.3.4-Lithium-SR4/
    #  distribution-karaf-0.3.4-Lithium-SR4.tar.gz
    # codename = Lithium-SR4
    if int(version["version_major"]) < 7:
        # ODL versions before Nitrogen use Karaf 3, have a codename
        # Include "-" in codename to avoid hanging "-" when no codename
        version["codename"] = "-" + re.search(r'0\.[0-9]+\.[0-9]+-(.*)\/',
                                              url).group(1)
    else:
        # ODL versions Nitrogen and after use Karaf 4, don't have a codename
        version["codename"] = ""

    # Package version is assumed to be 1 for release builds
    # TODO: Should be able to manually set this in case this is a rebuild
    version["pkg_version"] = "1"

    return version


def extract_autorelease_version(url, version):
    """Extract package version components from an autorelease build URL

    :arg str url: URL to autorelease tarball
    :arg dict version: Package version components for given distro
    :return dict version: Version components, with additions
    """
    # If this version of ODL has a codename, parse it from URL. Eg:
    # https://nexus.opendaylight.org/content/repositories/autorelease-1533/
    #     org/opendaylight/integration/distribution-karaf/0.4.4-Beryllium-SR4/
    # codename = Beryllium-SR4
    if int(version["version_major"]) < 7:
        # ODL versions before Nitrogen use Karaf 3, have a codename
        # Include "-" in codename to avoid hanging "-" when no codename
        version["codename"] = "-" + re.search(r'0\.[0-9]+\.[0-9]+-(.*)\/',
                                              url).group(1)
    else:
        # ODL versions Nitrogen and after use Karaf 4, don't have a codename
        version["codename"] = ""

    # Autorelease URLs don't include a date, parse HTML to find build date
    # Strip distro zip/tarball archive part of URL, resulting in base URL
    base_url = url.rpartition("/")[0]+url.rpartition("/")[1]
    # Using bash subprocess to parse HTML and find date of build
    # TODO: Do all of this with Python, don't spawn a bash process
    # Set base_url as an environment var to pass it to subprocess
    os.environ["base_url"] = base_url
    raw_date = subprocess.Popen(
        "curl -s $base_url | grep tar.gz -A1 | tail -n1 |"
        "sed \"s/<td>//g\" | sed \"s/\\n//g\" | awk '{print $3,$2,$6}' ",
        shell=True, stdout=subprocess.PIPE,
        stdin=subprocess.PIPE).stdout.read().rstrip().strip("</td>")
    build_date = datetime.datetime.strptime(raw_date, "%d %b %Y").strftime(
                                            '%Y%m%d')

    # Parse URL to find unique build ID. Eg:
    # https://nexus.opendaylight.org/content/repositories/autorelease-1533/
    #     org/opendaylight/integration/distribution-karaf/0.4.4-Beryllium-SR4/
    # build_id = 1533
    build_id = re.search(r'\/autorelease-([0-9]+)\/', url).group(1)

    # Combine build date and build ID into pkg_version
    version["pkg_version"] = "0.1." + build_date + "rel" + build_id

    return version


def extract_snapshot_version(url, version):
    """Extract package version components from a snapshot build URL

    :arg str url: URL to snapshot tarball
    :arg dict version: Package version components for given distro
    :return dict version: Version components, with additions
    """

    # All snapshot builds use SNAPSHOT codename
    # Include "-" in codename to avoid hanging "-" when no codename
    version["codename"] = "-SNAPSHOT"

    # Parse URL to find build date and build ID. Eg:
    # https://nexus.opendaylight.org/content/repositories/
    #     opendaylight.snapshot/org/opendaylight/integration/
    #     distribution-karaf/0.6.0-SNAPSHOT/
    #     distribution-karaf-0.6.0-20161201.031047-2242.tar.gz
    # build_date = 20161201
    # build_id = 2242
    re_out = re.search(r'0.[0-9]+\.[0-9]+-([0-9]+)\.[0-9]+-([0-9]+)\.', url)
    build_date = re_out.group(1)
    build_id = re_out.group(2)

    # Combine build date and build ID into pkg_version
    version["pkg_version"] = "0.1." + build_date + "snap" + build_id

    return version


def get_snap_url(version_major):
    """Get the most recent snapshot build of the given ODL major version

    :arg str version_major: ODL major version to get latest snapshot of
    :return str snapshot_url: URL to latest snapshot tarball of ODL version

    """
    # Dir that contains all shapshot build dirs, varies based on Karaf 3/4
    parent_dir_url = "https://nexus.opendaylight.org/content/repositories/" \
                     "opendaylight.snapshot/org/opendaylight/integration/{}/" \
                     .format(get_distro_name_prefix(version_major))

    # Get HTML of dir that contains all shapshot dirs
    parent_dir_html = urlopen(parent_dir_url).read().decode('utf-8')

    # Get most recent minor version of the given major version
    version_minor = max(re.findall(
                        r'>\d\.{}\.(\d)-SNAPSHOT\/'.format(version_major),
                        parent_dir_html))

    # Dir that contains snapshot builds for the given major version
    snapshot_dir_url = parent_dir_url + "0.{}.{}-SNAPSHOT/".format(
        version_major,
        version_minor)

    # Get HTML of dir that contains snapshot builds for given major version
    snapshot_dir_html = urlopen(snapshot_dir_url).read().decode('utf-8')

    # Find most recent URL to tarball, ie most recent snapshot build
    return re.findall(r'href="(.*\.tar\.gz)"', snapshot_dir_html)[-1]


def get_sysd_commit():
    """Get latest Int/Pack repo commit hash"""

    int_pack_repo = "https://github.com/opendaylight/integration-packaging.git"
    # Get the commit hash at the tip of the master branch
    args_git = ['git', 'ls-remote', int_pack_repo, "HEAD"]
    args_awk = ['awk', '{print $1}']
    references = subprocess.Popen(args_git, stdout=subprocess.PIPE,
                                  shell=False)
    sysd_commit = subprocess.check_output(args_awk, stdin=references.stdout,
                                          shell=False).strip()

    return sysd_commit


def get_java_version(version_major):
    """Get the java_version dependency for ODL builds

       :arg str version_major: OpenDaylight major version number
       :return int java_version: Java version required by given ODL version
    """
    if int(version_major) < 5:
        java_version = 7
    else:
        java_version = 8
    return java_version


def get_changelog_date(pkg_type):
    """Get the changelog datetime formatted for the given package type

    :arg str pkg_type: Type of datetime formatting (rpm, deb)
    :return str changelog_date: Date or datetime formatted for given pkg_type
    """
    if pkg_type == "rpm":
        # RPMs require a date of the format "Day Month Date Year". For example:
        # Mon Jun 21 2017
        return datetime.date.today().strftime("%a %b %d %Y")
    elif pkg_type == "deb":
        # Debs require both a date and time.
        # Date must be of the format "Day, Date Month Year". For example:
        # Mon, 21 Jun 2017
        date = datetime.date.today().strftime("%a, %d %b %Y")
        # Time must be of the format "HH:MM:SS +HHMM". For example:
        # 15:01:16 +0530
        time = datetime.datetime.now(tzlocal.get_localzone()).\
            strftime("%H:%M:%S %z")
        return "{} {}".format(date, time)
    else:
        raise ValueError("Unknown package type: {}".format(pkg_type))


def get_distro_name_prefix(version_major, download_url=""):
    """Return distro name prefix based on ODL major version or distro URL.

    :arg str version_major: OpenDaylight major version number
    :arg str download_url: URL to ODL distribution
    :return str distro_prefix: MR, Karaf 3 or 4-style distro name prefix

    """
    mrel_prefix = "opendaylight"
    k3_prefix = "distribution-karaf"
    k4_prefix = "karaf"
    mrel_url_base = "https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/opendaylight/"
    k3_url_base = "https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/distribution-karaf/"
    k4_url_base = "https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/integration/karaf/"

    if mrel_url_base in download_url:
        return mrel_prefix
    elif k3_url_base in download_url:
        return k3_prefix
    elif k4_url_base in download_url:
        return k4_prefix

    if int(version_major) < 7:
        # ODL versions before Nitrogen use Karaf 3, distribution-karaf- names
        return k3_prefix
    else:
        # ODL versions Nitrogen and after use Karaf 4, karaf- names
        return k4_prefix


def cache_distro(build):
    """Cache the OpenDaylight distribution to package as RPM/Deb.

    :param build: Description of an RPM build
    :type build: dict
    :return str distro_tar_path: Path to cached distribution tarball

    """
    # Specialize templates for the given build
    distro = distro_template.substitute(build)

    # Append file extensions to get ODL distro zip/tarball templates
    distro_tar = distro + ".tar.gz"
    distro_zip = distro + ".zip"

    # Prepend cache dir path to get template of full path to cached zip/tarball
    distro_tar_path = os.path.join(cache_dir, distro_tar)
    distro_zip_path = os.path.join(cache_dir, distro_zip)

    # Cache OpenDaylight tarball to be packaged
    if not os.path.isfile(distro_tar_path):
        if build["download_url"].endswith(".tar.gz"):
            print("Downloading: {}".format(build["download_url"]))
            urllib.urlretrieve(build["download_url"], distro_tar_path)
            print("Cached: {}".format(distro_tar))
        # If download_url points at a zip, repackage as a tarball
        elif build["download_url"].endswith(".zip"):
            if not os.path.isfile(distro_zip):
                print("URL is to a zip, will download and convert to tar.gz")
                print("Downloading: {}".format(build["download_url"]))
                urllib.urlretrieve(build["download_url"], distro_zip_path)
                print("Downloaded {}".format(distro_zip_path))
            else:
                print("Already cached: {}".format(distro_zip_path))
            # Extract zip archive
            # NB: zipfile.ZipFile.extractall doesn't preserve permissions
            # https://bugs.python.org/issue15795
            subprocess.call(["unzip", "-oq", distro_zip_path, "-d", cache_dir])
            # Get files in cache dir
            cache_dir_ls_all = glob.glob(os.path.join(cache_dir, "*"))
            # Remove pyc files that may be newer than just-extracted zip
            cache_dir_ls = filter(lambda f: '.pyc' not in f, cache_dir_ls_all)
            # Get the most recent file in cache dir, hopefully unzipped archive
            unzipped_distro_path = max(cache_dir_ls, key=os.path.getctime)
            print("Extracted: {}".format(unzipped_distro_path))
            # Remove path from 'unzipped_distro_path', as will cd to dir below
            unzipped_distro = os.path.basename(unzipped_distro_path)
            # Using the full paths here creates those paths in the tarball,
            # which breaks the build. There's a way to change the working dir
            # during a single tar command using the system tar binary, but I
            # don't see a way to do that with Python.
            # TODO: Can this be done without changing directories?
            # TODO: Try https://goo.gl/XMx5gb
            cwd = os.getcwd()
            os.chdir(cache_dir)
            with tarfile.open(distro_tar, "w:gz") as tb:
                tb.add(unzipped_distro)
                print("Taring {} into {}".format(unzipped_distro, distro_tar))
            os.chdir(cwd)
            print("Cached: {}".format(distro_tar))
    else:
        print("Already cached: {}".format(distro_tar))

    return distro_tar_path


def cache_sysd(build):
    """Cache the artifacts required for the given RPM build.

    :param build: Description of an RPM build
    :type build: dict
    :return dict unitfile_path: Paths to cached unit file and unit file tarball

    """
    # Specialize templates for the given build
    unitfile = unitfile_template.substitute(build)
    unitfile_url = unitfile_url_template.substitute(build)

    # Append file extensions to get ODL distro zip/tarball templates
    unitfile_tar = unitfile + ".tar.gz"

    # Prepend cache dir path to get template of full path to cached zip/tarball
    unitfile_path = os.path.join(cache_dir, unitfile)
    unitfile_tar_path = os.path.join(cache_dir, unitfile_tar)

    # Download ODL's systemd unit file
    if not os.path.isfile(unitfile_path):
        urllib.urlretrieve(unitfile_url, unitfile_path)
        print("Cached: {}".format(unitfile))
    else:
        print("Already cached: {}".format(unitfile_path))

    # Cache ODL's systemd unit file as a tarball
    if not os.path.isfile(unitfile_tar_path):
        # Using the full paths here creates those paths in the tarball, which
        # breaks the build. There's a way to change the working dir during a
        # single tar command using the system tar binary, but I don't see a
        # way to do that with Python.
        # TODO: Is there a good way to do this without changing directories?
        # TODO: Try https://goo.gl/XMx5gb
        cwd = os.getcwd()
        os.chdir(cache_dir)
        # Create a .tar.gz archive containing ODL's systemd unitfile
        with tarfile.open(unitfile_tar, "w:gz") as tb:
            tb.add(unitfile)
        os.chdir(cwd)

        print("Cached: {}".format(unitfile_tar))
    else:
        print("Already cached: {}".format(unitfile_tar_path))

    return {"unitfile_tar_path": unitfile_tar_path,
            "unitfile_path": unitfile_path}
