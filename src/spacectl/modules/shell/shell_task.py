import click
import subprocess
from spacectl.apply.task import Task
from spacectl.apply.task import apply_wrapper
from spacectl.lib.output import echo


class ShellTask(Task):
    def __init__(self, manifest, resource_dict, no_progress):
        super().__init__(manifest, resource_dict, no_progress)
        # self.set_spec(resource_dict)

    def set_spec(self, spec_dict):
        self.spec = spec_dict

    @apply_wrapper
    def apply(self):
        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT
        completed_process = subprocess.run(
            ["/bin/bash", "-c",
                self.spec["run"]
                # "abcde"
             ],
            stdout=stdout,
            stderr=stderr,
        )

        self.output = {
            "result": completed_process.stdout.decode("utf-8"),
            "return_code": completed_process.returncode
        }
        echo(self.output["result"], flag=not self.no_progress, err=bool(self.output["return_code"]))
