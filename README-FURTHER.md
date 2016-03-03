# Available Options

In order to keep the [parameters](group_vars/all) manageable we defaulted a lot of the options.  
Take a look at the [defaults](roles/nodes/defaults/main.yml) to see what other options are available.

## Webserver

You can choose between nginx and apache. There is a config template located at /roles/nodes/templates for both.
The switch ssl_nodes gives you the option to decide if you want your notes to use ssl depending on your setup.

```
webserver: "apache"
ssl_nodes: no
```

## Authentification

For external authentification there is LDAP and Shibboleth.

```
use_shibboleth: yes
use_ldap: yes
```

# working with ansible

If you worked with ansible before this should be nothing new.
You can send a command to all your nodes or a subset.

e.g. checking one the status of a service 
```
ansible -i hosts -m command -a "service seafile-server status" nodes
```

same can be done with the modules
```
ansible -i hosts -m command -m ping nodes
```
