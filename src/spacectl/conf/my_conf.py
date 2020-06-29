import os
from spaceone.core import utils
from spacectl.conf.global_conf import *


def set_config(data):
    utils.create_dir(CONFIG_DIR)
    utils.save_yaml_to_file(data, CONFIG_PATH)


def get_config(key=None, default=None):
    try:
        data = utils.load_yaml_from_file(CONFIG_PATH)
    except Exception:
        raise Exception('spaceconfig is undefined. (Use "spacectl config init")')

    if key:
        return data.get(key, default)
    else:
        return data


def set_endpoint(environment, endpoints):
    utils.create_dir(CONFIG_DIR)
    try:
        data = utils.load_yaml_from_file(ENDPOINT_PATH)
    except Exception:
        data = {}

    data[environment] = endpoints

    utils.save_yaml_to_file(data, ENDPOINT_PATH)


def remove_endpoint(environment, service=None):
    utils.create_dir(CONFIG_DIR)
    try:
        data = utils.load_yaml_from_file(ENDPOINT_PATH)
    except Exception:
        data = {}

    if environment in data:
        if service:
            if service in data[environment]:
                del data[environment][service]
        else:
            del data[environment]

        utils.save_yaml_to_file(data, ENDPOINT_PATH)


def get_endpoint(environment, service=None):
    try:
        data = utils.load_yaml_from_file(ENDPOINT_PATH)
    except Exception:
        raise Exception('Endpoint is undefined. (Use "spacectl endpoint init")')

    if environment not in data:
        raise Exception(f'The endpoint of the \'{environment}\' environment is not set. (See "spacectl endpoint show")')

    if service:
        return data[environment].get(service)
    else:
        return data[environment]


def list_endpoints(environment=None):
    try:
        data = utils.load_yaml_from_file(ENDPOINT_PATH)
    except Exception:
        raise Exception('Endpoint is undefined. (Use "spacectl endpoint init")')

    result = []
    for env, endpoints in data.items():
        if environment and environment != env:
            continue

        for service, endpoint in endpoints.items():
            result.append((env, service, endpoint))

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
