import click
from spacectl.lib.output import print_data
from spacectl.conf.global_conf import DEFAULT_ENVIRONMENT
from spacectl.conf.my_conf import set_config, get_config

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.group()
def config():
    """Modify spaceconfig files"""
    pass


@config.command()
@click.option('-d', '--domain-id', prompt='Domain ID', help='Domain ID')
@click.option('-k', '--api-key', prompt='API Key', help='API Key')
@click.option('-e', '--environment', prompt='Environment', default=DEFAULT_ENVIRONMENT, help='Environment')
def init(domain_id, api_key, environment):
    """Initialize spaceconfig"""
    data = {
        'domain_id': domain_id,
        'api_key': api_key,
        'environment': environment
    }
    set_config(data)


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
def environment(switch):
    """Display a spaceconfig"""

    if switch:
        data = get_config()
        data['environment'] = switch
        set_config(data)
        click.echo(switch)
    else:
        environment = get_config('environment')
        click.echo(environment)


@config.command()
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['json', 'yaml']), show_default=True)
def show(output):
    """Display a spaceconfig"""
    data = get_config()
    print_data(data, output)
