import datetime
import re
import subprocess


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
        rpm_release = "0.1." + date + "rel" + build_id
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
        rpm_release = "0.1." + odl_rpm.group(3) + "snap" + odl_rpm.group(5)
    elif "public" or "opendaylight.release" in url:
        rpm_release = "1"
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
    version["rpm_release"] = rpm_release
    version["codename"] = odl_version.group(4)
    return version


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
