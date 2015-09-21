#!/usr/bin/env python
# Build RPM .spec files from YAML RPM config and a Jinja2 .spec template

import os

import yaml
from jinja2 import Environment, FileSystemLoader

# Path to OpenDaylight .spec file template dir
spec_dir = os.path.dirname(os.path.abspath(__file__))

# Create the Jinja2 Environment
env = Environment(loader=FileSystemLoader(spec_dir))

# Load the OpenDaylight RPM .spec file template
template = env.get_template("opendaylight.spec")

# Load RPM build variables from a YAML config file
with open(os.path.join(spec_dir, "../build_vars.yaml")) as var_file:
  rpm_vars = yaml.load(var_file)

# Use the RPM .spec template to build a .spec file for each build vars set
for build in rpm_vars["builds"]:
  specfile_name = "opendaylight-{}.{}.{}-{}.spec".format(
    build["version_major"],
    build["version_minor"],
    build["version_patch"],
    build["rpm_release"])
  specfile_path = os.path.join(spec_dir, specfile_name)
  with open(specfile_path, "w") as specfile:
    specfile.write(template.render(build))
