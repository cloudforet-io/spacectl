import os
import click
from spacectl.lib.apply.task_manager import TaskManager
from spacectl.lib.apply import store


@click.group()
def cli():
    pass


@cli.command()
@click.argument('file_path')
@click.option('-o', '--output', default='none', help='Output format',
              type=click.Choice(['json', 'yaml', 'none']), show_default=True)
@click.option('-e', '--env', 'env', multiple=True, help='Configure additional environment variables.')
@click.option('-v', '--var', 'var', multiple=True,
              help='Configure additional variables. You can override existing variables as well.')
@click.option('--var-file', type=click.Path(exists=True), help='Yaml file to configure var and env')
@click.option('-s', '--silent', is_flag=True, default=False, show_default=True)
def apply(file_path, output, env, var, var_file, silent):
    store.init_env(env)
    store.init_var(var_file, var)
    task_manager = TaskManager(silent, output)
    task_manager.load(file_path)

    task_manager.run()


if __name__ == '__main__':
    apply()
