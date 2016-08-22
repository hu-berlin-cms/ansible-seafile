# Introduction

Ansible playbook to deploy seafile-pro cluster using HAProxy as loadbalancer, nginx or Apache as webservers, mariadb (single-node).
Primarily for use with ceph as storage backend, but also supports s3.

Ansible >=1.7 is needed. Tested with Ansible 1.9.

This playbook tries to keep in sync with the official manuals and therefore uses a "golden image", that is used
as clone source for the other instances.

It is tested against Seafile-Pro 5.1 deployed on Ubuntu 14.04.

This is work in progress. If you have ideas or find bugs, please file an issue.
We are planning to make this pretty flexible and modular, to ease adjusting it to your needs.

Some possibly interesting features:
* SSL-decryption at loadbalancer (haproxy); enables load distribution based on traffic/uri (Sync, Web, WebDAV)
* deploys own mariadb server or can use external server
* supports nginx and Apache (both with SSL)
* Shibboleth support using Apache as webserver
* Support running seafile as arbitrary user (*experimental*)
* Support for ceph and s3 as storage backends
* HA loadbalancer (Debian 8 or Ubuntu 16.04 needed on loadbalancer nodes)

# Prerequisites

## General 

Files needed in files/ directory (see the README there):

```
ceph.conf  # for ceph only
client.seafile  # for ceph only
seafile-cert.pem  # server certificate
seafile-chain.pem  # intermediate certificates
seafile-key.pem
seafile-license.txt
seafile-pro-server_5.0.1_x86-64.tar.gz  # pro installer archive
```

If you are using Shibboleth, put your config in ```files/shibboleth```. They will be copied to /etc/shibboleth on the nodes.

Adjust parameters (especially seafile_version):

```
groups_vars/all
```

Set passwords in separate files. You may use the templates:

```
cd vars
cp admin.yml.templ admin.yml
cp dbconfig.yml.templ dbconfig.yml
## edit the files
```

## Ceph

We assume you already have a ceph install.

### Create Ceph pools for Seafile

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

### Create Ceph user for Seafile (if Ceph is not used solely for seafile)

```
ceph auth get-or-create client.seafile mon 'allow r' osd 'allow rwx pool=seafile-blocks, allow rwx pool=seafile-commits, allow rwx pool=seafile-fs' -o client.seafile
```

# Prepare first run (for using Ansible pipelining and sudo, *disables requiretty!*)
```
./prepares-nodes.sh
```

# First run (initial install)

```
ansible-playbook -i hosts -e force_install=true site.yaml
```

# Further runs (config changes...)
```
ansible-playbook -i hosts site.yaml
```

# Upgrades

See [Upgrades](UPGRADE.md).

# Known issues

See [Known Issues](KnownIssues.md).

