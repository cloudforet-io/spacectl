import click
from spaceone.core.utils import load_yaml_from_file
from lib.output import print_data
from conf.global_conf import DEFAULT_ENVIRONMENT, DEFAULT_ENDPOINTS
from conf.my_conf import set_endpoint, remove_endpoint, get_endpoint, list_endpoints

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.group()
def endpoint():
    """Manage API endpoints"""
    pass


@endpoint.command()
@click.option('-e', '--environment', default=DEFAULT_ENVIRONMENT, help='Environment', show_default=True)
@click.option('-i', '--import', 'import_file_path', type=click.Path(exists=True), help='Import endpoints file (YAML)')
def init(environment, import_file_path):
    """Initialize API endpoints"""
    if import_file_path:
        endpoints = load_yaml_from_file(import_file_path)
        _check_import_file_format(endpoints)
        set_endpoint(environment, endpoints)

    else:
        set_endpoint(environment, DEFAULT_ENDPOINTS)


@endpoint.command()
@click.argument('environment')
@click.argument('service')
@click.argument('endpoint')
def add(environment, service, endpoint):
    """Add a API endpoint"""
    try:
        endpoints = get_endpoint(environment)
    except Exception:
        endpoints = {}

    if service in endpoints:
        raise ValueError(f"'{service}' service already exists in '{environment}' environment.")
    endpoints[service] = endpoint
    set_endpoint(environment, endpoints)


@endpoint.command()
@click.argument('environment')
@click.option('-s', '--service', help='Remove a specific service')
@click.option('-a', '--all', 'all_services', is_flag=True, help='Remove all services')
def remove(environment, service, all_services):
    """Remove a API endpoints"""

    if all_services:
        remove_endpoint(environment)
    else:
        if service:
            remove_endpoint(environment, service)
        else:
            raise Exception("'--service' or '--all' option is required.")


@endpoint.command()
@click.option('-e', '--environment', help='Environment (ex: production, ..)')
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(environment, output):
    """Display API endpoints"""
    endpoints = list_endpoints(environment)
    print_data(endpoints, output, headers=['Environment', 'Service', 'Endpoint'])


def _check_import_file_format(data):
    if not isinstance(data, dict):
        raise ValueError('Import file format is invalid. (format={service: endpoint, service: endpoint, ...})')

    for key, value in data.items():
        if not isinstance(value, str):
            raise ValueError('Import file format is invalid. (format={service: endpoint, service: endpoint, ...})')
