A temporary readme file
-------------------------------

`build_debianfile.py` reads build_vars.yaml and uses 
jinja2 templates to create debian files specific to a build. 
The directory `templates` contains jinja2 templates for
files debian/control, debian/rules, debian/changelog. These files
change dynamically for every build. The other files are mostly 
the same for all builds.

Usage:

In `templates` dir:

  $ python build_debianfiles.py
   - An `opendaylight` dir is created
   - The `opendaylight` dir contains specialized Opendaylight 
     directory name per-build

  $ opendaylight/opendaylight-$version_major.$version_minor.$version_patch-$pkg_version/

  $ dpkg-buildpackage -us -uc -b
   - This creates a .deb package in `opendaylight` directory
   - Install this package


Reference:
 
  https://github.com/opendaylight/integration-packaging/blob/master/rpm/build_vars.yaml
  https://github.com/opendaylight/integration-packaging/blob/master/rpm/specs/build_specs.py
  https://github.com/opendaylight/integration-packaging/tree/master/rpm/specs

