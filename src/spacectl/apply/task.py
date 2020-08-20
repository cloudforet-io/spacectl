import yaml
import spacectl.lib.parser.apply_manifest
from spacectl.modules.resource.conf import get_verb
import click
from functools import wraps


def apply_wrapper(func):
    # the instance which calls this func is bounded as self
    @wraps(func)
    def apply_inner(self):
        click.echo("##### Start: {task_name} #####".format(task_name=self.name))
        func(self)
        click.echo("##### Finish: {task_name} #####".format(task_name=self.name))
        click.echo("")
    return apply_inner


class Task:
    fields_to_apply_template = ["name", "uses", "spec", "apply_if"]

    def __init__(self, manifest, resource_dict):
        self.name = resource_dict.get("name", "Anonymous")
        self.id = resource_dict.get("id", "no_id")
        self.uses = resource_dict.get("uses", "@modules/resource")
        self.spec = {}
        self.apply_if = resource_dict.get("if", True)
        self.manifest = manifest
        self.set_spec(resource_dict.get("spec"))

    def to_dict(self):
        fields = self.__dict__
        excluded_fields = ["manifest"]

        d = {k: attr for k, attr in fields.items() if k not in excluded_fields}
        return d

    def set_spec(self, spec):
        print("TASK SET SPEC")

    @apply_wrapper
    def apply(self):
        pass


class TaskList(list):
    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError as e:
            try:
                return [task for task in self if task.id == attr][0]
            except IndexError:
                click.echo("The task id {attr} doesn't exist.".format(attr=attr), err=True)
                exit(1)

    def to_dict_list(self):
        return [task.to_dict() for task in self]

