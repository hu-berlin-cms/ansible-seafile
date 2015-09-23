# Changing Webservers

Due to the nature of Ansible it installs everything, that is needed, but it never removes anything (installed packages, etc.).
So if you are switching between nginx and Apache as webservers, you should remove the old webserver manually.

Example (after switching from nginx to Apache):
```
ansible -s -i hosts -m apt -a "name=nginx purge=yes state=absent" nodes
```

If you fail to do so, your os could start the wrong/old webserver with it's old configuration.
