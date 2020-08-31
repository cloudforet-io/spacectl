import click
import os
import copy
import yaml, json
from spacectl.apply.manifest import Manifest
from spacectl.lib.parser import apply_manifest
from spacectl.lib.parser.default import parse_key_value

from spacectl.lib.output import print_data, echo
import pprint


@click.group()
def cli():
    pass


@cli.command()
@click.option('-f', '--file-path', 'file_paths', multiple=True, type=click.Path(exists=True), help='manifest yaml file to apply. Multiple files will be overridden by order.')
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['json', 'yaml']), show_default=True)
@click.option('-e', '--env', 'env', multiple=True, help='Configure additional environment variables. e.g. -e a=b -e c=d')
@click.option('--set', 'var', multiple=True, help='Configure additional variables. You can override existing variables as well. e.g. --set a=b --set c=d')
@click.option('--no-progress', is_flag=True, default=False, show_default=True)
def apply(file_paths, output, env, var, no_progress):
    mf = None
    for i, path in enumerate(file_paths):
        f = open(path, "r")
        yaml_dict = yaml.safe_load(f)
        f.close()
        if i == 0:
            mf = Manifest(yaml_dict, no_progress)
        else:
            mf.add(yaml_dict)
    parsed_var = parse_key_value(var)
    mf.update("var", parsed_var)

    parsed_env = copy.deepcopy(os.environ)
    parsed_env.update(parse_key_value(env))
    mf.update("env", parsed_env)

    pprint.pprint(mf.to_dict())

    for task in mf.tasks:
        context = {
            "var": mf.var,
            "env": mf.env,
            "tasks": mf.tasks,
            "self": task,
        }
        apply_manifest.apply_template(context, task)
        task.apply()  # execute each overrided method.

    print_data(mf.to_dict(), output)
