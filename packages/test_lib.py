##############################################################################
# Copyright (c) 2016 Daniel Farrell.  All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License v1.0 which accompanies this distribution,
# and is available at http://www.eclipse.org/legal/epl-v10.html
##############################################################################

"""Tests for package build logic helper library."""

import unittest

import lib


class TestExtractVersion(unittest.TestCase):

    """Test logic to extract ODL versions from artifact URLs."""

    nexus_url = "https://nexus.opendaylight.org/content/repositories"

    def test_carbon_release_url(self):
        """Test URL of the ODL Carbon release."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.release/org/opendaylight/integration/distribution-karaf/0.6.0-Carbon/distribution-karaf-0.6.0-Carbon.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "6")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "1")
        self.assertEqual(version["codename"], "-Carbon")

    def test_carbon_release_zip_url(self):
        """Test URL of the ODL Carbon release zip archive."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.release/org/opendaylight/integration/distribution-karaf/0.6.0-Carbon/distribution-karaf-0.6.0-Carbon.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "6")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "1")
        self.assertEqual(version["codename"], "-Carbon")

    def test_carbon_sr1_release_url(self):
        """Test URL of the ODL Carbon SR1 release."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.release/org/opendaylight/integration/distribution-karaf/0.6.1-Carbon/distribution-karaf-0.6.1-Carbon.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "6")
        self.assertEqual(version["version_minor"], "1")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "1")
        self.assertEqual(version["codename"], "-Carbon")

    def test_carbon_sr1_release_zip_url(self):
        """Test URL of the ODL Carbon SR1 release zip archive."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.release/org/opendaylight/integration/distribution-karaf/0.6.1-Carbon/distribution-karaf-0.6.1-Carbon.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "6")
        self.assertEqual(version["version_minor"], "1")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "1")
        self.assertEqual(version["codename"], "-Carbon")

    def test_carbon_autorelease_url(self):
        """Test URL of an ODL Carbon autorelease build."""
        # noqa ShellCheckBear
        url = "%s/autorelease-1996/org/opendaylight/integration/distribution-karaf/0.6.2-Carbon/distribution-karaf-0.6.2-Carbon.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "6")
        self.assertEqual(version["version_minor"], "2")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20171002rel1996")
        self.assertEqual(version["codename"], "-Carbon")

    def test_carbon_autorelease_zip_url(self):
        """Test URL of an ODL Carbon autorelease build zip archive."""
        # noqa ShellCheckBear
        url = "%s/autorelease-1996/org/opendaylight/integration/distribution-karaf/0.6.2-Carbon/distribution-karaf-0.6.2-Carbon.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "6")
        self.assertEqual(version["version_minor"], "2")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20171002rel1996")
        self.assertEqual(version["codename"], "-Carbon")

    def test_nitrogen_autorelease_url(self):
        """Test URL of an ODL Nitrogen autorelease build."""
        # noqa ShellCheckBear
        url = "%s/autorelease-1991/org/opendaylight/integration/karaf/0.7.0/karaf-0.7.0.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "7")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20170927rel1991")
        self.assertEqual(version["codename"], "")

    def test_nitrogen_autorelease_zip_url(self):
        """Test URL of an ODL Nitrogen autorelease build zip archive."""
        # noqa ShellCheckBear
        url = "%s/autorelease-1991/org/opendaylight/integration/karaf/0.7.0/karaf-0.7.0.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "7")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20170927rel1991")
        self.assertEqual(version["codename"], "")

    def test_carbon_snapshot_url(self):
        """Test URL of an ODL Carbon snapshot build."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/distribution-karaf/0.6.2-SNAPSHOT/distribution-karaf-0.6.2-20171003.084929-847.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "6")
        self.assertEqual(version["version_minor"], "2")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20171003snap847")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_carbon_snapshot_zip_url(self):
        """Test URL of an ODL Carbon snapshot build zip archive."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/distribution-karaf/0.6.2-SNAPSHOT/distribution-karaf-0.6.2-20171003.084929-847.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "6")
        self.assertEqual(version["version_minor"], "2")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20171003snap847")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_nitrogen_snapshot_url(self):
        """Test URL of an ODL Nitrogen snapshot build."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.7.0-SNAPSHOT/karaf-0.7.0-20170927.033128-2013.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "7")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20170927snap2013")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_nitrogen_snapshot_zip_url(self):
        """Test URL of an ODL Nitrogen snapshot build zip archive."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.7.0-SNAPSHOT/karaf-0.7.0-20170927.033128-2013.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "7")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20170927snap2013")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_oxygen_snapshot_url(self):
        """Test URL of an ODL Oxygen snapshot build."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.8.0-SNAPSHOT/karaf-0.8.0-20170928.142221-597.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20170928snap597")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_oxygen_snapshot_zip_url(self):
        """Test URL of an ODL Oxygen snapshot build zip archive."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.8.0-SNAPSHOT/karaf-0.8.0-20170928.142221-597.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20170928snap597")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_carbon_multipatch_zip_url(self):
        """Test URL of an ODL Carbon multipatch-test build zip archive."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/integration/distribution/distribution-karaf/0.6.2-SNAPSHOT/distribution-karaf-0.6.2-20171002.113256-59.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "6")
        self.assertEqual(version["version_minor"], "2")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20171002snap59")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_nitrogen_multipatch_zip_url(self):
        """Test URL of an ODL Nitrogen multipatch-test build zip archive."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/integration/distribution/karaf/0.7.1-SNAPSHOT/karaf-0.7.1-20171003.134117-9.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "7")
        self.assertEqual(version["version_minor"], "1")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20171003snap9")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_oxygen_multipatch_zip_url(self):
        """Test URL of an ODL Oxygen multipatch-test build zip archive."""
        # noqa ShellCheckBear
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/integration/distribution/karaf/0.8.0-SNAPSHOT/karaf-0.8.0-20171003.122621-24.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20171003snap24")
        self.assertEqual(version["codename"], "-SNAPSHOT")


