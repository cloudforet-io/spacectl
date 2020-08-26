import click
import yaml, json
from spacectl.apply.manifest import Manifest
from spacectl.lib.parser import apply_manifest
from spacectl.lib.output import print_data
@click.group()
def cli():
    pass

@cli.command()
@click.option('-f', '--file-path', multiple=True, help='manifest yaml file to apply. Multiple files will be overridden by order.')
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['json', 'yaml']), show_default=True)
@click.option('--no-progress', is_flag=True, default=False)
def apply(file_path, output, no_progress):
    mf = None
    for i, path in enumerate(file_path):
        f = open(path, "r")
        yaml_dict = yaml.safe_load(f)
        f.close()
        if i == 0:
            mf = Manifest(yaml_dict, no_progress)
        else:
            mf.add(yaml_dict)

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