import click
import os
import copy
import yaml, json
from spacectl.lib.apply.task_manager import TaskManager
from spacectl.lib.parser import apply_manifest
from spacectl.lib.parser.default import parse_key_value
from spacectl.lib.apply import store
from spacectl.lib.output import print_data, echo
from spaceone.core import utils
import pprint


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file_path')
#@click.option('-f', '--file-path', 'file_paths', multiple=True, type=click.Path(exists=True), help='manifest yaml file to apply. Multiple files will be overridden by order.')
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['json', 'yaml', 'none']), show_default=True)
@click.option('-e', '--env', 'env', multiple=True, help='Configure additional environment variables.')
@click.option('-v', '--var', 'var', multiple=True, help='Configure additional variables. You can override existing variables as well.')
@click.option('--var-file', help='Input yaml file to configure var and env')
# @click.option('--no-progress', is_flag=True, default=False, show_default=True)
@click.option('-s', '--silent', is_flag=True, default=False, show_default=True)
def apply(file_path, output, env, var, var_file, silent):
    task_manager = TaskManager(silent)
    task_manager.load(file_path)
    task_manager.set_input(env, var, var_file)

    task_manager.run()

    if not output == 'none':
        print_data(store.get_output(), output)
