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
* update seafile-install.tar.gz symlink
* run prepare-upgrade.yml playbook **This STOPS running seafile instances!**
* manually run upgrade scripts on master node
* run finish-upgrade.yml playbook to finish the upgrade

Example of an upgrade:
```
# check md5sum of installer archive
md5sum seafile-pro-server_4.3.3_x86-64.tar.gz
417bd9d618367cac328e17076eeb2a3e  seafile-pro-server_4.3.3_x86-64.tar.gz
cat seafile-pro-server_4.3.3_x86-64.tar.gz.md5.txt
417bd9d618367cac328e17076eeb2a3e

# copy installer to deploy node
scp seafile-pro-server_4.3.3_x86-64.tar.gz deploy-node:configstack/files

# connect to deploy node
ssh deploy-node

# update symlink
cd configstack/files/
rm seafile-install.tar.gz 
ln -s seafile-pro-server_4.3.3_x86-64.tar.gz seafile-install.tar.gz
cd ..

# prepare upgrade; This STOPS all running instances
ansible-playbook -i hosts prepare-upgrade.yml 

# actual upgrade
ssh master-node
# run upgrade scripts needed for current upgrade (major, minor?)
sudo /data/seafile/seafile-pro-server-4.3.3/upgrade/minor-upgrade.sh
exit

# finish upgrade
ansible-playbook -i hosts finish-upgrade.yml
```

# Upgrading OS on nodes

To upgrade os packages on the nodes (not seafile itself!) run:
```
ansible -i hosts upgrade_os.yml
```
