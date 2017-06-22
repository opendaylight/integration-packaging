#!/usr/bin/env python
##############################################################################
# Copyright (c) 2016 Daniel Farrell and Others.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################
"""Common entry point for building OpenDaylight packages: RPM or DEB """

import argparse
import datetime
import sys

from deb import build_deb
from rpm import build_rpm
import vars

try:
    from tzlocal import get_localzone
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv.\n")
    raise


def build_package(build):
    """Branches to deb or rpm pipeline

    :arg dict build: A dictionary containing all the build vars
    """
    if build["pkg_type"] == "rpm":
        build_rpm.build_rpm(build)
    elif build["pkg_type"] == "deb":
        # `java_version` is required only for building debs
        build.update({"java_version":
                      vars.get_java_version(build["version_major"])})
        build_deb.build_deb(build)
    else:
        print("Unknown package type")


if __name__ == "__main__":
    """Accept the package type and agruments required for build
    TODO: Add More docs on ArgParser and argument
    """
    parser = argparse.ArgumentParser(add_help=False,
                                     conflict_handler="resolve")
    parser._optionals.title = "Required Arguments"
    package_build_group = parser.add_mutually_exclusive_group(required=True)
    package_build_group.add_argument("--rpm", action="store_true",
                                     help="Builds RPM package")
    package_build_group.add_argument("--deb", action="store_true",
                                     help="Builds DEB package")

    new_build_group = parser.add_argument_group("New build")
    new_build_group.add_argument(
        "--download_url", help="Tarball to repackage into package")
    new_build_group.add_argument(
        "--sysd_commit", help="Version of ODL unitfile to package")
    new_build_group.add_argument(
        "--changelog_date", help="Date this package was defined")
    new_build_group.add_argument(
        "--changelog_time", help="Time this package was defined")
    new_build_group.add_argument(
        "--changelog_name", help="Name of person who defined this package")
    new_build_group.add_argument(
        "--changelog_email", help="Email of person who defined package")

    # Arguments needed to build a package from latest snapshot
    # given a stable major branch
    latest_snap_group = parser.add_argument_group("Latest snapshot build")
    latest_snap_group.add_argument("--build-latest-snap", action='store_true',
                                   help="Build package from latest snpashot")
    latest_snap_group.add_argument("--major", help="Stable branch from which "
                                   "to build the snapshot")
    latest_snap_group.add_argument("--minor", help="Minor version of the "
                                   "stable branch to build the snapshot")
    latest_snap_group.add_argument("--sysd_commit",
                                   help="Version of ODL unitfile to package")
    latest_snap_group.add_argument("--changelog_name",
                                   help="Name of person who defined package")
    latest_snap_group.add_argument("--changelog_email",
                                   help="Email of person who defined package")
    # Print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # Dict containing all the variables needed for a build
    build = {}

    # Parse the given args
    args = parser.parse_args()

    # Check if the package to be created is rpm or deb and initialize timestamp
    # details with current time for packages accordingly. For details on
    # strftime please refer : https://docs.python.org/2/library/datetime.html#
    # strftime-and-strptime-behavior. For details on get_localzone refer :
    # https://pypi.python.org/pypi/tzlocal
    if args.rpm:
        build.update({"pkg_type": "rpm"})
        # Building RPM only requires `changelog_date` in the format
        # "Day Month Date Year" For ex - Mon Jun 21 2017
        if not args.changelog_date:
            args.changelog_date = datetime.date.today().strftime("%a %b %d %Y")
    if args.deb:
        build.update({"pkg_type": "deb"})
        if not args.changelog_date:
            # Building Deb requires `changelog_date` and 'changelog_time' in
            # the format "Day, Date Month Year" For ex - Mon, 21 Jun 2017 and
            # time along with Time Zone information as UTC offset in format
            # HH:MM:SS +HHMM". For ex - 15:01:16 +0530
            args.changelog_date = datetime.date.today().\
                                                strftime("%a, %d %b %Y")
            local_tz = get_localzone()
            args.changelog_time = datetime.datetime.now(local_tz).\
                strftime("%H:%M:%S %z")
            # Add comment
            build.update({"changelog_time": args.changelog_time})

    # Check if `sysd_commit` has been passed as an arg
    # Use latest Int/Pack repo commit hash as sysd_commit var
    # unless passed by param
    if not args.sysd_commit:
        args.sysd_commit = vars.get_sysd_commit()

    # Autorelase and ODL release require a `download_url` as an arg to extract
    # version information. Snapshot builds urls can be fetched when
    # `version_major` and `version_major`(optional) are provided as args.
    if args.build_latest_snap:
        if args.major:
            args.download_url = vars.get_snap_url(args.major, args.minor)

    if args.download_url:
        version = vars.extract_version(args.download_url)
        build.update(version)

    # Common parameters for all new and snapshot builds
    build.update({"download_url": args.download_url,
                  "sysd_commit": args.sysd_commit,
                  "changelog_name": args.changelog_name,
                  "changelog_email": args.changelog_email,
                  "changelog_date": args.changelog_date,
                  })

    build_package(build)
