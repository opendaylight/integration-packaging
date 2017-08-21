#!/usr/bin/env python

##############################################################################
# Copyright (c) 2016 Daniel Farrell and Others.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

import datetime
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
    if "autorelease" in url:
        # Autorelease URL does not include a date and hence date extraction
        # logic is needed for RPM versioning.
        # Docs:
        #   https://wiki.opendaylight.org/view/Integration/Packaging/Versioning
        # Substitute the part of the build URL not required with empty string
        date_url = re.sub('distribution-karaf-.*\.tar\.gz$', '', url)
        # Set date_url as an environment variable for it to be used in
        # a subprocess
        os.environ["date_url"] = date_url
        # Extract ODL artifact's date by scraping data from the build URL
        odl_date = subprocess.Popen(
            "curl -s $date_url | grep tar.gz -A1 | tail -n1 |"
            "sed \"s/<td>//g\" | sed \"s/\\n//g\" | awk '{print $3,$2,$6}' ",
            shell=True, stdout=subprocess.PIPE,
            stdin=subprocess.PIPE).stdout.read().rstrip().strip("</td>")
        date = datetime.datetime.strptime(odl_date, "%d %b %Y").strftime(
                                                                '%Y%m%d')
        # Search the ODL autorelease build URL to match the Build ID that
        # follows "autorelease-". eg:
        # https://nexus.opendaylight.org/content/repositories/autorelease-1533/
        #  org/opendaylight/integration/distribution-karaf/0.4.4-Beryllium-SR4/
        # build_id = 1533
        build_id = re.search(r'\/(autorelease)-([0-9]+)\/', url).group(2)
        pkg_version = "0.1." + date + "rel" + build_id
    elif "snapshot" in url:
        # Search the ODL snapshot build URL to match the date and the Build ID
        # that are between "distribution-karaf" and ".tar.gz".
        # eg: https://nexus.opendaylight.org/content/repositories/
        #      opendaylight.snapshot/org/opendaylight/integration/
        #      distribution-karaf/0.6.0-SNAPSHOT/
        #      distribution-karaf-0.6.0-20161201.031047-2242.tar.gz
        # build_id = 2242
        # date = 20161201
        odl_rpm = re.search(
            r'\/(distribution-karaf)-'
            r'([0-9]\.[0-9]\.[0-9])-([0-9]+)\.([0-9]+)-([0-9]+)\.(tar\.gz)',
            url)
        pkg_version = "0.1." + odl_rpm.group(3) + "snap" + odl_rpm.group(5)
    elif "public" or "opendaylight.release" in url:
        pkg_version = "1"
    else:
        raise ValueError("Unrecognized URL {}".format(url))

    version = {}
    # Search the ODL build URL to match 0.major.minor-codename-SR and extract
    # version information. eg: release:
    # https://nexus.opendaylight.org/content/repositories/public/org/
    #  opendaylight/integration/distribution-karaf/0.3.3-Lithium-SR3/
    #  distribution-karaf-0.3.3-Lithium-SR3.tar.gz
    #     match: 0.3.3-Lithium-SR3
    odl_version = re.search(r'\/(\d)\.(\d)\.(\d).(.*)\/', url)
    version["version_major"] = odl_version.group(2)
    version["version_minor"] = odl_version.group(3)
    version["version_patch"] = "0"
    version["pkg_version"] = pkg_version
    version["codename"] = odl_version.group(4)
    return version


def get_snap_url(version_major):
    """Fetches tarball url for snapshot releases using version information

    :arg str version_major: Major version for snapshot build
    :return arg snapshot_url: URL of the snapshot release
    """
    k3_parent_dir = "https://nexus.opendaylight.org/content/repositories/" \
        "opendaylight.snapshot/org/opendaylight/integration/" \
        "distribution-karaf/"
    k4_parent_dir = "https://nexus.opendaylight.org/content/repositories/" \
        "opendaylight.snapshot/org/opendaylight/integration/karaf/"
    sub_dir = ''
    snapshot_dir = ''
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
    if version_major < 5:
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
