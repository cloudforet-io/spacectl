import gspread
import json
import re
import string
import pandas as pd
import datetime

from spacectl.command.execute import _check_api_permissions, _get_service_and_resource, _get_client,_call_api, \
    _parse_parameter
from spacectl.conf.my_conf import get_config, get_endpoint, get_template
from spacectl.lib.apply.task import Task
from spacectl.lib.apply.task import execute_wrapper
from spacectl.modules.resource import validate
from spacectl.lib.output import echo

DEFAULT_HEADER_CELL = 'A4'
GOOGLE_SERVICE_ACCOUNT_JSON_DEFAULT_PATH = '~/.config/gspread/service_account.json'


class ExportGoogleSheetsTask(Task):
    def __init__(self, task_dict, silent):
        super().__init__(task_dict, silent)

    def set_spec(self, spec_dict):
        self.spec = spec_dict

    @execute_wrapper
    def execute(self):
        google_sheets = self._init_google_sheets()
        sheet = self._get_sheets(google_sheets)
        self.clear_all_worksheet(sheet)
        self.export_data(sheet)

    def export_data(self, sheet):
        for _index, raw_data in enumerate(self.spec.get('data', [])):
            task = self._convert_json(raw_data.get('input', {}))
            worksheet_name = self.set_worksheet_name(task, _index)
            echo(f"Export Worksheet: {worksheet_name}", flag=not self.silent)
            worksheet = self.select_worksheet(sheet, _index, worksheet_name)
            self.write_update_time(worksheet)
            self.export_worksheet(worksheet, task.get('output', []))

    def select_worksheet(self, sheet, index, worksheet_title):
        try:
            worksheet = sheet.get_worksheet(index)
            worksheet.update_title(worksheet_title)
            return worksheet
        except Exception:
            return sheet.add_worksheet(title=worksheet_title, rows=1000, cols=26)

    def export_worksheet(self, worksheet, data):
        df = pd.DataFrame(data)
        headers = df.columns.values.tolist()
        self._format_header(worksheet, DEFAULT_HEADER_CELL, headers)
        worksheet.update(DEFAULT_HEADER_CELL, [headers] + df.values.tolist())

    def write_update_time(self, worksheet):
        worksheet.update('A1', 'Update Time (UTC)')
        worksheet.update('B1', str(datetime.datetime.utcnow()))

    def _init_google_sheets(self):
        echo("Access Google Sheets..", flag=not self.silent)
        service_account = self.spec.get('service_account_json', GOOGLE_SERVICE_ACCOUNT_JSON_DEFAULT_PATH)
        return gspread.service_account(filename=service_account)

    def _get_sheets(self, google_sheets):
        echo(f"Open Sheets : {self.spec.get('sheet_id')}", flag=not self.silent)
        return google_sheets.open_by_key(self.spec.get('sheet_id'))

    def clear_all_worksheet(self, sheet):
        echo(f"Clear All Worksheet in selected sheet..", flag=not self.silent)
        sheet.add_worksheet(title='', rows=1000, cols=26)

        for worksheet in sheet.worksheets()[:-1]:
            sheet.del_worksheet(worksheet)

    @staticmethod
    def set_worksheet_name(task, index):
        return f'{index}. {task.get("name", "")}'

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