# OpenDaylight Docker Build

Launch docker build task for ODL version 15.2.0

```
$ docker build . -f Dockerfile -t opendaylight:15.2.0
```

Run container

```
$ docker run -d -p 8181:8181 --env FEATURES=odl-restconf,odl-netconf-topology opendaylight:15.2.0
```
