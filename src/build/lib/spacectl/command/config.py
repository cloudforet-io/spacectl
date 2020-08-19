import click
from spacectl.lib.output import print_data
from spacectl.conf.global_conf import DEFAULT_ENVIRONMENT
from spacectl.conf.my_conf import *

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.group()
def config():
    """Modify spaceconfig files"""
    pass


@config.command()
@click.option('-e', '--environment', prompt='Environment', help='Environment', default=DEFAULT_ENVIRONMENT)
@click.option('-f', '--import-file', type=click.Path(exists=True), help='YAML file only')
def init(environment, import_file):
    """Initialize spaceconfig"""
    set_environment(environment)

    if import_file:
        import_config(import_file, environment)
    else:
        set_config({}, environment)


@config.command()
@click.argument('key')
@click.argument('value')
def set(key, value):
    """Set specific spaceconfig"""
    data = get_config()
    data[key] = value
    set_config(data)


@config.command()
@click.argument('key')
def remove(key):
    """Remove specific spaceconfig"""
    data = get_config()

    if key in data:
        del data[key]

    set_config(data)


@config.command()
@click.option('-s', '--switch', help='Switch the environment')
@click.option('-r', '--remove', help='Remove the environment')
def environment(switch, remove):
    """Manage environments"""

    if switch:
        environments = list_environments()
        if switch not in environments:
            raise Exception(f"'{switch}' environment not found.")

        set_environment(switch)
        click.echo(f"Switched to '{switch}' environment.")
    elif remove:
        environments = list_environments()
        if remove not in environments:
            raise Exception(f"'{switch}' environment not found.")

        remove_environment(remove)
        click.echo(f"'{remove}' environment has been removed.")
    else:
        try:
            current_env = get_environment()
        except Exception:
            current_env = None

        environments = list_environments()
        if len(environments) == 0:
            raise Exception('spaceconfig is undefined. (Use "spacectl config init")')

        for env in environments:
            if current_env == env:
                click.echo(f'{env} (current)')
            else:
                click.echo(env)


@config.command()
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['json', 'yaml']), show_default=True)
def show(output):
    """Display a spaceconfig"""
    data = get_config()
    print_data(data, output)


@config.group()
def endpoint():
    """Manage API endpoints"""
    pass


@endpoint.command()
@click.argument('service')
@click.argument('endpoint')
def add(service, endpoint):
    """Add a API endpoint"""
    try:
        endpoints = get_endpoint()
    except Exception:
        endpoints = {}

    if service in endpoints:
        raise ValueError(f"'{service}' service already exists.")
    endpoints[service] = endpoint
    set_endpoint(endpoints)
    click.echo(f"'{service}: {endpoint}' endpoint has been added.")


@endpoint.command()
@click.argument('service')
def remove(service):
    """Remove a API endpoint"""
    remove_endpoint(service)
    click.echo(f"'{service}' endpoint has been removed.")


@endpoint.command()
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
def show(output):
    """Display API endpoints"""
    endpoints = list_endpoints()
    print_data(endpoints, output, headers=['Service', 'Endpoint'])
