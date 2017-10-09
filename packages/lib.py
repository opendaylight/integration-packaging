#!/usr/bin/env python

##############################################################################
# Copyright (c) 2016 Daniel Farrell and Others.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

import datetime
import os
import re
import subprocess
import sys
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
    re_out = re.search(r'\d\.(\d)\.(\d)', url)
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


def get_snap_url(version_major, version_minor=None):
    """Fetches tarball url for snapshot releases using version information

    :arg str version_major: Major version for snapshot build
    :arg str version_minor: Minor version for snapshot build(optional)
    :return arg snapshot_url: URL of the snapshot release
    """
    parent_dir = "https://nexus.opendaylight.org/content/repositories/" \
                 "opendaylight.snapshot/org/opendaylight/integration/{}/" \
                 .format(get_distro_name_prefix(version_major))

    # If the minor verison is given, get the sub-directory directly
    # else, find the latest sub-directory
    sub_dir = ''
    snapshot_dir = ''
    if version_minor:
        sub_dir = '0.' + version_major + '.' + version_minor + '-SNAPSHOT/'
        snapshot_dir = parent_dir + sub_dir
    else:
        subdir_url = urlopen(parent_dir)
        content = subdir_url.read().decode('utf-8')
        all_dirs = BeautifulSoup(content, 'html.parser')

        # Loops through all the sub-directories present and stores the
        # latest sub directory as sub-directories are already sorted
        # in early to late order.
        for tag in all_dirs.find_all('a', href=True):
            # Checks if the sub-directory name is of the form
            # '0.<major_version>.<minor_version>-SNAPSHOT'.
            dir = re.search(r'\/(\d)\.(\d)\.(\d).(.*)\/', tag['href'])
            # If the major version matches the argument provided
            # store the minor version, else ignore.
            if dir:
                if dir.group(2) == version_major:
                    snapshot_dir = tag['href']
                    version_minor = dir.group(3)

    try:
        req = requests.get(snapshot_dir)
        req.raise_for_status()
    except HTTPError:
        print "Could not find the snapshot directory"
    else:
        urlpath = urlopen(snapshot_dir)
        content = urlpath.read().decode('utf-8')
        html_content = BeautifulSoup(content, 'html.parser')
        # Loops through all the files present in `snapshot_dir`
        # and stores the url of latest tarball because files are
        # already sorted in early to late order.
        for tag in html_content.find_all('a', href=True):
            if tag['href'].endswith('tar.gz'):
                snapshot_url = tag['href']
    return snapshot_url


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
    :return int changelog_date: Date or datetime formatted for given pkg_type
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


def get_distro_name_prefix(version_major):
    """Return Karaf 3 or 4-style distro name prefix based on ODL major version

    :arg str major_version: OpenDaylight major version umber
    :return str distro_name_style: Karaf 3 or 4-style distro name prefix

    """
    if int(version_major) < 7:
        # ODL versions before Nitrogen use Karaf 3, distribution-karaf- names
        return "distribution-karaf"
    else:
        # ODL versions Nitrogen and after use Karaf 4, karaf- names
        return "karaf"
