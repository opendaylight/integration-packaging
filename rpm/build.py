#!/usr/bin/env python

##############################################################################
# Copyright (c) 2016 Daniel Farrell and Others.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

"""Build OpenDaylight's RPMs using YAML build configs and Jinja2 templates."""

import argparse
import datetime
import os
import re
import shutil
from string import Template
import subprocess
import sys
from urllib2 import urlopen

import cache.cache as cache
import specs.build_specs as build_specs

try:
    from bs4 import BeautifulSoup
    import requests
    from requests.exceptions import HTTPError
    import yaml
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv.\n")
    raise


# Common paths used in this script
# This file is assumed to be in the root of the RPM build logic's dir structure
project_root = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(project_root, "cache")
specs_dir = os.path.join(project_root, "specs")
rpmbuild_dir = os.path.join(os.path.expanduser("~"), "rpmbuild")
src_in_dir = os.path.join(rpmbuild_dir, "SOURCES")
spec_in_dir = os.path.join(rpmbuild_dir, "SPECS")
srpm_out_dir = os.path.join(rpmbuild_dir, "SRPMS")
rpm_out_dir = os.path.join(rpmbuild_dir, "RPMS", "noarch")

# Templates that can be specialized into common artifact names per-build
odl_template = Template("opendaylight-$version_major.$version_minor."
                        "$version_patch-$rpm_release.tar.gz")
specfile_template = Template("opendaylight-$version_major.$version_minor."
                             "$version_patch-$rpm_release.spec")
unitfile_tb_template = Template("opendaylight-$sysd_commit.service.tar.gz")
rpm_template = Template("opendaylight-$version_major.$version_minor."
                        "$version_patch-$rpm_release.el7.noarch.rpm")
srpm_template = Template("opendaylight-$version_major.$version_minor."
                         "$version_patch-$rpm_release.el7.src.rpm")


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
        # FIXME: Boron uses distribution-karaf vs karaf, fails
        date_url = re.sub('karaf-.*\.tar\.gz$', '', url)
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
        #  org/opendaylight/integration/karaf/0.4.4-Beryllium-SR4/
        # build_id = 1533
        build_id = re.search(r'\/(autorelease)-([0-9]+)\/', url).group(2)
        rpm_release = "0.1." + date + "rel" + build_id
    elif "snapshot" in url:
        # Search the ODL snapshot build URL to match the date and the Build ID
        # that are between "karaf" and ".tar.gz".
        # eg: https://nexus.opendaylight.org/content/repositories/
        #      opendaylight.snapshot/org/opendaylight/integration/
        #      karaf/0.6.0-SNAPSHOT/
        #      karaf-0.6.0-20161201.031047-2242.tar.gz
        # build_id = 2242
        # date = 20161201
        # FIXME: Boron uses distribution-karaf vs karaf, fails
        odl_rpm = re.search(
            r'\/(karaf)-'
            r'([0-9]\.[0-9]\.[0-9])-([0-9]+)\.([0-9]+)-([0-9]+)\.(tar\.gz)',
            url)
        rpm_release = "0.1." + odl_rpm.group(3) + "snap" + odl_rpm.group(5)
    elif "public" or "opendaylight.release" in url:
        rpm_release = "1"
    else:
        raise ValueError("Unrecognized URL {}".format(url))

    version = {}
    # Search the ODL build URL to match 0.major.minor-codename-SR and extract
    # version information. eg: release:
    # https://nexus.opendaylight.org/content/repositories/public/org/
    #  opendaylight/integration/karaf/0.3.3-Lithium-SR3/
    #  karaf-0.3.3-Lithium-SR3.tar.gz
    #     match: 0.3.3-Lithium-SR3
    odl_version = re.search(r'\/(\d)\.(\d)\.(\d).(.*)\/', url)
    version["version_major"] = odl_version.group(2)
    version["version_minor"] = odl_version.group(3)
    version["version_patch"] = "0"
    version["rpm_release"] = rpm_release
    version["codename"] = odl_version.group(4)
    return version


def build_rpm(build):
    """Build the RPMs described by the given build description

    :param build: Description of an RPM build, typically from build_vars.yaml
    :type build: dict

    """
    # Specialize a series of name templates for the given build
    odl_tarball = odl_template.substitute(build)
    odl_rpm = rpm_template.substitute(build)
    odl_srpm = srpm_template.substitute(build)
    odl_specfile = specfile_template.substitute(build)
    unitfile_tarball = unitfile_tb_template.substitute(build)

    # After building strings from the name templates, build their full path
    odl_tarball_path = os.path.join(cache_dir, odl_tarball)
    unitfile_tarball_path = os.path.join(cache_dir, unitfile_tarball)
    specfile_path = os.path.join(specs_dir, odl_specfile)
    spec_in_path = os.path.join(spec_in_dir, odl_specfile)
    rpm_out_path = os.path.join(rpm_out_dir, odl_rpm)
    srpm_out_path = os.path.join(srpm_out_dir, odl_srpm)

    # Call a helper function to cache the artifacts required for each build
    cache.cache_build(build)

    # Call helper script to build the required RPM .spec files
    build_specs.build_spec(build)

    # Clean up old rpmbuild dir structure if it exists
    if os.path.isdir(rpmbuild_dir):
        shutil.rmtree(rpmbuild_dir)

    # Create rpmbuild dir structure
    subprocess.call("rpmdev-setuptree")

    # Move unitfile, tarball and specfile to correct rpmbuild dirs
    shutil.copy(odl_tarball_path, src_in_dir)
    shutil.copy(unitfile_tarball_path, src_in_dir)
    shutil.copy(specfile_path, spec_in_dir)

    # Call rpmbuild, build both SRPMs/RPMs
    subprocess.call(["rpmbuild", "-ba", spec_in_path])

    # Copy the RPMs/SRPMs from their output dir to the cache dir
    shutil.copy(rpm_out_path, cache_dir)
    shutil.copy(srpm_out_path, cache_dir)


