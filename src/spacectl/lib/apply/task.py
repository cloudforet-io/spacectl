import click
import abc
from functools import wraps
from spacectl.lib.apply import store

def execute_wrapper(func):
    # the instance which calls this func is bounded as self
    @wraps(func)
    def apply_inner(self):
        if self.apply_if:
            if not self.silent:
                click.echo("\n##### Start: {task_name} #####".format(task_name=self.name))
            func(self)
            if not self.silent:
                click.echo("##### Finish: {task_name} #####\n".format(task_name=self.name))
                click.echo("")
        else:
            if not self.silent:
                click.echo("\n##### Skip: {task_name} #####".format(task_name=self.name))
                click.echo("[INFO] {condition_statement} is not True\n".format(condition_statement = self.task_dict["if"]))
        store.append_task_result(self)
    return apply_inner


class Task(metaclass=abc.ABCMeta):
    fields_to_apply_template = ["name", "uses", "spec", "apply_if"]

    def __init__(self, task_dict, silent):
        self.name = task_dict.get("name", "Anonymous")
        self.id = task_dict.get("id", "no_id")
        self.uses = task_dict.get("uses")
        self.spec = {}
        self.apply_if = task_dict.get("if", True)
        self.task_dict = task_dict
        self.silent = silent
        self.output = {}
        self.set_spec(task_dict.get("spec"))

    def to_dict(self):
        fields = self.__dict__
        excluded_fields = ["task_dict", "silent"]

        d = {k: attr for k, attr in fields.items() if k not in excluded_fields}

        override_key_names = (
            ("apply_if", "if"),
        )
        for old_name, new_name in override_key_names:
            d[new_name] = d[old_name]
            del d[old_name]
        return d

    @abc.abstractmethod
    def set_spec(self, spec_dict):
        pass

    @abc.abstractmethod
    @execute_wrapper
    def execute(self):
        pass
