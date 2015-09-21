#!/usr/bin/env python
# Build RPM .spec files from YAML RPM config and a Jinja2 .spec template

import os

try:
  import yaml
  from jinja2 import Environment, FileSystemLoader
except ImportError:
  sys.stderr.write("ERROR: Are you using our Vagrant env?")
  raise

# Path to the directory that contains this file is assumed to be the spec dir
spec_dir = os.path.dirname(os.path.abspath(__file__))

# Create the Jinja2 Environment
env = Environment(loader=FileSystemLoader(spec_dir))

# Load the OpenDaylight RPM .spec file template
template = env.get_template("opendaylight.spec")

# Load RPM build variables from a YAML config file
with open(os.path.join(spec_dir, "../build_vars.yaml")) as var_file:
  rpm_vars = yaml.load(var_file)

def build_spec(build):
  """Build the RPM .spec file from a template for the given build description.

  :param build: Description of an RPM build, typically from rpm_vars.yaml
  :type build: dict

  """
  specfile_name = "opendaylight-{}.{}.{}-{}.spec".format(
    build["version_major"],
    build["version_minor"],
    build["version_patch"],
    build["rpm_release"])
  specfile_path = os.path.join(spec_dir, specfile_name)
  with open(specfile_path, "w") as specfile:
    specfile.write(template.render(build))

# If run as a script, build .spec files for all builds
if __name__ == "__main__":
  for build in rpm_vars["builds"]:
    build_spec(build)
