import click
import copy
import gspread
import json
import re
import string
import pandas as pd

from spacectl.command.execute import _check_api_permissions, _get_service_and_resource, _get_client,_call_api, _parse_parameter
from spacectl.conf.my_conf import get_config, get_endpoint, get_template
from spacectl.lib.apply.task import Task
from spacectl.lib.apply.task import execute_wrapper
from spacectl.modules.resource import validate
from spacectl.lib.output import echo

DEFAULT_HEADER_CELL = 'A3'
GOOGLE_SERVICE_ACCOUNT_JSON_DEFAULT_PATH = '~/.config/gspread/service_account.json'

class ExportGoogleSheetsTask(Task):
    def __init__(self, task_dict, silent):
        super().__init__(task_dict, silent)

    def set_spec(self, spec_dict):
        self.spec = spec_dict

    @execute_wrapper
    def execute(self):
        google_sheets = self._init_google_sheets()
        worksheet = self._get_worksheet(google_sheets)
        header_cell = self.spec.get('header_start_at', DEFAULT_HEADER_CELL)
        self.export_data(worksheet, header_cell)

    def export_data(self, worksheet, header_cell):
        json_data = self._convert_json(self.spec.get('data', {}).get('input_data', []))
        df = pd.DataFrame(json_data)
        headers = df.columns.values.tolist()
        worksheet.update(header_cell, [headers] + df.values.tolist())
        self._format_header(worksheet, header_cell, headers)

    def _init_google_sheets(self):
        echo("Access Google Sheets..", flag=not self.silent)
        service_account = self.spec.get('service_account_json', GOOGLE_SERVICE_ACCOUNT_JSON_DEFAULT_PATH)
        return gspread.service_account(filename=service_account)

    def _get_sheets(self, google_sheets):
        echo(f"Open Sheets : {self.spec.get('sheet_id')}", flag=not self.silent)
        return google_sheets.open_by_key(self.spec.get('sheet_id'))

    def _get_worksheet(self, google_sheets):
        sheet = self._get_sheets(google_sheets)
        return sheet.get_worksheet(self.spec.get('worksheet_index', 0))

    def _convert_json(self, data):
        data = data.replace("'", "\"")
        data = data.replace("None", "null")
        json_data = json.loads(data)

        return json_data

    def _format_header(self, worksheet, start_at, headers):
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
            pass