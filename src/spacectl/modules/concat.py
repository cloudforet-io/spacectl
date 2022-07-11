from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper
from spacectl.lib.apply.store import get_task_result


class Task(BaseTask):

    @execute_wrapper
    def execute(self):
        self._validate()

        origin_task_result = get_task_result(self.id) or {}
        origin_output = origin_task_result.get('output', [])

        self.output = origin_output + self.spec.get('data', [])

    def _validate(self):
        if 'data' not in self.spec:
            raise ValueError(f'Required key: data\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
