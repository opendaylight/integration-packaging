#!/usr/bin/env bash
# Minimize the size of the resulting image

# Echo commands as they are run
set -x

sudo dd if=/dev/zero of=/EMPTY bs=1M
sudo rm -f /EMPTY
sudo sync
