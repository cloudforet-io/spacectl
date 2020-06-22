#!/usr/bin/env python3

import click
import traceback
from command import apply, config, endpoint, execute, version, api_resource, template

_DEBUG = False
_HELP = """
spacectl controls the SpaceONE services\n
API Reference: https://spaceone-dev.gitbook.io/spaceone-apis\n
Following steps for first time user.\n
    1. spacectl config init\n
    2. spacectl endpoint init
"""

cli = click.CommandCollection(sources=[apply.cli, config.cli, endpoint.cli, execute.cli,
                                       version.cli, api_resource.cli, template.cli], help=_HELP)


def main():
    try:
        cli(prog_name='spacectl')
    except Exception as e:
        click.echo(f'ERROR: {e}')
        click.echo()

        if _DEBUG:
            click.echo(traceback.format_exc())


if __name__ == '__main__':
    main()
