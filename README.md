# Introduction

Ansible playbook to deploy seafile-pro cluster using nginx, mariadb (single-node) and ceph.

Ansible >=1.6 is needed (installing mariadb/mysql using Ansible 1.5.4 doesn't work). Tested with Ansible 1.9.

**TODO**

# Prerequisites

We assume you already have a ceph install.

Files needed in files/ directory (see the README there):

```
ceph.conf
client.seafile
seafile-chain.pem
seafile-key.pem
seafile-license.txt
seafile-install.tar.gz  # symlink to pro installer archive
```

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

## Create Ceph user for Seafile (if Ceph is not used solely for seafile)

```
ceph auth get-or-create client.seafile mon 'allow r' osd 'allow rwx pool=seafile-blocks, allow rwx pool=seafile-commits, allow rwx pool=seafile-fs' -o client.seafile
```


# First Run (initial install)

```
ansible-playbook -i hosts -e force_install=true site.yaml
```
