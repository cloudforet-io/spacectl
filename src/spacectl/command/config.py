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
@click.option('-n', '--namespace', prompt='Namesapce', help='Namespace', default='default')
@click.option('-d', '--domain-id', prompt='Domain ID', help='Domain ID')
@click.option('-k', '--api-key', prompt='API Key', help='API Key')
@click.option('-e', '--environment', prompt='Environment', default=DEFAULT_ENVIRONMENT, help='Environment')
def init(namespace, domain_id, api_key, environment):
    """Initialize spaceconfig"""
    set_namespace(namespace)
    set_config({
        'domain_id': domain_id,
        'api_key': api_key,
        'environment': environment
    }, namespace=namespace)


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
@click.option('-s', '--switch', help='Switch the namespace')
@click.option('-r', '--remove', help='Remove the namespace')
def namespace(switch, remove):
    """Display a spaceconfig"""

    if switch:
        namespaces = list_namespaces()
        if switch not in namespaces:
            raise Exception(f"'{switch}' namespace not found.")

        set_namespace(switch)
        click.echo(switch)
    elif remove:
        namespaces = list_namespaces()
        if remove not in namespaces:
            raise Exception(f"'{remove}' namespace not found.")

        remove_namespace(remove)
    else:
        try:
            current_ns = get_namespace()
        except Exception:
            current_ns = None

        namespaces = list_namespaces()
        if len(namespaces) == 0:
            raise Exception('spaceconfig is undefined. (Use "spacectl config init")')

        for ns in namespaces:
            if current_ns == ns:
                click.echo(f'{ns} (current)')
            else:
                click.echo(ns)


@config.command()
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['json', 'yaml']), show_default=True)
def show(output):
    """Display a spaceconfig"""
    data = get_config()
    print_data(data, output)