def build_snapshot_rpm(build):
    """Build latest snapshot RPMs fetching information from URL.

    :param build: Description of an RPM build, from parent_dir URL
    :type build: dict

    """
    parent_dir = "https://nexus.opendaylight.org/content/repositories/" \
                 "opendaylight.snapshot/org/opendaylight/integration/karaf/"

    # If the minor verison is given, get the sub-directory directly
    # else, find the latest sub-directory
    sub_dir = ''
    snapshot_dir = ''
    try:
        sub_dir = '0.' + build['version_major'] + '.' + \
                   build['version_minor'] + '-SNAPSHOT/'
        snapshot_dir = parent_dir + sub_dir
    except KeyError:
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
                if dir.group(2) == build['version_major']:
                    snapshot_dir = tag['href']
                    build['version_minor'] = dir.group(3)

    try:
        req = requests.get(snapshot_dir)
        req.raise_for_status()
    except HTTPError:
        print "Could not find the snapshot directory"
        print "Tried: {}".format(snapshot_dir)
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

        # Get download_url
        build['download_url'] = snapshot_url

        # Call `extract_version` function to get version information
        # except Major and Minor version which are already present
        version = extract_version(build['download_url'])
        build['version_patch'] = version['version_patch']
        build['rpm_release'] = version['rpm_release']
        build['codename'] = version['codename']
        urlpath.close()

        build_rpm(build)


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


# When run as a script, accept a set of builds and execute them
if __name__ == "__main__":
    # Accept the version(s) of the build(s) to perform as args
    # TODO: More docs on ArgParser and argument
    parser = argparse.ArgumentParser(conflict_handler='resolve')

    new_build_group = parser.add_argument_group("New build")
    new_build_group.add_argument(
        "--download_url", help="Tarball to repackage into RPM")
    new_build_group.add_argument(
        "--sysd_commit", help="Version of ODL unitfile to package")
    new_build_group.add_argument(
        "--changelog_date", help="Date this RPM was defined")
    new_build_group.add_argument(
        "--changelog_name", help="Name of person who defined RPM")
    new_build_group.add_argument(
        "--changelog_email", help="Email of person who defined RPM")

    # Arguments needed to build RPM from latest snapshot
    # given a stable major branch
    latest_snap_group = parser.add_argument_group("Latest snapshot build")
    latest_snap_group.add_argument("--build-latest-snap", action='store_true',
                                   help="Build RPM from the latest snpashot")
    latest_snap_group.add_argument("--major", help="Stable branch from which "
                                   "to build the snapshot")
    latest_snap_group.add_argument("--minor", help="Minor version of the "
                                   "stable branch to build the snapshot")
    latest_snap_group.add_argument("--sysd_commit",
                                   help="Version of ODL unitfile to package")
    latest_snap_group.add_argument("--changelog_name",
                                   help="Name of person who defined RPM")
    latest_snap_group.add_argument("--changelog_email",
                                   help="Email of person who defined RPM")
    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse the given args
    args = parser.parse_args()

    # A dictionary containing essential build variables
    build = {}
    # Check if `changelog_date` has been passed as an arg
    # The current datetime should be the default date for RPM changelog date
    # but can still accept optional `changelog_date` param
    # `changelog_date` is in the format: 'Sat Dec 10 2016'
    # Docs:
    #   https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
    if not args.changelog_date:
        args.changelog_date = datetime.date.today().strftime("%a %b %d %Y")

    # Check if `sysd_commit` has been passed as an arg
    # Use latest Int/Pack repo commit hash as sysd_commit var
    # unless passed by param
    if not args.sysd_commit:
        args.sysd_commit = get_sysd_commit()

    # If download_url is given, update version info
    if args.download_url:
        build.update({"download_url": args.download_url})
        version = extract_version(args.download_url)
        build.update(version)

    # Common parameters for all new and snapshot builds
    build.update({"sysd_commit": args.sysd_commit,
                  "changelog_name": args.changelog_name,
                  "changelog_email": args.changelog_email,
                  "changelog_date": args.changelog_date,
                  })

    # If the flag `--build-latest-snap` is true, extract information
    # from the snapshot URL using major version and minor version(optional)
    # info, else proceed directly to build the RPM
    if args.build_latest_snap:
        if args.major:
            build.update({'version_major': args.major})
            if args.minor:
                build.update({'version_minor': args.minor})
            build_snapshot_rpm(build)
    else:
        build_rpm(build)
