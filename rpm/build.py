#!/usr/bin/env python
"""Build OpenDaylight's RPMs using YAML build configs and Jinja2 templates."""

import os
import sys
import argparse
import shutil
import subprocess
import datetime
import re

from string import Template
from urllib2 import urlopen
import requests
from requests.exceptions import HTTPError


try:
    import yaml
    from bs4 import BeautifulSoup
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv.\n")
    raise


import cache.cache as cache
import specs.build_specs as build_specs

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


def build_rpm(build):
    """Build the RPMs described by the given build description.

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
    parent_dir = 'https://nexus.opendaylight.org/content/repositories/opendaylight.snapshot/org/opendaylight/integration/distribution-karaf/'

    # If the minor verison is given, get the sub-directory directly
    # else, find the latest sub-directory
    sub_dir = ''
    snapshot_dir = ''
    if build['version_minor']:
        sub_dir = '0.' + build['version_major'] + '.' + build['version_minor'] + '-SNAPSHOT/'
        snapshot_dir = parent_dir + sub_dir
    else:
        subdir_url = urlopen(parent_dir)
        content = subdir_url.read().decode('utf-8')
        all_dirs = BeautifulSoup(content, 'html.parser')

        # Loops through all the sub-directories present and stores the
        # latest sub directory.
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
    else:
        urlpath = urlopen(snapshot_dir)
        content = urlpath.read().decode('utf-8')
        html_content = BeautifulSoup(content, 'html.parser')

        snapshot_url = ''
        # Loops thorugh all the files present in `snapshot_dir`
        # and stores the url of latest tarball.
        for tag in html_content.find_all('a', href=True):
            if tag['href'].endswith('tar.gz'):
                snapshot_url = tag['href']

        # Get download_url
        build['download_url'] = snapshot_url

        # Get changelog_date from the snapshot URL
        # eg: 'distribution-karaf-0.5.2-20161202.230609-363.tar.gz'
        # '\d{8}' searches for the date in the url
        extract_date = re.search(r'\d{8}', snapshot_url)
        extract_date = extract_date.group(0)
        year = int(extract_date[:4])
        month = int(extract_date[4:6])
        date = int(extract_date[6:])

        # %a: Abbreviated weekday name
        # %b: Abbreviated month name
        # %d: Zero padded decimal number
        # %Y: Year
        # `changelog_date` is in the format: 'Sat Dec 10 2016'
        # Docs: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        build['changelog_date'] = datetime.date(year, month, date).strftime("%a %b %d %Y")

        # Assign codename
        build['codename'] = "SNAPSHOT"
        urlpath.close()

        build_rpm(build)


# When run as a script, accept a set of builds and execute them
if __name__ == "__main__":
    # Load RPM build variables from a YAML config file
    build_vars_path = os.path.join(project_root, "build_vars.yaml")
    with open(build_vars_path) as rpm_var_file:
        build_vars = yaml.load(rpm_var_file)

    # Accept the version(s) of the build(s) to perform as args
    # TODO: More docs on ArgParser and argument
    parser = argparse.ArgumentParser(conflict_handler='resolve')
    existing_build_group = parser.add_argument_group("Existing build")
    existing_build_group.add_argument(
        "-v", "--version", action="append", metavar="major minor patch rpm",
        nargs="*", help="RPM version(s) to build"
    )
    new_build_group = parser.add_argument_group("New build")
    new_build_group.add_argument("--major", help="Major (element) version to build")
    new_build_group.add_argument("--minor", help="Minor (SR) version to build")
    new_build_group.add_argument("--patch", help="Patch version to build")
    new_build_group.add_argument("--rpm",   help="RPM version to build")
    new_build_group.add_argument("--sysd_commit", help="Version of ODL unitfile to package")
    new_build_group.add_argument("--codename", help="Codename for ODL version")
    new_build_group.add_argument("--download_url", help="Tarball to repackage into RPM")
    new_build_group.add_argument("--changelog_date", help="Date this RPM was defined")
    new_build_group.add_argument("--changelog_name", help="Name of person who defined RPM")
    new_build_group.add_argument("--changelog_email", help="Email of person who defined RPM")

    # Arguments needed to build RPM from latest snapshot given a stable major branch
    latest_snap_group = parser.add_argument_group("Latest snapshot build")
    latest_snap_group.add_argument("--build-latest-snap", action='store_true',
        help="Build RPM from the latest snpashot")
    latest_snap_group.add_argument("--major", required='true', help="Stable branch from which to build the snapshot")
    latest_snap_group.add_argument("--minor", help="Minor version of the stable branch to build the snapshot")
    latest_snap_group.add_argument("--patch", help="Patch version to build")
    latest_snap_group.add_argument("--rpm",   help="RPM version to build")
    latest_snap_group.add_argument("--sysd_commit", help="Version of ODL unitfile to package")
    latest_snap_group.add_argument("--codename", help="Codename for ODL snapshot")
    latest_snap_group.add_argument("--changelog_name", help="Name of person who defined RPM")
    latest_snap_group.add_argument("--changelog_email", help="Email of person who defined RPM")

    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Parse the given args
    args = parser.parse_args()

    # Build list of RPM builds to perform
    builds = []
    if args.version:
        # Build a list of requested versions as dicts of version components
        versions = []
        version_keys = ["version_major", "version_minor", "version_patch",
                        "rpm_release"]
        # For each version arg, match all version components to build_vars name
        for version in args.version:
            versions.append(dict(zip(version_keys, version)))

        # Find every RPM build that matches any version argument
        # A passed version "matches" a build when the provided version
        # components are a subset of the version components of a build. Any
        # version components that aren't passed are simply not checked, so
        # they can't fail the match, effectively wild-carding them.
        for build in build_vars["builds"]:
            for version in versions:
                # Converts both dicts' key:value pairs to lists of tuples and
                # checks that each tuple in the version list is present in the
                # build list.
                if all(item in build.items() for item in version.items()):
                    builds.append(build)
    else:
        builds.append({"version_major": args.major,
                       "version_minor": args.minor,
                       "version_patch": args.patch,
                       "rpm_release": args.rpm,
                       "sysd_commit": args.sysd_commit,
                       "codename": args.codename,
                       "download_url": args.download_url,
                       "changelog_date": args.changelog_date,
                       "changelog_name": args.changelog_name,
                       "changelog_email": args.changelog_email})

    # If the flag `--build-latest-snap` is true, extract information from the snapshot URL,
    # else directly build the RPM
    for build in builds:
        if args.build_latest_snap:
            build_snapshot_rpm(build)
        else:
            build_rpm(build)
