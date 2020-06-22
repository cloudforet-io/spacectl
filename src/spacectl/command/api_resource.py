import click

from spaceone.core import pygrpc
from spaceone.core.utils import parse_endpoint

from lib.output import print_data
from conf.global_conf import RESOURCE_ALIAS, DEFAULT_ENVIRONMENT
from conf.my_conf import get_config, get_endpoint

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.command()
@click.option('-e', '--environment', default=lambda: get_config('environment', DEFAULT_ENVIRONMENT),
              help='Environment', show_default=True)
def api_resources(environment):
    """Print the supported API resources"""
    endpoints = get_endpoint(environment)
    resources = _get_resources_from_client(endpoints)
    resources = _get_resource_alias(resources)
    _print_api_resources(resources)


def _get_resources_from_client(endpoints, api_version='v1'):
    resources = {}
    for service, endpoint in endpoints.items():
        try:
            e = parse_endpoint(endpoint)
            client = pygrpc.client(endpoint=f'{e.get("hostname")}:{e.get("port")}', version=api_version)

            resources[service] = {}
            for api_resource, verb in client.api_resources.items():
                resources[service][api_resource] = {
                    'alias': [],
                    'verb': verb
                }

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
