import click
from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper
from spacectl.lib.output import print_data


class Task(BaseTask):

    output_path = 'result'

    @execute_wrapper
    def execute(self):
        self._validate()

        output = self.spec.get('output', 'json')
        print_data(self.spec['data'], output)
        click.echo('')

    def _validate(self):
        if 'data' not in self.spec:
            raise ValueError(f'Required key: data\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
