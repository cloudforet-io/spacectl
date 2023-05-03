import os
from spaceone.core import utils
from spacectl.conf.global_conf import *

__all__ = ['set_environment', 'get_environment', 'remove_environment', 'list_environments',
           'import_config', 'set_config', 'get_config', 'set_endpoint', 'get_endpoint',
           'remove_endpoint', 'list_endpoints', 'set_template', 'get_template', 'remove_template']


def set_environment(environment):
    utils.create_dir(CONFIG_DIR)
    utils.create_dir(ENVIRONMENT_DIR)
    utils.save_yaml_to_file({'environment': environment}, ENVIRONMENT_CONF_PATH)


def get_environment():
    try:
        data = utils.load_yaml_from_file(ENVIRONMENT_CONF_PATH)
        environment = data.get('environment')

        if not environment:
            raise Exception(
                'The environment is not set. Switch the environment. (Use "spacectl config environment --help")')

        return environment

    except Exception as e:
        default_env = os.environ.get('SPACECTL_DEFAULT_ENVIRONMENT')
        environments = list_environments()

        if default_env in environments:
            set_environment(default_env)
            return default_env

        elif len(environments) > 0:
            raise Exception(
                'The environment is not set. Switch the environment. (Use "spacectl config environment --help")')
        else:
            raise Exception('spaceconfig is undefined. (Use "spacectl config init")')


def remove_environment(environment):
    try:
        environment_path = os.path.join(ENVIRONMENT_DIR, f'{environment}.yml')
        if os.path.exists(environment_path):
            os.remove(environment_path)
    except Exception as e:
        raise Exception(f'Environment deletion error: {e}')

    environments = list_environments()
    if len(environments) > 0:
        utils.save_yaml_to_file({'environment': environments[0]}, ENVIRONMENT_CONF_PATH)
    else:
        os.remove(ENVIRONMENT_CONF_PATH)


def list_environments():
    environments = []
    try:
        for f in os.listdir(ENVIRONMENT_DIR):
            if os.path.isfile(os.path.join(ENVIRONMENT_DIR, f)) and f.find('.yml') > 1:
                environments.append(f.rsplit('.', 1)[0])
    except Exception:
        raise Exception('spaceconfig is undefined. (Use "spacectl config init")')

    return environments


def import_config(import_file_path, environment=None):
    if environment is None:
        environment = get_environment()

    try:
        environment_path = os.path.join(ENVIRONMENT_DIR, f'{environment}.yml')
        data = utils.load_yaml_from_file(import_file_path)
        utils.save_yaml_to_file(data, environment_path)
    except Exception:
        raise Exception(f'Import file format is invalid. (file = {import_file_path})')


def set_config(new_data, environment=None):
    if environment is None:
        environment = get_environment()

    try:
        environment_path = os.path.join(ENVIRONMENT_DIR, f'{environment}.yml')
        utils.save_yaml_to_file(new_data, environment_path)
    except Exception:
        raise Exception('spaceconfig is undefined. (Use "spacectl config init")')


def get_config(key=None, default=None, environment=None):
    if environment is None:
        environment = get_environment()

    try:
        environment_path = os.path.join(ENVIRONMENT_DIR, f'{environment}.yml')
        data = utils.load_yaml_from_file(environment_path)
    except Exception:
        raise Exception('spaceconfig is undefined. (Use "spacectl config init")')

    if key:
        return data.get(key, default)
    else:
        return data


def set_endpoint(endpoints, environment=None):
    data = get_config(environment)
    data['endpoints'] = endpoints

    set_config(data, environment)


def get_endpoint(service=None, environment=None):
    endpoints = get_config('endpoints', {}, environment)

    if service:
        return endpoints.get(service)
    else:
        return endpoints


def remove_endpoint(service, environment=None):
    data = get_config(environment)
    endpoints = data.get('endpoints', {})

    if service in endpoints:
        del endpoints[service]

    data['endpoints'] = endpoints

    set_config(data, environment)


def list_endpoints(environment=None):
    endpoints = get_config('endpoints', {}, environment)
    result = []

    for service, endpoint in endpoints.items():
        result.append((service, endpoint))

    return result


def set_template(service, resource, data):
    utils.create_dir(TEMPLATE_DIR)
    my_template_path = os.path.join(TEMPLATE_DIR, f'{service}.{resource}.yml')
    utils.save_yaml_to_file(data, my_template_path)


def remove_template(service, resource):
    my_template_path = os.path.join(TEMPLATE_DIR, f'{service}.{resource}.yml')
    if os.path.exists(my_template_path):
        os.remove(my_template_path)


def get_template(service, resource):
    return _get_my_template(service, resource) or _get_default_template(service, resource)


def _get_my_template(service, resource):
    try:
        my_template_path = os.path.join(TEMPLATE_DIR, f'{service}.{resource}.yml')
        data = utils.load_yaml_from_file(my_template_path)
        data['type'] = 'custom'
        return data
    except Exception:
        return None


def _get_default_template(service, resource):
    try:
        default_template_path = os.path.join(DEFAULT_TEMPLATE_DIR, f'{service}.{resource}.yml')
        data = utils.load_yaml_from_file(default_template_path)
        data['type'] = 'default'
        return data
    except Exception:
        return None
