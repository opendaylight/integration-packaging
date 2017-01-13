#!/bin/bash -eux

sudo dnf -y remove gcc cpp kernel-devel kernel-headers perl
sudo dnf -y clean all
