import os
import pandas as pd

from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper


class Task(BaseTask):

    def __init__(self, task_info, *args, **kwargs):
        super().__init__(task_info, *args, **kwargs)
        self._validate()

    @execute_wrapper
    def execute(self):
        path = self.spec['path']
        sheet_name = self.spec['sheet']
        data = self.spec['data']

        directory, file_name, path_str = self._parse_path(path)

        self._create_directory(directory)
        self._export_data(path_str, sheet_name, data)

    @staticmethod
    def _create_directory(directory):
        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def _parse_path(path):
        if isinstance(path, list):
            directory = '/'.join(path[:-1])
            file_name = path[-1:][0].replace('/', '')
            path_str = f'{directory}/{file_name}'
        else:
            path_str = path
            path_arr = path_str.rsplit('/', 1)
            file_name = path_arr[0]
            if len(path_arr) == 1:
                directory = None
            else:
                directory = path_arr[1]

        return directory, file_name, path_str

    def _export_data(self, path_str, sheet_name, data):
        fill_na = self.spec.get('fill_na')
        reset = self.spec.get('reset', False)
        df = pd.DataFrame(data)

        if fill_na is not None:
            df = df.fillna(fill_na)

        sheet_name = sheet_name[:30]

        if reset:
            df.to_excel(path_str, sheet_name=sheet_name, index=False)
        else:
            with pd.ExcelWriter(path_str, mode='a') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def _validate(self):
        if 'path' not in self.spec:
            raise ValueError(f'Required key: path\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'sheet' not in self.spec:
            raise ValueError(f'Required key: sheet\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'data' not in self.spec:
            raise ValueError(f'Required key: data\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
