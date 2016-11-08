#!/usr/bin/env python
"""Build OpenDaylight's RPMs using YAML build configs and Jinja2 templates."""

import os
import sys
import argparse
import shutil
import subprocess
import re
from string import Template
from datetime import datetime

try:
    import yaml
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


def extract_version(url):
    """Determine ODL version information from the ODL tarball build URL.

    :param url: URL of the ODL tarball build for building RPMs.
    :type url: string
    returns: Dict of ODL major version, minor version, patch version,
              RPM relase version and elemental codename.

    """
    # Substitute the part of the build URL not required with white space
    date_url = re.sub('distribution-karaf-.*\.tar\.gz$', '', url)
    # Set date_url as an environmental variable for it to be used in a subprocess
    os.environ["date_url"] = date_url
    # Extract ODL artifact's date by scraping data from the build URL
    odl_date = subprocess.Popen("curl -s $date_url | grep tar.gz -A1 | tail -n1 | sed \"s/<td>//g\""
                                "| sed \"s/\\n//g\" | awk '{print $3,$2,$6}' ", shell=True,
                                stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE).stdout.read().rstrip().strip("</td>")
    date = datetime.strptime(odl_date, "%d %b %Y").strftime('%Y%m%d')

    if "autorelease" in url:
        # Search the ODL autorelease build URL to match the Build ID that follows "autorelease-".
        # eg: https://nexus.opendaylight.org/content/repositories/autorelease-1533/org/
        #     opendaylight/integration/distribution-karaf/0.4.4-Beryllium-SR4/
        # build_id = 1533
        build_id = re.search(r'\/(autorelease)-([0-9]+)\/', url).group(2)
        rpm_release = "0.1." + date + "rel" + build_id
    elif "snapshot" in url:
        # Search the ODL snapshot build URL to match the Build ID that preceeds ".tar.gz".
        # eg: https://nexus.opendaylight.org/content/repositories/opendaylight.snapshot/org/
        #     opendaylight/integration/distribution-karaf/0.6.0-SNAPSHOT/
        #     distribution-karaf-0.6.0-20161201.031047-2242.tar.gz
        # build_id = 2242
        build_id = re.search(r'-([0-9]+)\.(tar\.gz)', url).group(1)
        rpm_release = "0.1." + date + "snap" + build_id
    elif "public" or "opendaylight.release" in url:
        rpm_release = "1"
    else:
        raise ValueError("Unrecognized URL {}".format(url))

    version = {}
    # Search the ODL build URL to match 0.major.minor-codename-SR and extarct version information.
    # eg: release: https://nexus.opendaylight.org/content/repositories/public/org/opendaylight/
    #     integration/distribution-karaf/0.3.3-Lithium-SR3/
    #     distribution-karaf-0.3.3-Lithium-SR3.tar.gz
    #     match: 0.3.3-Lithium-SR3
    odl_version = re.search(r'\/(\d)\.(\d)\.(\d).(.*)\/', url)
    version["version_major"] = odl_version.group(2)
    version["version_minor"] = odl_version.group(3)
    version["version_patch"] = "0"
    version["rpm_release"] = rpm_release
    version["codename"] = odl_version.group(4)
    return version


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


# When run as a script, accept a set of builds and execute them
if __name__ == "__main__":
    # Load RPM build variables from a YAML config file
    build_vars_path = os.path.join(project_root, "build_vars.yaml")
    with open(build_vars_path) as rpm_var_file:
        build_vars = yaml.load(rpm_var_file)

    # Accept the version(s) of the build(s) to perform as args
    # TODO: More docs on ArgParser and argument
    parser = argparse.ArgumentParser()
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

    for build in builds:
        build_rpm(build)
