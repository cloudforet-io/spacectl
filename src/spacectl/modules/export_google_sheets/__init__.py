import gspread
import json
import re
import string
import pandas as pd
import datetime
import time

from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper
from spacectl.lib.output import echo

DEFAULT_HEADER_CELL = 'A1'


class Task(BaseTask):

    @execute_wrapper
    def execute(self):
        self._validate()

        google_sheets = self._init_google_sheets()
        sheet = self._get_sheets(google_sheets)
        self.clear_all_worksheet(sheet)
        self.export_data(sheet)

    def export_data(self, sheet):
        fill_na = self.spec.get('fill_na')
        for idx, raw_data in enumerate(self.spec.get('data', [])):
            time.sleep(3)
            # task = self._convert_json(raw_data.get('input', {}))
            task = raw_data.get('input', {})
            worksheet_name = self.set_worksheet_name(task)
            echo(f"Export Worksheet: {worksheet_name}")
            worksheet = self.select_worksheet(sheet, idx, worksheet_name)
            # self.write_update_time(worksheet)
            self.export_worksheet(worksheet, task.get('output', []), fill_na)

    def select_worksheet(self, sheet, idx, worksheet_title):
        try:
            if self.spec.get('reset', False) is True and idx == 0:
                worksheet = sheet.get_worksheet(0)
                worksheet.update_title(worksheet_title)
            else:
                worksheet = sheet.worksheet(worksheet_title)
            return worksheet
        except Exception:
            return sheet.add_worksheet(title=worksheet_title, rows=1000, cols=26)

    def export_worksheet(self, worksheet, data, fill_na=None):
        df = pd.DataFrame(data)

        if fill_na is not None:
            df = df.fillna(fill_na)

        headers = df.columns.values.tolist()
        self._format_header(worksheet, DEFAULT_HEADER_CELL, headers)
        export_values = []

        for row in df.values.tolist():
            changed_row = []
            for value in row:
                if isinstance(value, list):
                    changed_row.append('\n'.join(value))
                else:
                    changed_row.append(value)
            export_values.append(changed_row)

        worksheet.update(DEFAULT_HEADER_CELL, [headers] + export_values)

    def write_update_time(self, worksheet):
        worksheet.update('A1', 'Update Time (UTC)')
        worksheet.update('B1', str(datetime.datetime.utcnow()))

    def _init_google_sheets(self):
        echo("Access Google Sheets..", flag=not self.silent)
        service_account = self.spec.get('service_account_json')
        return gspread.service_account(filename=service_account)

    def _get_sheets(self, google_sheets):
        echo(f"Open Sheets : {self.spec.get('sheet_id')}", flag=not self.silent)
        return google_sheets.open_by_key(self.spec.get('sheet_id'))

    def clear_all_worksheet(self, sheet):
        reset = self.spec.get('reset', False)

        if reset:
            echo(f"Clear All Worksheet in selected sheet..", flag=not self.silent)
            sheet.add_worksheet(title='', rows=1000, cols=26)

            for worksheet in sheet.worksheets()[:-1]:
                sheet.del_worksheet(worksheet)

    @staticmethod
    def set_worksheet_name(task):
        return task.get('name', '')

    @staticmethod
    def _convert_json(data):
        data = data.replace("'", "\"")
        data = data.replace("None", "null")
        data = data.replace("True", "true")
        data = data.replace("False", "false")

        return json.loads(data)

    @staticmethod
    def _format_header(worksheet, start_at, headers):
        header_format = {
            'horizontalAlignment': 'CENTER',
            'borders': {
                'top': {'style': 'SOLID'},
                'bottom': {'style': 'SOLID'},
                'left': {'style': 'SOLID'},
                'right': {'style': 'SOLID'}
            },
            "backgroundColor": {
                "red": 12,
                "green": 12,
                "blue": 12
            },
            'textFormat': {'bold': True}
        }

        try:
            header_length = len(headers)
            _header_split = re.split('(\d+)', start_at)
            _col = _header_split[0]
            _col_idx = string.ascii_uppercase.index(_col)
            _chr_index = 64 + _col_idx + header_length if 64 + _col_idx + header_length <= 90 else 90
            _num = _header_split[1]

            header_cells = f'{start_at}:{chr(_chr_index)}{_num}'

            worksheet.format(header_cells, header_format)
        except Exception as e:
            echo(f'e => {e}')
            pass

    def _validate(self):
        if 'service_account_json' not in self.spec:
            raise ValueError(f'Required key: service_account_json\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'data' not in self.spec:
            raise ValueError(f'Required key: data\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')
