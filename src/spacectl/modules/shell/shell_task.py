import click
import subprocess
from spacectl.lib.apply.task import Task
from spacectl.lib.apply.task import execute_wrapper
from spacectl.lib.output import echo
from spacectl.lib.apply import store

class ShellTask(Task):
    def __init__(self, task_dict,silent):
        super().__init__(task_dict, silent)
        # self.set_spec(resource_dict)

    def set_spec(self, spec_dict):
        self.spec = spec_dict

    @execute_wrapper
    def execute(self):
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
        echo(self.output["result"], flag=not self.silent, err=bool(self.output["return_code"]))
