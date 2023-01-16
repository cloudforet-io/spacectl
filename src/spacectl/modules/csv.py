import pandas as pd
from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper


class Task(BaseTask):

    @execute_wrapper
    def execute(self):
        self._validate()
        df = pd.read_csv(self.spec['file'])
        self.output = df.to_dict('records')

    def _validate(self):
        if 'file' not in self.spec:
            raise ValueError(f'Required key: file\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
