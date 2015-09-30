# ODL is a noarch package, so this isn't necessary. It's also very slow.
%define __jar_repack 0

Name:       opendaylight
Version:    2.4.0
# The Fedora/CentOS packaging guidelines *require* the use of a disttag. ODL's
#   RPM build doesn't do anything Fedora/CentOS specific, so the disttag is
#   unnecessary and unused in our case, but both the docs and the pros (apevec)
#   agree that we should include it.
# See: https://fedoraproject.org/wiki/Packaging:DistTag
Release:    1.el7
BuildArch:  noarch
Summary:    OpenDaylight SDN Controller
Group:      Applications/Communications
License:    EPL-1.0
URL:        http://www.opendaylight.org
Source0:    https://nexus.opendaylight.org/content/groups/public/org/opendaylight/integration/distribution-karaf/0.2.4-Helium-SR4/distribution-karaf-0.2.4-Helium-SR4.tar.gz
Source1:    %name-c6d7ee1f21d62ff8ffb741c7a12c3d8d3aa3d6ed.service.tar.gz
Buildroot:  /tmp
# Required for ODL at run time
Requires:   java = 1:1.7.0
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
OpenDaylight Helium-SR4

%prep
# Extract Source0 (ODL archive)
%autosetup -n distribution-karaf-0.2.4-Helium-SR4
# Extract Source1 (systemd config)
%autosetup -T -D -b 1 -c -n %name-c6d7ee1f21d62ff8ffb741c7a12c3d8d3aa3d6ed.service

%install
# Create directory in build root for ODL
mkdir -p $RPM_BUILD_ROOT/opt/%name
# Copy ODL from archive to its dir in build root
cp -r ../distribution-karaf-0.2.4-Helium-SR4/* $RPM_BUILD_ROOT/opt/%name
# Create directory in build root for systemd .service file
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
# Copy ODL's systemd .service file to correct dir in build root
cp ../../BUILD/%name-c6d7ee1f21d62ff8ffb741c7a12c3d8d3aa3d6ed.service/%name-c6d7ee1f21d62ff8ffb741c7a12c3d8d3aa3d6ed.service $RPM_BUILD_ROOT/%{_unitdir}/%name.service

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
* Tue Sep 15 2015 Daniel Farrell <dfarrell@redhat.com> - 2.4.0-1
- Create Helium SR4 RPM
