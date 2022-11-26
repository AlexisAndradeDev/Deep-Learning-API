import os
# define a system variable called DJANGO_ENV and set it to the
# environment you want
env_name = os.environ.get('DJANGO_ENV', None)

ENVS = ['deployment', 'dev', 'unit_test', 'integration_test']

assert env_name in ENVS, f'Environment \'{env_name}\' is not valid. Define a system variable DJANGO_ENV and set it to: {ENVS}'

if env_name == 'deployment':
    from config.deployment import *
elif env_name == 'dev':
    from config.dev import *
elif env_name == 'unit_test':
    from config.unit_test import *
elif env_name == 'integration_test':
    from config.integration_test import *
