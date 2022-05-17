import subprocess
from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper


class Task(BaseTask):

    output_path = 'result'

    @execute_wrapper
    def execute(self):
        self._validate()

        stdout = subprocess.PIPE
        stderr = subprocess.STDOUT
        completed_process = subprocess.run(
            [
                "/bin/bash",
                "-c",
                self.spec['run']
            ],
            stdout=stdout,
            stderr=stderr,
        )

        if completed_process.returncode != 0:
            raise Exception(completed_process.stdout.decode('utf-8'))

        self.output = {
            "result": completed_process.stdout.decode('utf-8'),
            "return_code": completed_process.returncode
        }

    def _validate(self):
        if 'run' not in self.spec:
            raise ValueError(f'Required key: run\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
