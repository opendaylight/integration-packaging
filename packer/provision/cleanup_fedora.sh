#!/bin/bash -eux

yum -y remove gcc cpp kernel-devel kernel-headers perl
yum -y clean all
