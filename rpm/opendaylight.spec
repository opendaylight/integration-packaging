# ODL is a noarch package, so this isn't necessary. It's also very slow.
%define __jar_repack 0

Name:       opendaylight
Version:    %{rpm_version}
# The Fedora/CentOS packaging guidelines *require* the use of a disttag. ODL's
#   RPM build doesn't do anything Fedora/CentOS specific, so the disttag is
#   unnecessary and unused in our case, but both the docs and the pros (apevec)
#   agree that we should include it.
# See: https://fedoraproject.org/wiki/Packaging:DistTag
Release:    %{rpm_release}%{dist}
BuildArch:  noarch
Summary:    OpenDaylight SDN Controller
Group:      Applications/Communications
License:    EPL-1.0
URL:        http://www.opendaylight.org
Source0:    https://nexus.opendaylight.org/content/groups/public/org/opendaylight/integration/distribution-karaf/%{odl_version}-%{codename}/distribution-karaf-%{odl_version}-%{codename}.tar.gz
Source1:    https://github.com/dfarrell07/opendaylight-systemd/archive/%{sysd_commit}/opendaylight-systemd-%{sysd_commit}.tar.gz
Buildroot:  /tmp
# Required for ODL at run time
Requires:   java %{java_version}
# Required for creating odl group
Requires(pre): shadow-utils
# Required for configuring systemd
BuildRequires: systemd

%pre
# Create `odl` user/group
# Short circuits if the user/group already exists
# Home dir must be a valid path for various files to be created in it
getent passwd odl > /dev/null || useradd odl -M -d $RPM_BUILD_ROOT/opt/%name
getent group odl > /dev/null || groupadd odl

%description
OpenDaylight %{codename}

%prep
# Extract Source0 (ODL archive)
%autosetup -n distribution-karaf-%{odl_version}-%{codename}
# Extract Source1 (systemd config)
%autosetup -T -D -b 1 -n opendaylight-systemd-%{sysd_commit}

%install
# Create directory in build root for ODL
mkdir -p $RPM_BUILD_ROOT/opt/%name
# Copy ODL from archive to its dir in build root
cp -r ../distribution-karaf-%{odl_version}-%{codename}/* $RPM_BUILD_ROOT/opt/%name
# Create directory in build root for systemd .service file
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
# Copy ODL's systemd .service file to correct dir in build root
cp ../../BUILD/opendaylight-systemd-%{sysd_commit}/opendaylight.service $RPM_BUILD_ROOT/%{_unitdir}

%postun
# When the RPM is removed, the subdirs containing new files wouldn't normally
#   be deleted. Manually clean them up.
#   Warning: This does assume there's no data there that should be preserved
rm -rf $RPM_BUILD_ROOT/opt/%name

%files
# ODL will run as odl:odl, set as user:group for ODL dir, don't override mode
%attr(-,odl,odl) /opt/%name
# Configure systemd unitfile user/group/mode
%attr(0644,root,root) %{_unitdir}/%name.service


%changelog
* Tue Sep 15 2015 Daniel Farrell <dfarrell@redhat.com> - 3.1.0-1
- Create Lithium SR1 RPM
* Tue Sep 15 2015 Daniel Farrell <dfarrell@redhat.com> - 2.4.0-1
- Create Helium SR4 RPM
* Fri Jul 17 2015 Daniel Farrell <dfarrell@redhat.com> - 3.0.0-2
- Include required disttag in RPM release version
* Tue Jul 14 2015 Daniel Farrell <dfarrell@redhat.com> - 3.0.0-1
- Upgrade from Helium SR3 to Lithium
* Thu Apr 16 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.3-2
- Force Java version 1.7
* Mon Mar 23 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.3-1
- Upgrade from Helium SR2 to Helium SR3
* Sun Mar 15 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.2-4
- Don't override ODL dir mode, explicitly set unitfile owner:group
* Fri Mar 13 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.2-3
- Don't include ODL version in ODL dir name
* Tue Feb 10 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.2-2
- Bugfix in URL to download ODL systemd .service file
* Sat Jan 31 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.2-1
- Upgrade from Helium SR1.1 to Helium SR2
* Thu Jan 29 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.1-6
- Give odl user a valid home dir for automatically created files
* Tue Jan 13 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.1-5
- Set ODL ownership to odl:odl vs root:odl
* Mon Jan 12 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.1-4
- Added systemd config as a source
* Sat Jan 10 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.1-3
- Completely clean up ODL after uninstall
* Fri Jan 9 2015 Daniel Farrell <dfarrell@redhat.com> - 0.2.1-2
- Added systemd configuration
* Tue Dec 16 2014 Daniel Farrell <dfarrell@redhat.com> - 0.2.1-1
- Initial Karaf-based RPM
