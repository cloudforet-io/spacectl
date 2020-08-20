import yaml
from spacectl.apply.task import Task, TaskList
from spacectl.modules.resource.resource_task import ResourceTask
from spacectl.modules.shell.shell_task import ShellTask


class Manifest:

    def __init__(self, manifest_dict):
        self.var = manifest_dict["var"]
        self.env = manifest_dict["env"]
        self.tasks = TaskList()

        for task_dict in manifest_dict["tasks"]:
            module = task_dict["uses"].split("/")[-1]
            task = None
            if module == "resource":
                task = ResourceTask(self, task_dict)
            elif module == "shell":
                task = ShellTask(self, task_dict)
            self.tasks.append(task)

    def to_dict(self):
        return {
            "var": self.var,
            "env": self.env,
            "tasks": self.tasks.to_dict_list()
        }