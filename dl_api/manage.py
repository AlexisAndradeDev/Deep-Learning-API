#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import shutil
import os
import sys
import copy
import subprocess

COMMAND = 1
ENVS = ['deployment', 'dev', 'integration_test', 'unit_test']

def create_private_storage(PRIVATE_STORAGE_ROOT):
    os.mkdir(PRIVATE_STORAGE_ROOT)
    os.mkdir(PRIVATE_STORAGE_ROOT / 'datasets')
    os.mkdir(PRIVATE_STORAGE_ROOT / 'models')

def delete_private_storage(PRIVATE_STORAGE_ROOT):
    shutil.rmtree(PRIVATE_STORAGE_ROOT)

def migrate_env_database(env):
    """
    Migrates the database of an environment.

    Args:
        env (str): Name of the environment.
    """    
    # copy current environment variables and change env name
    env_variables = dict(os.environ)
    env_variables['DJANGO_ENV'] = env

    # migrate env database
    process = subprocess.Popen(
        f'{sys.executable} manage.py migrate',
        env=env_variables,
    )
    process.communicate()
    print(f'Environment \'{env}\' migrated.')

def delete_database(database_path):
    os.remove(database_path)

def setup_server(env, private_storage_root):
    create_private_storage(private_storage_root)
    migrate_env_database(env)

def validate_environment(system_env, command_env, command):
    assert system_env in ENVS, f'Environment \'{system_env}\' is not valid. Define a system variable DJANGO_ENV and set it to: {ENVS}'

    if command_env and system_env not in ['dev'] and command_env != system_env:
        raise AssertionError(f'Environment \'{system_env}\' can\'t execute other environments.')

    if command == 'test' and system_env != 'unit_test':
        raise AssertionError(f'Environment \'{system_env}\' is not valid for \'{command}\' command. Switch to unit_test environment.')

    if command == 'integration-test-server' and system_env != 'integration_test':
        raise AssertionError(f'Environment \'{system_env}\' is not valid for \'{command}\' command. Switch to integration_test environment.')

def get_env_specified_in_command_line(argv):
    """
    Returns the environment name specified by the user in the command line.

    Args:
        argv (list of str): Command line arguments.

    Raises:
        Exception: If the entered environment is not in ENVS.

    Returns:
        command_env: Name of the environment.
        argument_index: Index in the command line args of the argument 
            that specifies the name of the environment.
    """    
    command_env = None
    argument_index = None
    if '--env' in argv:
        try:
            argument_index = argv.index('--env')
            command_env = argv[argument_index+1]
        except Exception as e:
            raise Exception(f'Argument \'--env\' must have a value: {ENVS}')
        assert command_env in ENVS, f'Environment \'{command_env}\' is not valid. Set \'--env\' to: {ENVS}'
    return command_env, argument_index

def delete_personalized_argument(argv, argument_index):
    """
    Deletes the personalized argument from the command line arguments
    list.

    Args:
        argv (list of str): Command line arguments.
        argument_index (int): Index of the argument.
    """    
    # delete arg
    argv.pop(argument_index)
    # delete arg value
    argv.pop(argument_index)

def get_personalized_arguments(argv):
    """
    Returns the personalized arguments (those not created by Django).
    Deletes each personalized argument from the command line arguments
    after getting it.

    Args:
        argv (list of str): Command line arguments.

    Returns:
        command_env: Name of the environment.
    """
    command_env, argument_index = get_env_specified_in_command_line(argv)
    if argument_index != None:
        delete_personalized_argument(argv, argument_index)

    return command_env

def main():
    """Run administrative tasks."""
    argv = copy.copy(sys.argv)

    system_env = os.environ.get('DJANGO_ENV', None)
    assert system_env in ENVS, f'\'DJANGO_ENV\' system variable must have a value: {ENVS}'

    command_env = get_personalized_arguments(argv)

    command = argv[1]

    validate_environment(system_env, command_env, command)
    
    if command_env:
        active_env = command_env
    else:
        active_env = system_env

    os.environ['DJANGO_SETTINGS_MODULE'] = f'config.{active_env}'

    if active_env == 'dev':
        import config.dev as settings
    elif active_env == 'deployment':
        import config.deployment as settings
    elif active_env == 'integration_test':
        import config.integration_test as settings
    elif active_env == 'unit_test':
        import config.unit_test as settings
    else:
        raise AssertionError(
            f"Environment {active_env} settings could not be imported. "
            "Make sure you follow the 'settings' and 'config' structure used "
            f"in the original repository."
        )

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    print(f'Active environment: {active_env}')
    # execute command
    if active_env == 'dev':
        if command == 'migrate-all':
            # migrate all envs
            for env in ENVS:
                migrate_env_database(env)
        else:
            execute_from_command_line(argv)

    elif active_env == 'deployment':
        if command in ['runserver', 'migrate']:
            execute_from_command_line(argv)
        else:
            raise Exception(f'Command \'{command}\' can\'t be run in \'{active_env}\' environment.')

    elif active_env == 'integration_test':
        if command == 'runserver':
            if os.environ.get('RUN_MAIN') != 'true':
                # when the runserver command is executed, the integration test 
                # environment is setup; then, the runserver command is run again; 
                # finally, some files and dirs are deleted
                try:
                    setup_server(active_env, settings.PRIVATE_STORAGE_ROOT)

                    # run server
                    execute_from_command_line(argv)
                finally:
                    # exit server
                    delete_private_storage(settings.PRIVATE_STORAGE_ROOT)
                    database_path = settings.DATABASES.get('default').get('NAME')
                    delete_database(database_path)
            else:
                # Django runs the runserver command twice, in the second run (the
                # one that executes 'runserver') RUN_MAIN system variable is set to 
                # 'true' by Django.
                execute_from_command_line(argv)

        elif command in ['migrate']:
            execute_from_command_line(argv)

        else:
            raise Exception(f'Command \'{command}\' can\'t be run in \'{active_env}\' environment.')

    elif active_env == 'unit_test':
        if command == 'test':
            create_private_storage(settings.PRIVATE_STORAGE_ROOT)

            try:
                execute_from_command_line(argv)
            finally:
                delete_private_storage(settings.PRIVATE_STORAGE_ROOT)
        elif command in ['migrate']:
            execute_from_command_line(argv)
        else:
            raise Exception(f'Command \'{command}\' can\'t be run in \'{active_env}\' environment.')


if __name__ == '__main__':
    main()
