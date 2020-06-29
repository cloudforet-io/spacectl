import click
from spaceone.core.utils import load_yaml_from_file
from spacectl.lib.output import print_data
from spacectl.conf.global_conf import RESOURCE_ALIAS, DEFAULT_PARSER
from spacectl.conf.my_conf import set_template, remove_template, get_template

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.group()
def template():
    """Manage resource templates"""
    pass


@template.command()
@click.argument('resource')
@click.option('-f', '--file', 'file_path', type=click.Path(exists=True), help='Import template file (YAML)')
def set(resource, file_path):
    """Set resource template"""
    service, resource = _get_service_and_resource(resource)

    if file_path:
        template = load_yaml_from_file(file_path)
        set_template(service, resource, template)

    else:
        raise Exception("'--file' option is required.")


@template.command()
@click.argument('resource')
def remove(resource):
    """Remove resource template"""
    service, resource = _get_service_and_resource(resource)
    remove_template(service, resource)


@template.command()
@click.argument('resource')
def show(resource):
    """Display resource template"""
    service, resource = _get_service_and_resource(resource)
    template = get_template(service, resource)

    if template:
        template['parser'] = template.get('parser', DEFAULT_PARSER)
        print_data(template, 'yaml')
    else:
        click.echo(f'{service}.{resource} template is undefined.')
        click.echo()


def _get_service_and_resource(resource):
    if resource in RESOURCE_ALIAS:
        return RESOURCE_ALIAS[resource]
    else:
        resource_split = resource.split('.')
        if len(resource_split) != 2:
            raise ValueError(f'Resource format is invalid. (resource = <service>.<resource>)')
        return resource_split[0], resource_split[1]