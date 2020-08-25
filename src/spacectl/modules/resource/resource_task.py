import click
import copy

from spacectl.command.execute import _check_api_permissions, _get_service_and_resource, _get_client,_call_api, _parse_parameter
from spacectl.conf.my_conf import get_config, get_endpoint, get_template

from spacectl.modules.resource.conf import get_verb
from spacectl.apply.task import Task
from spacectl.apply.task import apply_wrapper
from spacectl.modules.resource import validate

class ResourceTask(Task):
    def __init__(self, manifest, resource_dict):
        super().__init__(manifest, resource_dict)

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


    @apply_wrapper
    def apply(self):
        # spaceone api 실행
        service, resource = self.spec["resource_type"].split(".")
        if self.spec['mode'] == 'EXEC':
            self._exec(service, resource)

        if self.spec['mode'] in ['DEFAULT', 'READ_ONLY', 'NO_UPDATE']:
            self._read(service, resource)

        if len(self.output) == 0 and self.spec['mode'] in ['DEFAULT', 'NO_UPDATE']:
            self._create(service, resource)

        if len(self.output) == 1 and self.spec['mode'] == 'DEFAULT':
            self._update(service, resource)

    def _exec(self, service, resource):
        try:
            verb = self.spec["verb"]["exec"]
            click.echo("Start " + ".".join([service, resource, verb]))
            _check_api_permissions(service, resource, verb)
            self.output = _execute_api(service, resource, verb, self.spec.get("data", {}), api_version="v1", output="yaml", parser={})
            click.echo("Finish " + ".".join([service, resource, verb]))
            click.echo(f'### {verb} Response ###')
            click.echo(self.output)
        except Exception as e:
            click.echo(e, err=True)
            exit(1)

    def _read(self, service, resource):
        try:
            read_params = {match: self.spec["data"][match] for match in self.spec["matches"]}
            verb = self.spec["verb"]["read"]
            # list를 지원안하면 exception
            read_resources = _execute_api(service, resource, verb, read_params, api_version="v1", output="yaml", parser={})
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
            click.echo(f'### {verb} Response ###')
            click.echo(read_resources)
        except Exception as e:
            click.echo(e, err=True)
    def _update(self, service, resource):
        try:
            verb = self.spec["verb"]["update"]
            click.echo("Start " + ".".join([service, resource, verb]))
            _check_api_permissions(service, resource, verb)
            self.output = _execute_api(service, resource, verb, self.spec['data'], api_version="v1", output="yaml", parser={})
            click.echo("Finish " + ".".join([service, resource, verb]))
            click.echo(f'### {verb} Response ###')
            click.echo(self.output)
        except Exception as e:
            click.echo(e, err=True)
            click.echo("Unavailable update field so Skip" +
                       ".".join([service, resource, "update"]),
                       err=True)
    def _create(self, service, resource):
        verb = self.spec["verb"]["create"]
        click.echo("Start " + ".".join([service, resource, verb]))
        create_result = _execute_api(service, resource, verb, self.spec['data'], api_version="v1", output="yaml", parser={})
        click.echo("Finished " + ".".join([service, resource, verb]))
        self.output = create_result
        click.echo(f'### {verb} Response ###')
        click.echo(self.output)

    def __str__(self):
        result_dict = {}
        for field in self.fields_to_apply_template:
            result_dict[field] = getattr(self, field)
        return str(field)
def _execute_api(service, resource, verb, params={}, api_version='v1', output='yaml', parser=None):

    config = get_config()
    _check_api_permissions(service, resource, verb)
    client = _get_client(service, api_version)

    # _call_api can change some data of params so need deepcopy
    # e.g. credential of identity.Token
    response = _call_api(client, resource, verb, copy.deepcopy(params), config=config)

    if verb == 'list':
        results = response.get('results', [])
        if len(results) == 0:
            return []
        elif len(results) > 1:
            Exception()
        else:
            return results
    elif verb == 'create':
        return response
    elif verb == 'update':
        return response
    else:
        click.echo("Non-standard verb: " + verb)
        return response