#!/bin/bash -eux

dnf -y remove gcc cpp kernel-devel kernel-headers perl
dnf -y clean all
