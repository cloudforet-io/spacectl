import click
import os
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
        path = self.spec.get('path')

        if path:
            if isinstance(path, list):
                directory = '/'.join(path[:-1])
                file_name = path[-1:][0].replace("/", "")
                path = f'{directory}/{file_name}'
            else:
                directory = path.rsplit('/', 1)[0]

            # Create directory
            os.makedirs(directory, exist_ok=True)

            # Save data to file
            click.echo(f'Save data to file: {path}')
            click.echo('')
            utils.save_json_to_file(self.spec['data'], path, indent=4)
        else:
            print_data(self.spec['data'], output)
            click.echo('')

    def _validate(self):
        if 'data' not in self.spec:
            raise ValueError(f'Required key: data\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
