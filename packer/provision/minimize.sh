#!/usr/bin/env bash

# Options:
#   -x: Echo commands
#   -e: Fail on errors
set -ex

# This doesn't seem to reduce the size of the box, and may break
# Docker builds. See comments on git.opendaylight.org/gerrit/#/c/50382.

# Write 0s in free space until full (full->exit 1, force 0)
#sudo dd if=/dev/zero of=/EMPTY bs=1M || true

# Remove pointer to all the 0-space
#sudo rm -f /EMPTY

# Block until the empty file has been removed, otherwise, Packer
# will try to kill the box while the disk is still full and that's bad
#sudo sync
