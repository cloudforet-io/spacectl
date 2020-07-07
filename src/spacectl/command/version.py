import click
import pkg_resources
from spacectl.conf.global_conf import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASCII_LOGO = os.path.join(BASE_DIR, 'template', 'ascii_logo')
LOGO_BASIC = ['#####         ', '         ######', '####################################################']

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
    return version_str

def _get_version_from_pkg():
    try:
        _version = pkg_resources.get_distribution('spacectl').version
        version_info = LOGO_BASIC[0] + 'spacectl version: ' + _version + LOGO_BASIC[1] + '\n' + LOGO_BASIC[2]
        return version_info
    except Exception:
        return None


def _get_version_from_file():

    try:
        with open(os.path.join(SRC_DIR, 'VERSION'), 'r') as f:
            _version = f.read().strip()
            f.close()
            if(_version is not None):
                version_info = LOGO_BASIC[0] + 'spacectl version: ' +  _version + LOGO_BASIC[1] + '\n' + LOGO_BASIC[2]
                return _get_ascii_logo() + version_info
    except Exception:
        return None
