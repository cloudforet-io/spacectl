import yaml
from spacectl.apply.task import Task, TaskList
from spacectl.modules.resource.resource_task import ResourceTask
from spacectl.modules.shell.shell_task import ShellTask
from spacectl.lib.output import echo

import click

class Manifest:

    def __init__(self, manifest_dict, no_progress):
        self.var = manifest_dict.get("var", {})
        self.env = manifest_dict.get("env", {})
        self.tasks = TaskList()

        for task_dict in manifest_dict.get("tasks", []):
            task = self._create_task(task_dict, no_progress)
            self.tasks.append(task)
        self.no_progress = no_progress

    def add(self, manifest_dict):
        self.var.update(manifest_dict.get("var", {}))
        self.env.update(manifest_dict.get("env", {}))
        for task_dict in manifest_dict.get("tasks", []):
            task = self._create_task(task_dict, self.no_progress)
            self.tasks.append(task)

    def update(self, key, value_dict):
        if not isinstance(getattr(self, key), dict):
            echo(f'{key} is a valid update field of Manifest', err=True, terminate=True)
        getattr(self, key).update(value_dict)


    def to_dict(self):
        return {
            "var": self.var,
            # "env": self.env,
            "tasks": self.tasks.to_list()
        }

    def _create_task(self, task_dict, no_progress):
        module = task_dict["uses"].split("/")[-1]
        task = None
        if module == "resource":
            task = ResourceTask(self, task_dict, no_progress)
        elif module == "shell":
            task = ShellTask(self, task_dict, no_progress)
        else:
            click.echo('{uses} is not a valid "uses" type.'.format(uses=task_dict["uses"]), err=True)
        return task
