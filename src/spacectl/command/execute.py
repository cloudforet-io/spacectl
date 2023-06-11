import click
import fnmatch
import types
import os

from google.protobuf.json_format import MessageToDict
from spaceone.core.error import ERROR_BASE
from spaceone.core import pygrpc
from spaceone.core.utils import parse_endpoint, load_json

from spacectl.lib.output import print_data
from spacectl.lib.template import *
from spacectl.conf.global_conf import RESOURCE_ALIAS, EXCLUDE_APIS
from spacectl.conf.my_conf import get_config, get_endpoint

__all__ = ['cli']


@click.group()
def cli():
    pass


@cli.command()
@click.argument('resource')
@click.option('-p', '--parameter', multiple=True, help='Input Parameter (-p <key>=<value> -p ...)')
@click.option('-j', '--json-parameter', help='JSON parameter')
@click.option('-f', '--file-parameter', 'file_path', type=click.Path(exists=True), help='YAML file only')
@click.option('-v', '--api-version', default='v1', help='API Version', show_default=True)
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['json', 'yaml']), show_default=True)
def get(resource, parameter, json_parameter, file_path, api_version, output):
    """Show details of a specific resource"""
    service, resource = _get_service_and_resource(resource)
    params = _parse_parameter(file_path, json_parameter, parameter)
    _execute_api(service, resource, 'get', params=params, api_version=api_version, output=output)


@cli.command()
@click.argument('resource')
@click.option('-p', '--parameter', multiple=True, help='Parameter (-p <key>=<value>)')
@click.option('-j', '--json-parameter', help='JSON type parameter')
@click.option('-f', '--file-parameter', 'file_path', type=click.Path(exists=True), help='Parameter file (YAML)')
@click.option('-m', '--minimal', 'minimal_columns', is_flag=True, help='Minimal columns')
@click.option('-a', '--all', 'all_columns', is_flag=True, help='All columns')
@click.option('-c', '--columns', help='Specific columns (-c id,name)')
@click.option('-t', '--template-file', 'template_path', type=click.Path(exists=True), help='Template file (YAML)')
@click.option('-l', '--limit', type=int, help='Number of rows')
@click.option('-s', '--sort', help="Sorting by given key (-s [-]<key>)")
@click.option('-v', '--api-version', default='v1', help='API Version', show_default=True)
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml', 'csv', 'quiet']), show_default=True)
def list(resource, parameter, json_parameter, file_path, minimal_columns, all_columns, columns, template_path,
         limit, sort, api_version, output):
    """Display one or many resources"""
    service, resource = _get_service_and_resource(resource)

    if columns:
        columns = columns.split(',')

    template = load_template(service, resource, columns, template_path=template_path)
    parser = None

    params = _parse_parameter(file_path, json_parameter, parameter)
    params['query'] = params.get('query', {})

    if all_columns:
        params['query']['minimal'] = False
    elif minimal_columns:
        params['query']['minimal'] = True
    elif template:
        parser = load_parser(service, resource, template)
        params['query']['only'] = parser.keys

    if limit:
        params['query']['page'] = {'limit': limit}

    if sort:
        if sort.startswith('-'):
            desc = True
            sort_key = sort[1:]
        else:
            desc = False
            sort_key = sort

        if parser:
            sort_key = parser.get_sort_key(sort_key) or sort_key

        params['query']['sort'] = {
            'key': sort_key,
            'desc': desc
        }

    _execute_api(service, resource, 'list', params=params, api_version=api_version, output=output, parser=parser)


@cli.command()
@click.argument('resource')
@click.option('-p', '--parameter', multiple=True, help='Input Parameter (-p <key>=<value> -p ...)')
@click.option('-j', '--json-parameter', help='JSON type parameter')
@click.option('-f', '--file-parameter', 'file_path', type=click.Path(exists=True), help='YAML file only')
@click.option('-c', '--columns', help='Specific columns (-c id,name)')
@click.option('-l', '--limit', type=int, help='Number of rows')
@click.option('-v', '--api-version', default='v1', help='API Version', show_default=True)
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml', 'csv', 'quiet']), show_default=True)
def analyze(resource, parameter, json_parameter, file_path, columns, limit, api_version, output):
    """Analyze resources"""
    service, resource = _get_service_and_resource(resource)
    parser = None

    if columns:
        columns = columns.split(',')
        template = load_template(service, resource, columns)
        parser = load_parser(service, resource, template)

    params = _parse_parameter(file_path, json_parameter, parameter)

    if limit:
        params['query'] = params.get('query', {})
        params['query']['page'] = {'limit': limit}

    _execute_api(service, resource, 'analyze', params=params, api_version=api_version, output=output, parser=parser)

@cli.command()
@click.argument('resource')
@click.option('-p', '--parameter', multiple=True, help='Input Parameter (-p <key>=<value> -p ...)')
@click.option('-j', '--json-parameter', help='JSON type parameter')
@click.option('-f', '--file-parameter', 'file_path', type=click.Path(exists=True), help='YAML file only')
@click.option('-c', '--columns', help='Specific columns (-c id,name)')
@click.option('-l', '--limit', type=int, help='Number of rows')
@click.option('-v', '--api-version', default='v1', help='API Version', show_default=True)
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml', 'csv', 'quiet']), show_default=True)
def stat(resource, parameter, json_parameter, file_path, columns, limit, api_version, output):
    """Querying statistics for resources"""
    service, resource = _get_service_and_resource(resource)
    parser = None

    if columns:
        columns = columns.split(',')
        template = load_template(service, resource, columns)
        parser = load_parser(service, resource, template)

    params = _parse_parameter(file_path, json_parameter, parameter)

    if limit:
        if service == 'statistics' and resource == 'Resource':
            params['page'] = {'limit': limit}
        else:
            params['query'] = params.get('query', {})
            params['query']['page'] = {'limit': limit}

    _execute_api(service, resource, 'stat', params=params, api_version=api_version, output=output, parser=parser)


