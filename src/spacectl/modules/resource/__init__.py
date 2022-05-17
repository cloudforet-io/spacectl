import click
import copy
from spaceone.core import utils
from spaceone.core.auth.jwt import JWTUtil

from spacectl.command.execute import _check_api_permissions, _get_service_and_resource, _get_client,_call_api, \
    _parse_parameter
from spacectl.conf.my_conf import get_config, get_endpoint, get_template
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper
from spacectl.modules.resource import validate
from spacectl.lib.output import echo
from spacectl.lib.template import *


class Task(BaseTask):

    def set_spec(self, spec_dict):
        self.spec = spec_dict
        if not self.spec.get("matches"):
            self.spec["matches"] = []

        self._set_mode()
        self._set_verb()

        self.spec["no_verification"] = self.spec.get("no_verification") \
            if self.spec.get("no_verification") else True

    def _set_mode(self):
        self.spec["mode"] = self.spec.get("mode", "DEFAULT")

    def _set_verb(self):
        mode = self.spec["mode"]
        custom_verb = {}
        if "verb" in self.spec:
            for k, v in self.spec["verb"].items():
                custom_verb[k] = v
        default_verb = {
            "read": "list",
            "create": "create",
            "update": "update"
        }
        validate.check_valid_verb(self.name, mode, custom_verb)
        self.spec["verb"] = default_verb
        self.spec["verb"].update(custom_verb)

    @execute_wrapper
    def execute(self):
        # execute the SpaceONE API
        service, resource = self.spec["resource_type"].split(".")
        parser = None

        if output := self.spec.get('output'):
            options = output.get('options', {})

            if output.get('template') == 'file':
                parser = self._load_parser(options.get('file', ''))
            elif output.get('template') == 'metadata':
                parser = self._load_parser_from_metadata(options.get('metadata', ''))

            self._add_only_query(parser)

        if self.spec['mode'] == 'EXEC':
            self._exec(service, resource)

        if self.spec['mode'] in ['DEFAULT', 'READ_ONLY', 'NO_UPDATE']:
            self._read(service, resource)

        if len(self.output) == 0 and self.spec['mode'] in ['DEFAULT', 'NO_UPDATE']:
            self._create(service, resource)

        if len(self.output) == 1 and self.spec['mode'] == 'DEFAULT':
            self._update(service, resource)

        if parser:
            if isinstance(self.output, list):
                self.output = [parser.parse_data(res) for res in self.output]
            elif isinstance(self.output, dict):
                self.output = parser.parse_data(self.output)

    def _exec(self, service, resource):
        try:
            verb = self.spec["verb"]["exec"]
            # echo("Start " + ".".join([service, resource, verb]), flag=not self.silent)
            _check_api_permissions(service, resource, verb)
            self.output = _execute_api(service, resource, verb, self.spec.get("data", {}), api_version="v1", output="yaml", parser={}, silent=self.silent)
            # echo("Finish " + ".".join([service, resource, verb]), flag=not self.silent)
            # echo(f'### {verb} Response ###', flag=not self.silent)
            # echo(self.output, flag=not self.silent)
        except Exception as e:
            echo(e, err=True, terminate=True)

    def _read(self, service, resource):
        try:
            read_params = {match: self.spec["data"][match] for match in self.spec["matches"]}
            verb = self.spec["verb"]["read"]

            read_resources = _execute_api(service, resource, verb, read_params, api_version="v1", output="yaml", parser={}, silent=self.silent)
            if isinstance(read_resources, list):
                length = len(read_resources)
                if length == 0:
                    self.output = {}
                elif length >= 1:
                    self.output = read_resources[0]

                if length >= 2:
                    click.echo("Multiple resources are searched so select the first one.")

            elif isinstance(read_resources, dict):  # like dict
                self.output = read_resources
            echo(f'### {verb} Response ###', flag=not self.silent)
            echo(read_resources, flag=not self.silent)
        except Exception as e:
            click.echo(e, err=True)

    def _update(self, service, resource):
        try:
            verb = self.spec["verb"]["update"]
            echo("Start " + ".".join([service, resource, verb]), flag=not self.silent)
            _check_api_permissions(service, resource, verb)
            self.output = _execute_api(service, resource, verb, self.spec['data'], api_version="v1", output="yaml", parser={}, silent=self.silent)
            echo("Finish " + ".".join([service, resource, verb]), flag=not self.silent)
            echo(f'### {verb} Response ###', flag=not self.silent)
            echo(self.output, flag=not self.silent)
        except Exception as e:
            echo(e, flag=True, err=True)
            echo(
                "Unavailable update field so Skip" +
                ".".join([service, resource, "update"]),
                flag=True, err=True, terminate=True
            )

    def _create(self, service, resource):
        verb = self.spec["verb"]["create"]
        echo("Start " + ".".join([service, resource, verb]), flag=not self.silent)
        create_result = _execute_api(service, resource, verb, self.spec['data'], api_version="v1", output="yaml", parser={}, silent=self.silent)
        echo("Finished " + ".".join([service, resource, verb]), flag=not self.silent)
        self.output = create_result
        echo(f'### {verb} Response ###', flag=not self.silent)
        echo(self.output, flag=not self.silent)

    def __str__(self):
        result_dict = {}
        for field in self.fields_to_apply_template:
            result_dict[field] = getattr(self, field)
        return str(field)

    def _load_parser(self, template_json_path):
        template = load_template(None, None, None, template_path=template_json_path)
        return load_parser(None, None, template)

    def _load_parser_from_metadata(self, metadata):
        cloud_service_type = self._get_cloud_service_type(metadata)
        user_config = self._get_user_config(metadata)
        show_optional = False

        if user_config:
            table_fields = user_config.get('data', {}).get('options', {}).get('fields', [])
            show_optional = True
        else:
            table_fields = cloud_service_type.get('metadata', {}).get('view', {}).get('table', {}).get('layout', {}).get(
                'options', {}).get('fields', [])

        template = self._generate_template_from_metadata_table_fields(table_fields, show_optional)
        return load_parser(None, None, template)

    def _add_only_query(self, parser):
        query = self.spec['data'].get('query', {})
        query['only'] = parser.keys
        self.spec['data']['query'] = query

    def _generate_template_from_metadata_table_fields(self, table_fields, show_optional):
        _list = []
        for _field in table_fields:
            if show_optional:
                _list.append(self._set_field(_field))
            else:
                if not _field.get('options', {}).get('is_optional', False):
                    _list.append(self._set_field(_field))

        return {'template': {'list': _list}}

    def _set_field(self, field):
        if key := field.get('key'):
            _f = key

            if sub_key := field.get('options', {}).get('sub_key'):
                _f = f'{_f}.{sub_key}'

            if name := field.get('name'):
                return f'{_f}|{name}'
            else:
                return _f

    def _get_resource_type_from_metadata(self, metadata):
        try:
            provider, cloud_service_group, cloud_service_type = metadata.split('.')
            return provider, cloud_service_group, cloud_service_type
        except Exception as e:
            raise Exception(e)

    def _get_user_config_name(self, metadata, user):
        provider, cloud_service_group, cloud_service_type = self._get_resource_type_from_metadata(metadata)
        return f"console:USER:{user}:page-schema:inventory.CloudService?provider={provider}&cloud_service_group={cloud_service_group}&cloud_service_type={cloud_service_type}:table"

    def _get_user_name(self):
        api_key = get_config().get('api_key', '')
        user_name = JWTUtil.unverified_decode(api_key).get('aud', '')
        return user_name

    def _get_user_config(self, metadata):
        verb = 'list'
        params = {
            'name': self._get_user_config_name(metadata, self._get_user_name())
        }
        responses = _execute_api('config', 'UserConfig', verb, params, api_version="v1", output="json", parser={}, silent=True)

        if responses:
            return responses[0]
        else:
            return {}

    def _get_cloud_service_type(self, metadata):
        provider, cloud_service_group, cloud_service_type = self._get_resource_type_from_metadata(metadata)

        verb = 'list'
        params = {
            'provider': provider,
            'group': cloud_service_group,
            'name': cloud_service_type
        }
        responses = _execute_api('inventory', 'CloudServiceType', verb, params,
                                 api_version="v1", output="json", parser={}, silent=True)

        if len(responses) > 0:
            return responses[0]
        else:
            return {}


def _execute_api(service, resource, verb, params={}, api_version='v1', output='yaml', parser=None, silent=False):
    config = get_config()
    _check_api_permissions(service, resource, verb)
    client = _get_client(service, api_version)

    # _call_api can change some data of params so need deepcopy
    # e.g. credential of identity.Token
    response_stream = _call_api(client, resource, verb, copy.deepcopy(params), config=config)

    for response in response_stream:
        if verb in ['list', 'stat']:
            results = response.get('results', [])

            if len(results) == 0:
                return []
            elif len(results) > 0:
                return results
            else:
                Exception()
        elif verb == 'create':
            return response
        elif verb == 'update':
            return response
        else:
            echo("[INFO] Non-standard verb: " + verb, flag=not silent)
            return response
