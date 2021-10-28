# OpenDaylight Helm Chart

OpenDaylight Helm Chart is a packaging for kubernetes deployment.
The composition of this chart consist of statefulset that can scale to multiple standalone instances of OpenDaylight Pods.

## Customization

Before deploying, there are several areas can be customized.
Either by editing values.yaml or using --set flag pass-in with the helm command 
e.g
```
helm install sdnc opendaylight --set persistence.enabled=true
```

### Java Memory and GC settings

In values.yaml, java max memory and GC settings can be customized

```
  javaOptions:
    maxGCPauseMillis: 100
    parallelGCThreads : 3
    numberGCLogFiles: 10
    minMemory: 512m
    maxMemory: 2048m
    gcLogOptions: ""
```

### OpenDaylight Features

In values.yaml, one can customize features to be included during instance startup.  By default, only restconf is included.

```
config:
  odl_basedir: /opt/opendaylight
  #features: odl-restconf,odl-restconf-all,odl-bgpcep-pcep,odl-bgpcep-bgp,odl-bgpcep-bgp-config-example,odl-bgpcep-bmp,odl-bgpcep-bmp-config-example,odl-jolokiaa,odl-daexim-all
  features: odl-restconf,odl-restconf-all
```

### Container Image Version

The pull policy can be customized in values.yaml.

```
image:
  repository: nexus3.opendaylight.org:10001/opendaylight/opendaylight
  pullPolicy: IfNotPresent
```

The container image version is located in Chart.yaml
```
appVersion: "14.2.0"
```
so the combined image from above two files will be:
`nexus3.opendaylight.org:10001/opendaylight:14.2.0`

### Persistent Volume

By default the OpenDaylight Pod uses ephemeral volume.
The data stored at /data will lost after container restarts.

To support data persistence, it requires kubernetes persistent storageClass.  Depend on your environment, there are many implementation of storage plugin.  Following is example of define a storageClass on OpenEBS storage plugin.

create storageClass vg01-lvmpv for OpenEBS on volume group vg01
```
kubectl apply -f - <<EOD
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: vg01-lvmpv
allowVolumeExpansion: true
parameters:
   volgroup: "vg01"
provisioner: local.csi.openebs.io
EOD
```

Once storageClass is defined, adjust the values.yaml
- enabled = true
- size = `adjustable based on number of devices supported`
- storageClass = `defined storageClass`
```
persistence:
  enabled: false
  accessMode: ReadWriteOnce
  size: 5Gi
  mountPath: /data
  storageClass: vg01-lvmpv
  volName: odlvol
```

### Dry run
the generated definition can be inspected before actual deployment using --dry-run flag
```
helm install sdnc opendaylight --dry-run 
```

## Deploy

Following will deploy a release called sdnc to default namespace with persistent volume
```
helm install sdnc opendaylight --set persistence.enabled=true
```

if need to deploy on different namespace (sdntest)
```
helm install sdnc opendaylight --set persistence.enabled=true --create-namespace -n sdntest
```


the output:
```
NAME: sdnc
LAST DEPLOYED: Thu Oct 28 12:58:19 2021
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
1. Get the application URL by running these commands:
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=opendaylight,app.kubernetes.io/instance=sdnc" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
```

List deployed charts
```
helm list

NAME	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART             	APP VERSION
sdnc	default  	1       	2021-10-28 12:58:19.548011 -0400 EDT	deployed	opendaylight-0.1.0	14.2.0
```

Inspect Pods, by default only one instance of OpenDaylight Pods
```
kubectl get po

NAME                  READY   STATUS    RESTARTS   AGE
sdnc-opendaylight-0   1/1     Running   0          52s


kubectl get pvc

NAME                         STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
odlvol-sdnc-opendaylight-0   Bound    pvc-5d7ece71-088e-4dd6-9fda-67a928a51495   5Gi        RWO            vg01-lvmpv     77s
```

scale out to 3 standalone opendaylight instance
```
kubectl edit statefulset sdnc-opendaylight
```

update replica from 1 to 3
```
spec:
  podManagementPolicy: OrderedReady
  replicas: 1
```

```
 kubectl get po
NAME                  READY   STATUS    RESTARTS   AGE
sdnc-opendaylight-0   1/1     Running   0          6m37s
sdnc-opendaylight-1   1/1     Running   0          3m2s
sdnc-opendaylight-2   1/1     Running   0          2m20s
```

uninstall sdnc release
```
helm uninstall sdnc

release "sdnc" uninstalled
```

the persistent volumes still preserved and can be reuse for next deployment
```
kubectl get pvc

NAME                         STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
odlvol-sdnc-opendaylight-0   Bound    pvc-5d7ece71-088e-4dd6-9fda-67a928a51495   5Gi        RWO            vg01-lvmpv     10m
odlvol-sdnc-opendaylight-1   Bound    pvc-df825859-5970-453b-90df-22eb754a15f8   5Gi        RWO            vg01-lvmpv     6m47s
odlvol-sdnc-opendaylight-2   Bound    pvc-e074f280-4393-4b96-b34d-5d6ab22bdf77   5Gi        RWO            vg01-lvmpv     6m5s
```

### Access RESTCONF Swagger
base on the notes output from heml install, set up port forwarding to first instance
```
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=opendaylight,app.kubernetes.io/instance=sdnc" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace default $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace default port-forward $POD_NAME 8080:$CONTAINER_PORT
```

from browser, go to `http://127.0.0.1:8080/apidoc/explorer/index.html` then login with `admin/admin` 