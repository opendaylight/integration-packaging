#!/bin/bash
_hostname=consul
_container_name=$_hostname
_image=progrium/consul

docker stop $_container_name

docker ps | grep $_container_name
