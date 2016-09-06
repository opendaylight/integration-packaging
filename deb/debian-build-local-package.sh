#!/bin/bash

CHANGELOGNAME='John Doe'
CHANGELOGEMAIL='john@doe.com'

check_tarball ()
{
if [ -f $TARBALL ];
then
   cp $TARBALL .
else
   echo "Error: distribution-karaf-tarball not found"
   exit 1
fi
}

check_distribution ()
{
DISTRIBUTION_PATH=$1
TARBALL_PATH=$DISTRIBUTION_PATH/distribution-karaf/target
if [ -d $TARBALL_PATH ];
then
   TARBALL=$(ls $TARBALL_PATH/distribution-karaf-*.tar.gz)
   check_tarball
else
   echo "Error: distribution-karaf-directory not found"
   exit 1
fi
}

if [ $# -ne 2 ]; then
	echo "Error: Two Arguments expected"
        echo "Usage: --dist <distribution-karaf-directory>"
        echo "       --dist /home/user/distribution"
        echo "       --file <distribution-karaf-tarball>"
	echo "       --file distribution-karaf-x.y.z-XXXXX.tar.gz"
	exit 127
fi

case "$1" in
        --dist) 
		check_distribution $2
            ;;
        --file)
		TARBALL=$2
		check_tarball 
            ;;
        *) 
		echo "Usage: --dist <distribution-karaf-directory>"
		echo "       --dist /home/user/distribution"
		echo "       --file <distribution-karaf-tarball>"
		echo "       --file distribution-karaf-x.y.z-XXXXX.tar.gz"
		echo "       --file <distribution-karaf-tarball>"
		exit 1
esac 

FILENAME=$(basename "$TARBALL")
FILENAME="${FILENAME%.*}"
FILENAME="${FILENAME%.*}"
CODENAME="${FILENAME##*-}"
VERSION="${FILENAME%-*}" 
VERSION="${VERSION##*-}" 
VERSION_PATCH="${VERSION##*.}"
VERSION_MINOR="${VERSION%.*}"
VERSION_MINOR="${VERSION_MINOR##*.}"
VERSION_MAJOR="${VERSION%%.*}"

mkdir debian

echo '#!/usr/bin/make -f' > debian/rules 
echo '' >> debian/rules 
echo 'VERSION_MAJOR = '$VERSION_MAJOR >> debian/rules 
echo 'VERSION_MINOR = '$VERSION_MINOR >> debian/rules 
echo 'VERSION_PATCH = '$VERSION_PATCH >> debian/rules 
echo 'CODENAME = '$CODENAME >> debian/rules 
echo 'VERSION = $(VERSION_MAJOR).$(VERSION_MINOR).$(VERSION_PATCH)-$(CODENAME)' >> debian/rules 
echo 'PACKAGEVERSION = $(VERSION)-$(DISTRIBUTION)0' >> debian/rules 
echo 'TARBALL = distribution-karaf-$(VERSION).tar.gz' >> debian/rules 
echo '' >> debian/rules 
echo '%:' >> debian/rules 
echo -e '\tdh $@ --with systemd' >> debian/rules 
echo '' >> debian/rules 
echo 'override_dh_auto_clean:' >> debian/rules 
echo 'override_dh_auto_test:' >> debian/rules 
echo 'override_dh_auto_build:' >> debian/rules 
echo 'override_dh_usrlocal:' >> debian/rules 
echo 'override_dh_auto_install:' >> debian/rules 
echo -e '\ttar -xf $(TARBALL)' >> debian/rules 
echo -e '\tmkdir -p ./debian/opendaylight/opt/opendaylight/' >> debian/rules 
echo -e '\tcp -r ./distribution-karaf-$(VERSION)/* ./debian/opendaylight/opt/opendaylight/' >> debian/rules 
echo '' >> debian/rules 
echo 'override_dh_gencontrol:' >> debian/rules 
echo -e '\tdh_gencontrol -- -v$(PACKAGEVERSION)' >> debian/rules 


echo 'opendaylight ('$VERSION_MAJOR'.'$VERSION_MINOR'.'$VERSION_PATCH'-1) UNRELEASED; urgency=medium' > debian/changelog
echo '' >> debian/changelog
echo '  * Release: OpenDaylight '$VERSION_MAJOR'.'$VERSION_MINOR'.'$VERSION_PATCH'-'$CODENAME >> debian/changelog
echo ' -- '$CHANGELOGNAME' <'$CHANGELOGEMAIL'>  '$(date +"%a, %d %b %Y %T %z") >> debian/changelog

echo 'Source: opendaylight' > debian/control 
echo 'Build-Depends: debhelper (>= 9), wget, ca-certificates, dh-systemd' >> debian/control
echo 'Maintainer: '$CHANGELOGNAME' <'$CHANGELOGEMAIL'> ' >> debian/control
echo '' >> debian/control
echo 'Package: opendaylight' >> debian/control
echo 'Depends: ${misc:Depends}, adduser, openjdk-8-jre-headless' >> debian/control
echo 'Architecture: any' >> debian/control
echo 'Description: OpenDaylight SDN controller' >> debian/control

cp templates/compat templates/karaf templates/opendaylight.install templates/opendaylight.postinst templates/opendaylight.postrm templates/opendaylight.upstart debian
dpkg-buildpackage -us -uc -b
rm $TARBALL
rm -rf $FILENAME
cd ..

