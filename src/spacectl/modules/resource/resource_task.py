import click

from spacectl.command.execute import _check_api_permissions, _get_service_and_resource, _get_client,_call_api, _parse_parameter
from spacectl.conf.my_conf import get_config, get_endpoint, get_template

from spacectl.modules.resource.conf import get_verb
from spacectl.apply.task import Task
from spacectl.apply.task import apply_wrapper

class ResourceTask(Task):
    def __init__(self, manifest, resource_dict):
        super().__init__(manifest, resource_dict)
        self.executed_verbs = []


    def set_spec(self, spec):
        self.spec = spec
        if not self.spec.get("matches"):
            self.spec["matches"] = []

        read_verb, create_verb, update_verb = get_verb(self.spec["resource_type"])
        verb = {
            "read": read_verb,
            "create": create_verb,
            "update": update_verb
        }
        for default_verb, custom_verb in spec.get("verb", {}).items():
            verb.update({default_verb: custom_verb})
        self.spec["verb"] = verb

        self.spec["no_verification"] = self.spec.get("no_verification") \
            if self.spec.get("no_verification") else True

    @apply_wrapper
    def apply(self):
        # spaceone api 실행
        service, resource = self.spec["resource_type"].split(".")
        read_params = {match: self.spec["data"][match] for match in self.spec["matches"]}
        read_resources = []
        if self.spec["verb"]["read"]:
            try:
                verb = self.spec["verb"]["read"]
                # list를 지원안하면 exception
                read_resources = _execute_api(service, resource, verb, read_params, api_version="v1", output="yaml", parser={})
                self.executed_verbs.append(verb)
                if isinstance(read_resources, list):
                    length = len(read_resources)
                    if length == 0:
                        self.output = {}
                    elif length >= 1:
                        self.output = read_resources[0]

                    if length >= 2:
                        click.echo("Multiple resources are searched so select the first one.")

                    self.output["read_length"] = len(read_resources)
                elif isinstance(read_resources, dict):  # like dict
                    self.output = read_resources
                    if read_resources != {}: self.output["read_length"] = 1
                click.echo(f'### {verb} Response ###')
                click.echo(read_resources)
            except Exception as e:
                click.echo(e, err=True)

        params = {key: value for key, value in self.spec["data"].items()}

        if len(read_resources) == 1 and self.spec["verb"]["update"]:
            try:
                verb = self.spec["verb"]["update"]
                click.echo("Start " + ".".join([service, resource, verb]))
                _check_api_permissions(service, resource, verb)
                self.output = _execute_api(service, resource, verb, params, api_version="v1", output="yaml", parser={})
                self.executed_verbs.append(verb)
                click.echo("Finish " + ".".join([service, resource, verb]))
                click.echo(f'### {verb} Response ###')
                click.echo(self.output)
            except Exception as e:
                click.echo(e, err=True)
                click.echo("Unavailable update field so Skip" +
                           ".".join([service, resource, "update"]),
                           err=True)
                # self.output = read_resources[0]
                # self.output["length"] = 0

        elif len(read_resources) == 0 and self.spec["verb"]["create"]:
            verb = self.spec["verb"]["create"]
            click.echo("Start " + ".".join([service, resource, verb]))
            create_result = _execute_api(service, resource, verb, params, api_version="v1", output="yaml", parser={})
            self.executed_verbs.append(verb)
            click.echo("Finished " + ".".join([service, resource, verb]))
            self.output = create_result
            click.echo(f'### {verb} Response ###')
            click.echo(self.output)
        else:
            click.echo(f'No Create or Update on {self}')

def _execute_api(service, resource, verb, params={}, api_version='v1', output='yaml', parser=None):
    config = get_config()
    _check_api_permissions(service, resource, verb)
    client = _get_client(service, api_version)

    response = _call_api(client, resource, verb, params, config=config)

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
        click.echo("Non-standard verb: "+ verb)
        return response