import click
import pkg_resources
from spacectl.conf.global_conf import *

ASCII_LOGO = os.path.join(ASSET_DIR, 'ascii_logo')
LOGO_BASIC = ['#####         '
              , '         ######',
              '\n',
              '####################################################']

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.command()
def version():
    """Print the client version information"""
    click.echo(_get_version_from_pkg() or _get_version_from_file() or 'unknown')


def _get_ascii_logo():
    version_str = ''
    f = open(ASCII_LOGO, 'r')
    lines = f.readlines()
    for line in lines:
        version_str = version_str+line
    f.close()
    return version_str + '\n'


def _get_version_info(_version):
    LOGO_BASIC.insert(0, _get_ascii_logo())
    LOGO_BASIC.insert(2, 'spacectl version: ' + _version)
    return ''.join(LOGO_BASIC)


def _get_version_from_pkg():
    try:
        _version = pkg_resources.get_distribution('spacectl').version
        return _get_version_info(_version)
    except Exception:
        return None


def _get_version_from_file():
    try:
        with open(os.path.join(SRC_DIR, 'VERSION'), 'r') as f:
            _version = f.read().strip()
            if _version:
                return _get_version_info(_version)
    except Exception:
        return None
