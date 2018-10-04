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

    def test_oxygen_release_url(self):
        """Test URL of the ODL Oxygen release."""
        url = "%s/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.0/karaf-0.8.0.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "1")
        self.assertEqual(version["codename"], "")

    def test_oxygen_release_zip_url(self):
        """Test URL of the ODL Oxygen release zip archive."""
        url = "%s/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.0/karaf-0.8.0.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "1")
        self.assertEqual(version["codename"], "")

    def test_oxygen_sr1_url(self):
        """Test URL of the ODL Oxygen SR2."""
        url = "%s/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.2/karaf-0.8.2.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "2")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "1")
        self.assertEqual(version["codename"], "")

    def test_oxygen_sr1_zip_url(self):
        """Test URL of the ODL Oxygen SR2 zip archive."""
        url = "%s/repositories/opendaylight.release/org/opendaylight/integration/karaf/0.8.2/karaf-0.8.2.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "2")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "1")
        self.assertEqual(version["codename"], "")

    def test_oxygen_snapshot_url(self):
        """Test URL of an ODL Oxygen snapshot build."""
        # NB: This will need to be updated as old builds expire
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.8.0-SNAPSHOT/karaf-0.8.0-20180202.194543-1393.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20180202snap1393")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_oxygen_snapshot_zip_url(self):
        """Test URL of an ODL Oxygen snapshot build zip archive."""
        # NB: This will need to be updated as old builds expire
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.8.0-SNAPSHOT/karaf-0.8.0-20180202.194543-1393.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20180202snap1393")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_fluorine_snapshot_url(self):
        """Test URL of an ODL Fluorine snapshot build."""
        # NB: This will need to be updated as old builds expire
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.9.0-SNAPSHOT/karaf-0.9.0-20180411.203859-563.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "9")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20180411snap563")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_fluorine_snapshot_zip_url(self):
        """Test URL of an ODL Fluorine snapshot build zip archive."""
        # NB: This will need to be updated as old builds expire
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.9.0-SNAPSHOT/karaf-0.9.0-20180411.203859-563.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "9")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20180411snap563")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_neon_snapshot_url(self):
        """Test URL of an ODL Neon snapshot build."""
        # NB: This will need to be updated as old builds expire
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.10.0-SNAPSHOT/karaf-0.10.0-20181004.142605-697.tar.gz" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "10")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20181004snap697")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_neon_snapshot_zip_url(self):
        """Test URL of an ODL Neon snapshot build zip archive."""
        # NB: This will need to be updated as old builds expire
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/karaf/0.10.0-SNAPSHOT/karaf-0.10.0-20181004.142605-697.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "10")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20181004snap697")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_oxygen_multipatch_zip_url(self):
        """Test URL of an ODL Oxygen multipatch-test build zip archive."""
        # NB: This will need to be updated as old builds expire
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/integration/distribution/karaf/0.8.0-SNAPSHOT/karaf-0.8.0-20180204.191936-134.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "8")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20180204snap134")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_fluorine_multipatch_zip_url(self):
        """Test URL of an ODL Fluorine multipatch-test build zip archive."""
        # NB: This will need to be updated as old builds expire
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/integration/distribution/karaf/0.9.0-SNAPSHOT/karaf-0.9.0-20180531.192226-59.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "9")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20180531snap59")
        self.assertEqual(version["codename"], "-SNAPSHOT")

    def test_neon_multipatch_zip_url(self):
        """Test URL of an ODL Neon multipatch-test build zip archive."""
        # NB: This will need to be updated as old builds expire
        url = "%s/opendaylight.snapshot/org/opendaylight/integration/integration/distribution/karaf/0.10.0-SNAPSHOT/karaf-0.10.0-20180925.093600-5.zip" % self.nexus_url
        version = lib.extract_version(url)
        self.assertEqual(version["version_major"], "10")
        self.assertEqual(version["version_minor"], "0")
        self.assertEqual(version["version_patch"], "0")
        self.assertEqual(version["pkg_version"], "0.1.20180925snap5")
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

    def test_oxygen(self):
        """Test Oxygen major version gives sane snapshot URL."""
        self.validate_snap_url(lib.get_snap_url("8"))

    def test_fluorine(self):
        """Test Fluorine major version gives sane snapshot URL."""
        self.validate_snap_url(lib.get_snap_url("9"))


