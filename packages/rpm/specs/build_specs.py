#!/usr/bin/env python
"""Build RPM .spec files from build description and a Jinja2 .spec template."""

import os
from string import Template
import sys

try:
    import jinja2
except ImportError:
    sys.stderr.write("We recommend using our included Vagrant env.\n")
    sys.stderr.write("Else, do `pip install -r requirements.txt` in a venv.\n")
    raise

# Path to the directory that contains this file is assumed to be the spec dir
spec_dir = os.path.dirname(os.path.abspath(__file__))

# Create the Jinja2 Environment
env = jinja2.Environment(loader=jinja2.FileSystemLoader(spec_dir))

# Load the OpenDaylight RPM .spec file Jinja2 template
template = env.get_template("opendaylight.spec")

# Python string Template, specialized into a specfile file name per-build
specfile_template = Template("opendaylight-$version_major.$version_minor."
                             "$version_patch-$pkg_version.spec")


def build_spec(build):
    """Build RPM .spec file for the given build description using a template.

    :param build: Description of an RPM build, typically from build.py
    :type build: dict

    """
    specfile_name = specfile_template.substitute(build)
    specfile_path = os.path.join(spec_dir, specfile_name)
    with open(specfile_path, "w") as specfile:
        specfile.write(template.render(build))
