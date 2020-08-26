# from spacectl.modules.shell.conf import
import subprocess
from spacectl.apply.task import Task
from spacectl.apply.task import apply_wrapper

class ShellTask(Task):
    def __init__(self, manifest, resource_dict, no_progress):
        super().__init__(manifest, resource_dict, no_progress)
        # self.set_spec(resource_dict)

    def set_spec(self, spec_dict):
        self.spec = spec_dict

    @apply_wrapper
    def apply(self):
        subprocess.run(["/bin/bash", "-c", self.spec["run"]])