class TestGetSnapURL(unittest.TestCase):

    """Test logic get URL to latest snapshot build of given major version."""

    url_base = "https://nexus.opendaylight.org/content/repositories/opendaylight.snapshot/org/opendaylight/integration"

    def validate_snap_url(self, snap_url):
        """Helper for validating snapshot URLs are sane."""
        self.assertIn(self.url_base, snap_url)
        self.assertIn("tar.gz", snap_url)
        self.assertNotIn("release", snap_url)
        self.assertNotIn("public", snap_url)

    def test_carbon(self):
        """Test Carbon major version gives sane snapshot URL."""
        self.validate_snap_url(lib.get_snap_url("6"))

    def test_nitrogen(self):
        """Test Nitrogen major version gives sane snapshot URL."""
        self.validate_snap_url(lib.get_snap_url("7"))

    def test_oxygen(self):
        """Test Oxygen major version gives sane snapshot URL."""
        self.validate_snap_url(lib.get_snap_url("8"))


class TestGetDistroNamePrefix(unittest.TestCase):

    """Test logic to get Karaf 3/4 distro name prefix per ODL major version."""

    k3_distro_prefix = "distribution-karaf"
    k4_distro_prefix = "karaf"

    def test_carbon(self):
        """Test Carbon major version gives Karaf 3 prefix."""
        distro_prefix = lib.get_distro_name_prefix("6")
        self.assertEqual(distro_prefix, self.k3_distro_prefix)

    def test_nitrogen(self):
        """Test Nitrogen major version gives Karaf 4 prefix."""
        distro_prefix = lib.get_distro_name_prefix("7")
        self.assertEqual(distro_prefix, self.k4_distro_prefix)

    def test_oxygen(self):
        """Test Oxygen major version gives Karaf 4 prefix."""
        distro_prefix = lib.get_distro_name_prefix("8")
        self.assertEqual(distro_prefix, self.k4_distro_prefix)

    def test_carbon_int(self):
        """Test Carbon major version as int gives Karaf 3 prefix."""
        distro_prefix = lib.get_distro_name_prefix(6)
        self.assertEqual(distro_prefix, self.k3_distro_prefix)

    def test_nitrogen_int(self):
        """Test Nitrogen major version as int gives Karaf 4 prefix."""
        distro_prefix = lib.get_distro_name_prefix(7)
        self.assertEqual(distro_prefix, self.k4_distro_prefix)

    def test_oxygen_int(self):
        """Test Oxygen major version as int gives Karaf 4 prefix."""
        distro_prefix = lib.get_distro_name_prefix(8)
        self.assertEqual(distro_prefix, self.k4_distro_prefix)