@cli.command()
@click.argument('verb')
@click.argument('resource')
@click.option('-p', '--parameter', multiple=True, help='Input Parameter (-p <key>=<value> -p ...)')
@click.option('-j', '--json-parameter', help='JSON parameter')
@click.option('-f', '--file-parameter', 'file_path', type=click.Path(exists=True), help='YAML file only')
@click.option('-v', '--api-version', default='v1', help='API Version', show_default=True)
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['table', 'csv', 'json', 'yaml']), show_default=True)
def exec(verb, resource, parameter, json_parameter, file_path, api_version, output):
    """Execute a method to resource"""
    service, resource = _get_service_and_resource(resource)
    params = _parse_parameter(file_path, json_parameter, parameter)
    _execute_api(service, resource, verb, params=params, api_version=api_version, output=output)


def _parse_parameter(file_parameter=None, json_parameter=None, parameter=None):
    if parameter is None:
        parameter = []

    if file_parameter:
        params = load_yaml_from_file(file_parameter)
    else:
        params = {}

    if json_parameter:
        json_params = load_json(json_parameter)
        params.update(json_params)

    for p in parameter:
        p_split = p.split('=')
        if len(p_split) == 2:
            params[p_split[0]] = p_split[1]
        else:
            raise ValueError(f'Input parameter({p}) is invalid. (format: key=value)')

    return params


def _execute_api(service, resource, verb, params=None, api_version='v1', output='yaml', parser=None):
    if params is None:
        params = {}

    config = get_config()
    _check_api_permissions(service, resource, verb)
    client = _get_client(service, api_version)
    response_stream = _call_api(client, resource, verb, params, config=config)

    for response in response_stream:
        if verb in ['list', 'stat', 'analyze'] and parser:
            results = []
            try:
                for result in response.get('results', []):
                    results.append(parser.parse_data(result))
            except Exception:
                raise Exception(f'{service}.{resource} template format is invalid.')

            response['results'] = results
        options = {}

        if 'total_count' in response:
            options['total_count'] = response['total_count']

        if output in ['table', 'csv', 'quiet'] and 'results' in response:
            options['root_key'] = 'results'

            print_data(response, output, **options)
        else:
            print_data(response, output)


def _check_api_permissions(service, resource, verb):
    request_api = f'{service}.{resource}.{verb}'

    for exclude_api in EXCLUDE_APIS:
        if fnmatch.fnmatch(request_api, exclude_api):
            raise Exception(f"{request_api} not allowed.")


def _get_service_and_resource(resource):
    if resource in RESOURCE_ALIAS:
        return RESOURCE_ALIAS[resource]
    else:
        resource_split = resource.split('.')
        if len(resource_split) != 2:
            raise ValueError(f'Resource format is invalid. (resource = <service>.<resource>)')
        return resource_split[0], resource_split[1]


def _get_client(service, api_version):
    endpoint = get_endpoint(service)

    if endpoint is None:
        raise Exception(f'Endpoint is not set. (service={service})')

    try:
        e = parse_endpoint(endpoint)

        protocol = e.get('scheme')

        if protocol not in ['grpc', 'grpc+ssl']:
            raise ValueError(f'Unsupported protocol. (supported protocol = grpc | grpc+ssl, endpoint={endpoint})')

        if protocol == 'grpc+ssl':
            ssl_enabled = True
        else:
            ssl_enabled = False

        client = pygrpc.client(endpoint=f'{e.get("hostname")}:{e.get("port")}',
                               version=api_version, ssl_enabled=ssl_enabled, max_message_length=1024*1024*256)
        client.service = service
        client.api_version = api_version
        return client
    except ERROR_BASE as e:
        raise e
    except Exception:
        raise ValueError(f'Endpoint is invalid. (endpoint={endpoint})')


def _check_resource_and_verb(client, resource, verb):
    if not hasattr(client, resource):
        raise Exception(f"'{client.service}.{client.api_version}' service does not have a '{resource}' resource.")

    if not hasattr(getattr(client, resource), verb):
        raise Exception(f"'{client.service}.{client.api_version}.{resource}' resource does not have a '{verb}' verb.")


def _call_api(client, resource, verb, params=None, **kwargs):
    if params is None:
        params = {}

    _check_resource_and_verb(client, resource, verb)

    config = kwargs.get('config', {})
    api_key = config.get('api_key')
    domain_id = config.get('domain_id')

    if domain_id:
        params['domain_id'] = config.get('domain_id')

    try:
        metadata = (()) if api_key is None else (('token', api_key),)
        resource_client = getattr(client, resource)
        resource_verb = getattr(resource_client, verb)
        response_or_iterator = resource_verb(
            params,
            metadata=metadata
        )
        if isinstance(response_or_iterator, Exception):
            raise response_or_iterator
        elif isinstance(response_or_iterator, types.GeneratorType):
            for response in response_or_iterator:
                yield _change_message(response)
        else:
            yield _change_message(response_or_iterator)
    except ERROR_BASE as e:
        if e.error_code == 'ERROR_AUTHENTICATE_FAILURE':
            raise Exception('The api_key is not set or incorrect. (Use "spacectl config init")')
        else:
            raise Exception(e.message.strip())
    except Exception as e:
        if hasattr(e, 'exception'):
            raise Exception(e.exception())
        else:
            raise Exception(e)


def _change_message(message):
    return MessageToDict(message, preserving_proto_field_name=True)
