#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dl_api.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # check if environment is valid
    try:
        from dl_api.settings import ENVS
    except:
        raise ImportError(
            "Could not import ENVS from settings module. "
            "Make sure you follow the 'settings' and 'config' structure used "
            "in the original repository."
        )

    env_name = os.environ.get('DJANGO_ENV', None)
    assert env_name in ENVS, f'Environment \'{env_name}\' is not valid. Define a system variable DJANGO_ENV and set it to: {ENVS}'

    print(f'Environment: {env_name}')

    # execute command
    if sys.argv[1] == 'migrate':
        # migrate all envs
        from dl_api.settings import ENVS
        for env in ENVS:
            os.environ.setdefault('DJANGO_ENV', env)
            execute_from_command_line(sys.argv)
            print(f'Environment \'{env}\' migrated.')
        os.environ.setdefault('DJANGO_ENV', env_name)

    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
