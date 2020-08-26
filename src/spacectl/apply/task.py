import click
import abc
from functools import wraps


def apply_wrapper(func):
    # the instance which calls this func is bounded as self
    @wraps(func)
    def apply_inner(self):
        if self.apply_if:
            if not self.no_progress:
                click.echo("##### Start: {task_name} #####".format(task_name=self.name))
            func(self)
            if not self.no_progress:
                click.echo("##### Finish: {task_name} #####".format(task_name=self.name))
                click.echo("")
        else:
            if not self.no_progress:
                click.echo("##### Skip: {task_name} #####".format(task_name=self.name))
                click.echo("[INFO] {condition_statement} is not True".format(condition_statement = self.task_dict["if"]))
    return apply_inner


class Task(metaclass=abc.ABCMeta):
    fields_to_apply_template = ["name", "uses", "spec", "apply_if"]

    def __init__(self, manifest, task_dict, no_progress):
        self.name = task_dict.get("name", "Anonymous")
        self.id = task_dict.get("id", "no_id")
        self.uses = task_dict.get("uses")
        self.spec = {}
        self.apply_if = task_dict.get("if", True)
        self.manifest = manifest
        self.task_dict = task_dict
        self.no_progress = no_progress
        self.output = {}
        self.set_spec(task_dict.get("spec"))

    def to_dict(self):
        fields = self.__dict__
        excluded_fields = ["manifest", "task_dict"]

        d = {k: attr for k, attr in fields.items() if k not in excluded_fields}
        return d

    @abc.abstractmethod
    def set_spec(self, spec_dict):
        pass

    @abc.abstractmethod
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

    def to_list(self):
        return [task.to_dict() for task in self]

