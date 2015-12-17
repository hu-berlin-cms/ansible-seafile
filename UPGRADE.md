# Upgrading ansible-seafile

Simply run
```
git pull
```

master should always contain the most recent and working version.

# Upgrading Seafile

An upgrade has to be done on the master node and then needs to be deployed to the clones.

To assist you with upgrading Seafile we provide two playbooks:
* prepare-upgrade.yml
* finish-upgrade.yml

If you want to use them, upgrading consists of the following steps:
* copy new seafile installer archive to files dir
* update seafile_version variable to new version
* run prepare-upgrade.yml playbook **This STOPS running seafile instances!**
* manually run upgrade scripts on master node
* run finish-upgrade.yml playbook to finish the upgrade (site.yaml would work, too)

Example of an upgrade:
```
# check md5sum of installer archive
md5sum seafile-pro-server_5.0.1_x86-64.tar.gz
e498a4978e1e7f1c8755aa9d21712c91  seafile-pro-server_5.0.1_x86-64.tar.gz
cat seafile-pro-server_5.0.1_x86-64.tar.gz.md5.txt
e498a4978e1e7f1c8755aa9d21712c91

# copy installer to deploy node
scp seafile-pro-server_5.0.1_x86-64.tar.gz deploy-node:configstack/files

# connect to deploy node
ssh deploy-node

# update version string
sed -i 's/^seafile_version:.*/seafile_version: "5.0.1"/' group_vars/all

# prepare upgrade; This STOPS all running instances
ansible-playbook -i hosts prepare-upgrade.yml 

# actual upgrade
ssh master-node
# run upgrade scripts needed for current upgrade (major, minor?)
sudo /data/seafile/seafile-pro-server-5.0.1/upgrade/minor-upgrade.sh
exit

# finish upgrade
ansible-playbook -i hosts finish-upgrade.yml
```

If you don't want to use them, upgrading consists of the following steps:
* copy new seafile installer archive to files dir
* update seafile_version variable to new version (to support version specific changes)
* copy new seafile installer to master node
* extract new seafile installer on master node
* stop all running seafile instances
* manually run upgrade scripts on master node
* run site.yaml playbook to finish the upgrade

# Upgrading OS on nodes

To upgrade os packages on the nodes (not seafile itself!) run:
```
ansible -i hosts upgrade_os.yml
```

You can simulate this, if you want to see in advance, what would be done:
```
ansible -i hosts -e simulate=yes upgrade_os.yml
```
