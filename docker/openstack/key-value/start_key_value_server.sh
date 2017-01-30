#!/bin/bash
_hostname=consul
_container_name=$_hostname
_image=progrium/consul

docker run -d -p 8500:8500 -h $_hostname --name $_container_name \
    $_image -server -bootstrap

export _consul_IP=$( docker inspect -f '{{.NetworkSettings.IPAddress}}' consul)

echo "Consul key-value server is now running at $_consul_IP:8500"
docker ps | grep $_container_name
