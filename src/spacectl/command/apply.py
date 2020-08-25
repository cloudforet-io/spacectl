import yaml, json
from spacectl.apply.manifest import Manifest
from spacectl.lib.parser import apply_manifest

import click
from pprint import pprint
from spacectl.lib import output

from spacectl.lib.output import print_data
from spacectl.conf.global_conf import RESOURCE_ALIAS, EXCLUDE_APIS, DEFAULT_PARSER
from spacectl.conf.my_conf import get_config, get_endpoint, get_template

from spacectl.modules import resource, shell

@click.group()
def cli():
    pass

@cli.command()
@click.option('-f', '--file-path', help='manifest yaml file to apply')
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['json', 'yaml']), show_default=True)
def apply(file_path, output):
    with open(file_path) as f:
        yaml_dict = yaml.safe_load(f)
    mf = Manifest(yaml_dict)

    for task in mf.tasks:
        context = {
            "var": mf.var,
            "env": mf.env,
            "tasks": mf.tasks,
            "self": task,
        }
        apply_manifest.apply_template(context, task)
        module = task.uses.split("/", 1)[-1]
        if task.apply_if:
            task.apply()  # execute each overrided method.

    # print_data(mf.to_dict(), output)