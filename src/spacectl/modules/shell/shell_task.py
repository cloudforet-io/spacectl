# from spacectl.modules.shell.conf import
from spacectl.command.apply.task import Task

class ShellTask(Task):
    def __init__(self, manifest, resource_dict):
        super().__init__(manifest, resource_dict)
        # self.set_spec(resource_dict)

    def set_spec(self, spec):
        self.spec = spec
