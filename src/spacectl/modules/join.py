import pandas as pd
import numpy as np
from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper
from spacectl.lib.template import *


class Task(BaseTask):

    @execute_wrapper
    def execute(self):
        self._validate()

        join_keys = self.spec.get('join_keys')
        how = self.spec.get('how', 'left')
        columns = self.spec.get('output', {}).get('columns')
        append_origin_columns = self.spec.get('output', {}).get('append_origin_columns', {})
        origin_columns = []
        origin_columns_location = append_origin_columns.get('location')
        origin_columns_start = append_origin_columns.get('start', 0)
        origin_columns_end = append_origin_columns.get('end')

        df = pd.DataFrame(self.spec.get('origin_data', []))

        if origin_columns_location:
            origin_columns = list(df.columns)
            if origin_columns_end:
                origin_columns = origin_columns[origin_columns_start:origin_columns_end]
            else:
                origin_columns = origin_columns[origin_columns_start:]

        if len(df) > 0:
            other_df = pd.DataFrame(self.spec.get('other_data', []))

            if len(other_df) > 0:
                df = df.merge(other_df, on=join_keys, how=how)
                df = df.replace({np.nan: None})

        results = df.to_dict('records')

        if columns:
            if origin_columns_location == 'LEFT':
                columns = origin_columns + columns
            elif origin_columns_location == 'RIGHT':
                columns = columns + origin_columns

            parser = self._load_parser(columns)
            results = [parser.parse_data(res) for res in results]

        self.output = results

    @staticmethod
    def _load_parser(columns):
        template = load_template(None, None, columns)
        return load_parser(None, None, template)

    def _validate(self):
        if 'origin_data' not in self.spec:
            raise ValueError(f'Required key: origin_data\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'other_data' not in self.spec:
            raise ValueError(f'Required key: other_data\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'join_keys' not in self.spec:
            raise ValueError(f'Required key: join_keys\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
