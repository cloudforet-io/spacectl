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

DEFAULT_WORKSHEET = 'Sheet1'
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
        sheet = self._get_sheets(google_sheets)
        header_cell = self.spec.get('header_start_at', DEFAULT_HEADER_CELL)
        default_worksheet_name = self.spec.get('worksheet_start_at', DEFAULT_WORKSHEET)
        self.export_data(sheet, header_cell, default_worksheet_name)

    def export_data(self, sheet, header_cell, default_worksheet_name):
        for input_data in self.spec.get('data', {}).get('input_data', []):
            output = self._get_output(input_data)
            verb = self._get_verb(input_data)
            worksheet_name = self._get_worksheet_name(input_data)

            # Creating or rename worksheet
            worksheet_exists = self._chk_worksheet_exists(sheet, worksheet_name)
            default_worksheet_exists = self._chk_worksheet_exists(sheet, default_worksheet_name)
            if worksheet_exists & default_worksheet_exists:
                # Overwrite data into existed worksheet
                pass
            elif default_worksheet_exists:
                # Rename default worksheets and overwrites on them.
                default_worksheet = self._get_worksheet(sheet, default_worksheet_name)
                default_worksheet.update_title(worksheet_name)
            else:
                if not worksheet_exists:
                    sheet.add_worksheet(title=worksheet_name, rows=100, cols=20)

            worksheet = self._get_worksheet(sheet, worksheet_name)
            if verb == 'stat':
                df = pd.DataFrame(output.get('results',[]))
                headers = df.columns.values.tolist()
                self._clear_worksheet(worksheet)
                self._format_header(worksheet, header_cell, headers)
                worksheet.update(header_cell, [headers] + df.values.tolist())
                pass
            else:
                df = pd.DataFrame(output)
                headers = df.columns.values.tolist()
                self._clear_worksheet(worksheet)
                self._format_header(worksheet, header_cell, headers)
                worksheet.update(header_cell, [headers] + df.values.tolist())

    def _init_google_sheets(self):
        echo("Access Google Sheets..", flag=not self.silent)
        service_account = self.spec.get('service_account_json', GOOGLE_SERVICE_ACCOUNT_JSON_DEFAULT_PATH)
        return gspread.service_account(filename=service_account)

    def _get_sheets(self, google_sheets):
        echo(f"Open Sheets : {self.spec.get('sheet_id')}", flag=not self.silent)
        return google_sheets.open_by_key(self.spec.get('sheet_id'))

    @staticmethod
    def _get_worksheet(sheet, worksheet_name):
        return sheet.worksheet(worksheet_name)

    def _get_output(self, raw_task_output):
        value = raw_task_output.get('value', {})
        json_value = self._convert_json(value)
        return json_value.get('output', [])

    def _get_verb(self, raw_task_output):
        value = raw_task_output.get('value', {})
        json_value = self._convert_json(value)
        name = json_value.get('spec', {}).get('verb', {}).get('exec', '')
        mode = f'{name}'
        return mode

    def _get_worksheet_name(self, raw_task_output):
        value = raw_task_output.get('value', {})
        json_value = self._convert_json(value)
        name = json_value.get('name', '')
        worksheet_name = f'{name}'
        return worksheet_name

    @staticmethod
    def _chk_worksheet_exists(sheet, worksheet_name):
        worksheet_exists = False
        worksheet_list = sheet.worksheets()
        worksheet_name_list = []
        for i in worksheet_list:
            worksheet_name_list.append(i.title)
        if worksheet_name in worksheet_name_list:
            worksheet_exists = True
        return worksheet_exists

    @staticmethod
    def _convert_json(data):
        data = data.replace("'", "\"")
        data = data.replace("None", "null")
        data = data.replace("True", "true")
        data = data.replace("False", "false")
        json_data = json.loads(data)

        return json_data

    @staticmethod
    def _clear_worksheet(worksheet):
        header_format = {
            'horizontalAlignment': 'LEFT',
            'backgroundColor': {
                "red": 1.0,
                "green": 1.0,
                "blue": 1.0
            },
            'borders': {
                'top': {'style': 'NONE'},
                'bottom': {'style': 'NONE'},
                'left': {'style': 'NONE'},
                'right': {'style': 'NONE'}
            },
            'textFormat': {'bold': False}
        }
        try:
            header_cells = f'A1:Z100'
            worksheet.format(header_cells, header_format)
            worksheet.clear()
        except Exception as e:
            echo(f'e => {e}')
            pass

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