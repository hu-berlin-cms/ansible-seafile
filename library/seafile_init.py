#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Enno Gröper <enno.groeper@cms.hu-berlin.de>

DOCUMENTATION = '''
Init seafile cluster
'''

EXAMPLES = '''
'''

import sys
import os
import imp

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(default='/data/haiwen'),
            subdir=dict(default=None, required=True),
            seafile_mysql_user=dict(default='seafile'),
            seafile_mysql_password=dict(default=None, required=True),
            ccnet_db_name=dict(default='ccnet-db'),
            seafile_db_name=dict(default='seafile-db'),
            seahub_db_name=dict(default='seahub-db'),
            mysql_host=dict(default='127.0.0.1'),
            mysql_port=dict(default=3306,type='int'),
            server_name = dict(default='seafile'),
            ip_or_domain = dict(default='seafile.localdomain'),
            ccnet_port = dict(default=10001,type='int'),
            seafile_port = dict(default=12001,type='int'),
            seafile_fileserver_port = dict(default=8082,type='int'),
            central_conf_dir=dict(default=True, choices=BOOLEANS),
            #initialize=dict(default=False, choices=BOOLEANS),
            #something=dict(aliases=['whatever'])
        ),
        supports_check_mode=False
    )

    # touch __init__.py for importing
    #sys.path.insert(0, os.path.join(module.params['path'], module.params['subdir']))
    try:
        #import setup-seafile-mysql.py
        seaset = imp.load_source('seaset', os.path.join(module.params['path'], module.params['subdir'], 'setup-seafile-mysql.py'))

    except Exception as e:
        module.fail_json(msg="Could not import setup-seafile-mysql.py: %s" % e)

    # FIXME guard program exits (sys.exit due to error() call)
    # lets use the imported variables
    env_mgr = seaset.env_mgr
    ccnet_config = seaset.ccnet_config
    seafile_config = seaset.seafile_config
    seafdav_config = seaset.seafdav_config
    seahub_config = seaset.seahub_config
    user_manuals_handler = seaset.user_manuals_handler
    pro_config = seaset.pro_config
    seaset.db_config = seaset.ExistingDBConfigurator()
    db_config = seaset.db_config

    # init
    env_mgr.check_pre_condiction()

    #env_mgr = seaset.EnvManager()
    #env_mgr.check_pre_condiction()
    #ccnet_config = seaset.CcnetConfigurator()
    #seafile_config = seaset.SeafileConfigurator()
    #seafdav_config = seaset.SeafDavConfigurator()
    #seahub_config = seaset.SeahubConfigurator()
    #user_manuals_handler = seaset.UserManualHandler()
    #pro_config = seaset.ProfessionalConfigurator()
    #db_config = seaset.ExistingDBConfigurator()
    ## adjust setup-seafile-mysql global db_config
    #seaset.db_config = db_config

    # set parameters
    db_config.seafile_mysql_user = module.params['seafile_mysql_user']
    db_config.seafile_mysql_password = module.params['seafile_mysql_password']
    db_config.ccnet_db_name = module.params['ccnet_db_name']
    db_config.seafile_db_name = module.params['seafile_db_name']
    db_config.seahub_db_name = module.params['seahub_db_name']
    db_config.use_existing_db = True
    db_config.mysql_host = module.params['mysql_host']
    db_config.mysql_port = module.params['mysql_port']
    ccnet_config.ccnet_dir = os.path.join(env_mgr.top_dir, 'ccnet')
    ccnet_config.server_name = module.params['server_name']
    ccnet_config.ip_or_domain = module.params['ip_or_domain']
    ccnet_config.port = module.params['ccnet_port']
    seafile_config.seafile_dir = os.path.join(env_mgr.top_dir, 'seafile-data')
    seafile_config.port = module.params['seafile_port']
    seafile_config.fileserver_port = module.params['seafile_fileserver_port']
    if module.params['central_conf_dir'] in BOOLEANS_TRUE:
        seahub_config.seahub_settings_py = os.path.join(env_mgr.top_dir, 'conf', 'seahub_settings.py')
    else:
        seahub_config.seahub_settings_py = os.path.join(env_mgr.top_dir, 'seahub_settings.py')
    #seahub_config.admin_email = 'test@blubb'
    #seahub_config.admin_password = ''

    # Part 2: generate configuration
    ##db_config.generate()
    ccnet_config.generate()
    seafile_config.generate()
    seafdav_config.generate()
    seahub_config.generate()
    # FIXME python detection, for now we use default
    if not 'PYTHON' in os.environ:
        os.environ['PYTHON'] = "/usr/bin/python"
    pro_config.generate()
    seahub_config.do_syncdb()
    seahub_config.prepare_avatar_dir()
    ## db_config.create_seahub_admin()
    user_manuals_handler.copy_user_manuals()
    seaset.create_seafile_server_symlink()
    seaset.set_file_perm()

    module.exit_json(changed=True)


# import module snippets
from ansible.module_utils.basic import *  # noqa
#from ansible.module_utils.known_hosts import *

if __name__ == '__main__':
    main()
