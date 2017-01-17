#!/bin/bash
# file: build_compute.sh
# info: builds a docker compute image 
IMAGE_NAME=s3p/compute:latest

docker build -t ${IMAGE_NAME} \
    --build-arg http_proxy=$http_proxy --build-arg https_proxy=$https_proxy .
