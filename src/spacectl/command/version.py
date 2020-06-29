import click
import pkg_resources
from spacectl.conf.global_conf import *

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.command()
def version():
    """Print the client version information"""
    click.echo(_get_version_from_pkg() or _get_version_from_file() or 'unknown')


def _get_version_from_pkg():
    try:
        return pkg_resources.get_distribution('spacectl').version
    except Exception:
        return None


def _get_version_from_file():
    try:
        with open(os.path.join(SRC_DIR, 'VERSION'), 'r') as f:
            _version = f.read().strip()
            f.close()
            return _version
    except Exception:
        return None
