# from spacectl.modules.shell.conf import
import subprocess
from spacectl.apply.task import Task
from spacectl.apply.task import apply_wrapper

class ShellTask(Task):
    def __init__(self, manifest, resource_dict):
        super().__init__(manifest, resource_dict)
        # self.set_spec(resource_dict)

    def set_spec(self, spec):
        self.spec = spec

    @apply_wrapper
    def apply(self):
        subprocess.run(["/bin/bash", "-c", self.spec["run"]])
