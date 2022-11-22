#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def validate_environment(ENVS, env, command):
    assert env in ENVS, f'Environment \'{env}\' is not valid. Define a system variable DJANGO_ENV and set it to: {ENVS}'
    # test env must be used for test command
    if command == "test" and env != "test":
        raise AssertionError(f'Environment \'{env}\' is not valid for \'{command}\' command. Switch to test environment.')

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

    try:
        from dl_api.settings import ENVS
    except Exception as e:
        raise ImportError(
            "Could not import ENVS from settings module. "
            "Make sure you follow the 'settings' and 'config' structure used "
            f"in the original repository. Exception message: {e}"
        )

    # check if environment is valid
    user_env = os.environ.get('DJANGO_ENV', None)
    command = sys.argv[1]
    validate_environment(ENVS, user_env, command)

    print(f'Environment: {user_env}')

    # execute command
    if command == 'migrate':
        # migrate all envs
        from dl_api.settings import ENVS
        for env in ENVS:
            os.environ.setdefault('DJANGO_ENV', env)
            execute_from_command_line(sys.argv)
            print(f'Environment \'{env}\' migrated.')
        os.environ.setdefault('DJANGO_ENV', user_env)

    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
