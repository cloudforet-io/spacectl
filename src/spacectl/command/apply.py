import click

__all__ = ['cli']


@click.group()
def cli():

    pass


@cli.command()
def apply():
    """Apply a configuration to a resource by filename or stdin"""
    pass
