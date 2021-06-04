import click

from spaceone.core.error import ERROR_BASE
from spaceone.core import pygrpc
from spaceone.core.utils import parse_endpoint

from spacectl.lib.output import print_data
from spacectl.conf.global_conf import RESOURCE_ALIAS
from spacectl.conf.my_conf import get_config, get_endpoint

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.command()
def api_resources():
    """Print the supported API resources"""
    environment = get_config('environment')
    endpoints = get_endpoint(environment)
    resources = _get_resources_from_client(endpoints)
    resources = _get_resource_alias(resources)
    _print_api_resources(resources)


def _get_resources_from_client(endpoints, api_version='v1'):
    resources = {}
    for service, endpoint in endpoints.items():
        try:
            e = parse_endpoint(endpoint)
            protocol = e.get('scheme')

            if protocol not in ['grpc', 'grpc+ssl']:
                raise ValueError(f'Unsupported protocol. (supported_protocol=grpc|grpc+ssl, endpoint={endpoint})')

            if protocol == 'grpc+ssl':
                ssl_enabled = True
            else:
                ssl_enabled = False

            client = pygrpc.client(endpoint=f'{e.get("hostname")}:{e.get("port")}',
                                   version=api_version, ssl_enabled=ssl_enabled)

            resources[service] = {}
            for api_resource, verb in client.api_resources.items():
                resources[service][api_resource] = {
                    'alias': [],
                    'verb': verb
                }
        except ERROR_BASE as e:
            raise e
        except ValueError as e:
            raise e
        except Exception:
            raise ValueError(f'Endpoint is invalid. (endpoint={endpoint})')

    return resources


def _get_resource_alias(resources):
    for alias, resource_type in RESOURCE_ALIAS.items():
        service, resource = resource_type
        if service in resources:
            if resource in resources[service]:
                resources[service][resource]['alias'].append(alias)

    return resources


def _print_api_resources(resources):
    data = []
    for service, service_value in resources.items():
        for resource, resource_value in service_value.items():
            data.append((service, resource, ', '.join(resource_value['alias']), ', '.join(resource_value['verb'])))

    print_data(data, 'table', headers=['Service', 'Resource', 'Short Names', 'Verb'])
