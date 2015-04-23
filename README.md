# Introduction

Ansible playbook to deploy seafile-pro cluster using nginx, mariadb (single-node) and ceph.

**TODO**

# Prerequisites

We assume you already have a ceph install.

## Create Ceph pools for Seafile

Create pools:

```
## on ceph master node
## create ceph pools
rados mkpool seafile-blocks
rados mkpool seafile-commits
rados mkpool seafile-fs
```

Adjust pool parameters:

```
## use better parameters: size 3, pg_num 1024, pgp_num 1024
for pool in seafile-blocks seafile-commits seafile-fs; do ceph osd pool set $pool size 3 ; ceph osd pool set $pool pg_num 1024; sleep 60; ceph osd pool set $pool pgp_num 1024; done
```
