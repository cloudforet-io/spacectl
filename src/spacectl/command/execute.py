import click
import fnmatch

from google.protobuf.json_format import MessageToDict
from spaceone.core.error import ERROR_BASE
from spaceone.core import pygrpc
from spaceone.core.utils import parse_endpoint, load_json, load_yaml_from_file

from lib.output import print_data
from conf.global_conf import RESOURCE_ALIAS, EXCLUDE_APIS, DEFAULT_ENVIRONMENT, DEFAULT_PARSER
from conf.my_conf import get_config, get_endpoint, get_template

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
@click.option('-e', '--environment', default=lambda: get_config('environment', DEFAULT_ENVIRONMENT),
              help='Environment', show_default=True)
def get(resource, parameter, json_parameter, file_path, api_version, output, environment):
    """Show details of a specific resource"""
    service, resource = _get_service_and_resource(resource)
    params = _parse_parameter(file_path, json_parameter, parameter)
    _execute_api(service, resource, 'get', params=params, api_version=api_version, output=output, env=environment)


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
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
@click.option('-e', '--environment', default=lambda: get_config('environment', DEFAULT_ENVIRONMENT),
              help='Environment', show_default=True)
def list(resource, parameter, json_parameter, file_path, minimal_columns, all_columns, columns, template_path,
         limit, sort, api_version, output, environment):
    """Display one or many resources"""
    service, resource = _get_service_and_resource(resource)
    template = _load_template(service, resource, columns, template_path)
    parser = None

    params = _parse_parameter(file_path, json_parameter, parameter)
    params['query'] = params.get('query', {})

    if all_columns:
        params['query']['minimal'] = False
    elif minimal_columns:
        params['query']['minimal'] = True
    elif template:
        parser = _load_parser(service, resource, template)
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

    _execute_api(service, resource, 'list', params=params, api_version=api_version, output=output,
                 env=environment, parser=parser)


@cli.command()
@click.argument('resource')
@click.option('-j', '--json-parameter', help='JSON type parameter')
@click.option('-f', '--file-parameter', 'file_path', type=click.Path(exists=True), help='YAML file only')
@click.option('-l', '--limit', type=int, help='Number of rows')
@click.option('-s', '--sort', help="Sorting by given key (-s [-]<key>)")
@click.option('-v', '--api-version', default='v1', help='API Version', show_default=True)
@click.option('-o', '--output', default='table', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
@click.option('-e', '--environment', default=lambda: get_config('environment', DEFAULT_ENVIRONMENT),
              help='Environment', show_default=True)
def stat(resource, json_parameter, file_path, limit, sort, api_version, output, environment):
    """Querying statistics for resources"""
    service, resource = _get_service_and_resource(resource)
    params = _parse_parameter(file_path, json_parameter)
    params['query'] = params.get('query', {})

    if limit:
        params['query']['page'] = {'limit': limit}

    if sort:
        if sort.startswith('-'):
            desc = True
            sort_key = sort[1:]
        else:
            desc = False
            sort_key = sort

        params['query']['sort'] = {
            'name': sort_key,
            'desc': desc
        }

    _execute_api(service, resource, 'stat', params=params, api_version=api_version, output=output, env=environment)


@cli.command()
@click.argument('verb')
@click.argument('resource')
@click.option('-p', '--parameter', multiple=True, help='Input Parameter (-p <key>=<value> -p ...)')
@click.option('-j', '--json-parameter', help='JSON parameter')
@click.option('-f', '--file-parameter', 'file_path', type=click.Path(exists=True), help='YAML file only')
@click.option('-v', '--api-version', default='v1', help='API Version', show_default=True)
@click.option('-o', '--output', default='yaml', help='Output format',
              type=click.Choice(['table', 'json', 'yaml']), show_default=True)
@click.option('-e', '--environment', default=lambda: get_config('environment', DEFAULT_ENVIRONMENT),
              help='Environment', show_default=True)
def exec(verb, resource, parameter, json_parameter, file_path, api_version, output, environment):
    """Execute a method to resource"""
    service, resource = _get_service_and_resource(resource)
    params = _parse_parameter(file_path, json_parameter, parameter)
    _execute_api(service, resource, verb, params=params, api_version=api_version, output=output, env=environment)


def _parse_parameter(file_parameter=None, json_parameter=None, parameter=[]):
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


def _execute_api(service, resource, verb, params={}, api_version='v1', output='yaml', env=None, parser=None):
    config = get_config()
    _check_api_permissions(service, resource, verb)
    client = _get_client(service, api_version, env)
    response = _call_api(client, resource, verb, params, config=config)

    if verb == 'list' and parser:
        results = []
        try:
            for result in response.get('results', []):
                results.append(parser.parse_data(result))
        except Exception:
            raise Exception(f'{service}.{resource} template format is invalid.')

        response['results'] = results

    if verb in ['list', 'stat']:
        options = {
            'root_key': 'results'
        }

        if 'total_count' in response:
            options['total_count'] = response['total_count']

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


def _get_client(service, api_version, env):
    if env is None:
        raise Exception('The environment of spaceconfig is not set. (Use "spacectl config init")')

    endpoint = get_endpoint(env, service)

    if endpoint is None:
        raise Exception(f'Endpoint is not set. (environment={env}, service={service})')

    try:
        e = parse_endpoint(endpoint)
        client = pygrpc.client(endpoint=f'{e.get("hostname")}:{e.get("port")}',
                               version=api_version, max_message_length=1024*1024*256)
        client.service = service
        client.api_version = api_version
        return client
    except Exception:
        raise ValueError(f'Endpoint is invalid. (endpoint={endpoint})')


def _check_resource_and_verb(client, resource, verb):
    if not hasattr(client, resource):
        raise Exception(f"'{client.service}.{client.api_version}' service does not have a '{resource}' resource.")

    if not hasattr(getattr(client, resource), verb):
        raise Exception(f"'{client.service}.{client.api_version}.{resource}' resource does not have a '{verb}' verb.")


def _call_api(client, resource, verb, params={}, **kwargs):
    config = kwargs.get('config', {})
    if 'api_key' not in config:
        raise Exception('The api_key of spaceconfig is not set. (Use "spacectl config init")')

    _check_resource_and_verb(client, resource, verb)

    api_key = config['api_key']
    params['domain_id'] = config.get('domain_id')

    try:
        message = getattr(getattr(client, resource), verb)(
            params,
            metadata=(('token', api_key),)
        )
        return _change_message(message)
    except ERROR_BASE as e:
        raise Exception(e.message.strip())
    except Exception as e:
        raise Exception(e)


def _change_message(message):
    return MessageToDict(message, preserving_proto_field_name=True)


def _load_template(service, resource, columns, template_path):
    if columns:
        template = {
            'template': {
                'list': columns.split(',')
            }
        }
    elif template_path:
        template = load_yaml_from_file(template_path)
    else:
        template = get_template(service, resource)
    return template


def _load_parser(service, resource, template):
    parser = template.get('parser', DEFAULT_PARSER)
    template = template.get('template')

    if parser is None:
        raise Exception(f"'parser' is undefined in {service}.{resource} template.")

    if template is None:
        raise Exception(f"'template' is undefined in {service}.{resource} template.")

    try:
        module_name, class_name = parser.rsplit('.', 1)
        parser_module = __import__(module_name, fromlist=[class_name])
    except Exception:
        raise Exception(f'Parser is invalid. ({parser})')

    try:
        return getattr(parser_module, class_name)(template)
    except Exception:
        raise Exception(f'{service}.{resource} template format is invalid.')
