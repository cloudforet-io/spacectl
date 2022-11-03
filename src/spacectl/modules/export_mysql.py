import pymysql

from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper


class Task(BaseTask):

    def __init__(self, task_info, *args, **kwargs):
        super().__init__(task_info, *args, **kwargs)
        self.conn = None
        self._validate()
        self._create_session()

    @execute_wrapper
    def execute(self):
        data = self.spec.get('data', [])
        for item in data:
            self._insert_data(item)

    def _convert_value(self, value):
        if isinstance(value, str):
            return f'"{value}"'
        else:
            return str(value)

    def _insert_data(self, item):
        keys_str = ", ".join(item.keys())
        values_str = ", ".join(map(self._convert_value, item.values()))
        sql = f'INSERT INTO {self.spec["table"]} ({keys_str}) VALUES ({values_str})'

        self.conn.cursor().execute(sql)
        self.conn.commit()

    def _create_session(self):
        conn_info = {
            'host': self.spec['host'],
            'port': self.spec.get('port', 3306),
            'user': self.spec['user'],
            'password': self.spec['password'],
            'db': self.spec['db'],
            'charset': 'utf8'
        }

        if 'pem' in self.spec:
            conn_info['ssl_ca'] = self.spec['pem']

        self.conn = pymysql.connect(**conn_info)

    def _validate(self):
        if 'host' not in self.spec:
            raise ValueError(f'Required key: host\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'user' not in self.spec:
            raise ValueError(f'Required key: user\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'password' not in self.spec:
            raise ValueError(f'Required key: password\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'db' not in self.spec:
            raise ValueError(f'Required key: db\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'table' not in self.spec:
            raise ValueError(f'Required key: table\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