class TestGetDistroNamePrefix(unittest.TestCase):

    """Test logic to get Karaf 3/4 distro name prefix per ODL major version."""

    k3_distro_prefix = "distribution-karaf"
    k4_distro_prefix = "karaf"

    def test_oxygen(self):
        """Test Oxygen major version gives Karaf 4 prefix."""
        distro_prefix = lib.get_distro_name_prefix("8")
        self.assertEqual(distro_prefix, self.k4_distro_prefix)

    def test_oxygen_int(self):
        """Test Oxygen major version as int gives Karaf 4 prefix."""
        distro_prefix = lib.get_distro_name_prefix(8)
        self.assertEqual(distro_prefix, self.k4_distro_prefix)

    def test_fluorine(self):
        """Test Fluorine major version gives Karaf 4 prefix."""
        distro_prefix = lib.get_distro_name_prefix("9")
        self.assertEqual(distro_prefix, self.k4_distro_prefix)

    def test_fluorine_int(self):
        """Test Fluorine major version as int gives Karaf 4 prefix."""
        distro_prefix = lib.get_distro_name_prefix(9)
        self.assertEqual(distro_prefix, self.k4_distro_prefix)


class TestGetSysdCommit(unittest.TestCase):

    """Test fn to get most recent Int/Pack hash to use as sysd file version."""

    def test_type(self):
        """Check that returned value is of the right type."""
        sysd_hash = lib.get_sysd_commit()
        self.assertIsInstance(sysd_hash, str)

    def test_len(self):
        """Check that returned value the normal length for a commit hash."""
        sysd_hash = lib.get_sysd_commit()
        self.assertEqual(len(sysd_hash), 40)

    def test_only_valid_chars(self):
        """Check that returned value only contains typical commit hash chars."""
        sysd_hash = lib.get_sysd_commit()
        self.assertRegexpMatches(sysd_hash, "^[A-Za-z0-9-]+$")


class TestGetJavaVersion(unittest.TestCase):

    """Test fn to get Java version required for a given ODL version."""

    def test_type_given_int(self):
        """Pass int, check that returned value is of the right type."""
        java_version = lib.get_java_version(6)
        self.assertIsInstance(java_version, int)

    def test_type_given_str(self):
        """Pass int, check that returned value is of the right type."""
        java_version = lib.get_java_version("6")
        self.assertIsInstance(java_version, int)

    def test_old_given_int(self):
        """Pass old ODL major version, check that Java 7 returned."""
        java_version = lib.get_java_version(4)
        self.assertEqual(java_version, 7)

    def test_old_given_str(self):
        """Pass old ODL major version, check that Java 7 returned."""
        java_version = lib.get_java_version("4")
        self.assertEqual(java_version, 7)

    def test_oxygen_given_int(self):
        """Pass Oxygen major version, check that Java 8 returned."""
        java_version = lib.get_java_version(8)
        self.assertEqual(java_version, 8)

    def test_oxygen_given_str(self):
        """Pass Oxygen major version, check that Java 8 returned."""
        java_version = lib.get_java_version("8")
        self.assertEqual(java_version, 8)

    def test_fluorine_given_int(self):
        """Pass Fluorine major version, check that Java 8 returned."""
        java_version = lib.get_java_version(9)
        self.assertEqual(java_version, 8)

    def test_fluorine_given_str(self):
        """Pass Fluorine major version, check that Java 8 returned."""
        java_version = lib.get_java_version("9")
        self.assertEqual(java_version, 8)


class TestGetChangelogDate(unittest.TestCase):

    """Test lib fn that gives date for changelog in RPM or Deb format."""

    def test_type_rpm(self):
        """Test type of return object is correct given RPM arg."""
        changelog_date = lib.get_changelog_date("rpm")
        self.assertIsInstance(changelog_date, str)

    def test_type_deb(self):
        """Test type of return object is correct given Deb arg."""
        changelog_date = lib.get_changelog_date("deb")
        self.assertIsInstance(changelog_date, str)

    def test_has_year_rpm(self):
        """Test returned value has a year in it given RPM arg."""
        changelog_date = lib.get_changelog_date("rpm")
        self.assertRegexpMatches(changelog_date, "[20]\d\d")

    def test_has_year_deb(self):
        """Test returned value has a year in it given Deb arg."""
        changelog_date = lib.get_changelog_date("deb")
        self.assertRegexpMatches(changelog_date, "[20]\d\d")

    def test_has_month_rpm(self):
        """Test returned value has a month in it given RPM arg."""
        changelog_date = lib.get_changelog_date("rpm")
        self.assertRegexpMatches(
            changelog_date,
            "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec")

    def test_has_month_deb(self):
        """Test returned value has a month in it given Deb arg."""
        changelog_date = lib.get_changelog_date("deb")
        self.assertRegexpMatches(
            changelog_date,
            "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec")

    def test_has_day_rpm(self):
        """Test returned value has a day in it given RPM arg."""
        changelog_date = lib.get_changelog_date("rpm")
        self.assertRegexpMatches(
            changelog_date,
            "Mon|Tue|Wed|Thu|Fri|Sat|Sun")

    def test_has_day_deb(self):
        """Test returned value has a day in it given Deb arg."""
        changelog_date = lib.get_changelog_date("deb")
        self.assertRegexpMatches(
            changelog_date,
            "Mon|Tue|Wed|Thu|Fri|Sat|Sun")
