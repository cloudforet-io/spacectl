import click
import copy

from spacectl.command.execute import _check_api_permissions, _get_service_and_resource, _get_client,_call_api, _parse_parameter
from spacectl.conf.my_conf import get_config, get_endpoint, get_template
from spacectl.lib.apply.task import Task
from spacectl.lib.apply.task import execute_wrapper
from spacectl.modules.resource import validate
from spacectl.lib.output import echo


class ResourceTask(Task):
    def __init__(self, task_dict, silent):
        super().__init__(task_dict, silent)

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
            echo("Start " + ".".join([service, resource, verb]), flag=not self.silent)
            _check_api_permissions(service, resource, verb)
            self.output = _execute_api(service, resource, verb, self.spec.get("data", {}), api_version="v1", output="yaml", parser={}, silent=self.silent)
            echo("Finish " + ".".join([service, resource, verb]), flag=not self.silent)
            echo(f'### {verb} Response ###', flag=not self.silent)
            echo(self.output, flag=not self.silent)
        except Exception as e:
            echo(e, err=True, terminate=True)

    def _read(self, service, resource):
        try:
            read_params = {match: self.spec["data"][match] for match in self.spec["matches"]}
            verb = self.spec["verb"]["read"]
            # list를 지원안하면 exception
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


def _execute_api(service, resource, verb, params={}, api_version='v1', output='yaml', parser=None, silent=False):

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
        echo("[INFO] Non-standard verb: " + verb, flag=not silent)
        return response