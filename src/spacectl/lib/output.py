import click
import csv
import sys
from tabulate import tabulate
from spaceone.core import utils


def print_data(data, output, **kwargs):
    if 'root_key' in kwargs:
        data = utils.get_dict_value(data, kwargs['root_key'], [])
        del kwargs['root_key']

    if output == 'table':
        if len(data) == 0:
            echo('NO DATA')
        else:
            _print_table(data, **kwargs)
    elif output == 'json':
        _print_json(data, **kwargs)
    elif output == 'yaml':
        _print_yaml(data, **kwargs)
    elif output == 'csv':
        _print_csv(data, **kwargs)
    elif output == 'quiet':
        _print_quiet(data, **kwargs)
    elif output == 'text':
        echo(data)


def _print_table(data, **kwargs):
    data, headers, total_count = _parse_data_by_options(data, **kwargs)

    if isinstance(data, dict):
        _print_yaml(data)
    else:
        click.echo(tabulate(data, tablefmt='presto', headers=headers or 'keys'))

        if total_count:
            click.echo()
            click.echo(f' Count: {len(data)} / {int(total_count)}')


def _print_csv(data, **kwargs):
    data, headers, total_count = _parse_data_by_options(data, **kwargs)

    if isinstance(data, dict):
        _print_yaml(data)
    else:
        if headers:
            writer = csv.writer(sys.stdout)
            writer.writerow(headers)
            writer.writerows(data)
        else:
            writer = csv.DictWriter(sys.stdout, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)


def _parse_data_by_options(data, **kwargs):
    headers = kwargs.get('headers')
    total_count = kwargs.get('total_count')

    if isinstance(data, list) and len(data) > 0 and not isinstance(data[0], (dict, list, tuple)):
        headers = ['Values']
        data = [[v] for v in data]

    return data, headers, total_count


def _print_json(data, **kwargs):
    if data == {}:
        click.echo()
    else:
        click.echo(utils.dump_json(data, indent=4))


def _print_yaml(data, **kwargs):
    if data == {}:
        click.echo()
    else:
        click.echo('---')
        click.echo(utils.dump_yaml(data))


def _print_quiet(data, **kwargs):
    for d in data:
        items = list(d.values())
        if len(items) != 1:
            click.echo("Please Selector only one column for quiet output.", err=True)
            exit(1)

        click.echo(items[0])


def echo(message, flag=True, err=False, terminate=False):
    if flag:
        click.echo(message, err=err)
    if terminate:
        exit(1)
