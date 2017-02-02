#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2015, Enno Gröper <enno.groeper@cms.hu-berlin.de>

DOCUMENTATION = '''
Create seafile admin, if none exists
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
            name=dict(default=None, required=True),
            password=dict(default=None, required=True),
        ),
        supports_check_mode=False
    )

    # for importing ccnet module
    sys.path.append(
        os.path.join(
            module.params['path'],
            module.params['subdir'],
            'seafile/lib64/python2.6/site-packages'))
    # 'CCNET_CONF_DIR'
    if not 'CCNET_CONF_DIR' in os.environ:
        os.environ['CCNET_CONF_DIR'] = os.path.join(module.params['path'], 'ccnet')
    # 'SEAFILE_CENTRAL_CONF_DIR'
    if not 'SEAFILE_CENTRAL_CONF_DIR' in os.environ:
        os.environ['SEAFILE_CENTRAL_CONF_DIR'] = os.path.join(module.params['path'], 'conf')

    try:
        #import setup-seafile-mysql.py
        seaadmin = imp.load_source('seaadmin', os.path.join(module.params['path'], module.params['subdir'], 'check_init_admin.py'))

    except Exception as e:
        module.fail_json(msg="Could not import check_init_admin.py: %s" % e)

    try:
        if seaadmin.need_create_admin():
            seaadmin.create_admin(
                module.params['name'],
                module.params['password'])
        else:
            module.exit_json(changed=false)
    except Exception as e:
        module.fail_json(msg="Could not create admin: %s" % e)

    module.exit_json(changed=True)


# import module snippets
from ansible.module_utils.basic import *  # noqa
#from ansible.module_utils.known_hosts import *

if __name__ == '__main__':
    main()
