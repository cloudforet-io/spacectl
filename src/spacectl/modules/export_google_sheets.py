import gspread
import re
import string
import pandas as pd
import time
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

from spaceone.core import utils
from spacectl.lib.apply.task import BaseTask
from spacectl.lib.apply.task import execute_wrapper
from spacectl.lib.output import echo

DEFAULT_HEADER_CELL = 'A1'
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]
# DEFAULT_QUERY = f"'{ROOT_FOLDER_ID}' in parents and trashed = false"
FILE_QUERY = "mimeType != 'application/vnd.google-apps.folder'"
FOLDER_QUERY = "mimeType = 'application/vnd.google-apps.folder'"


class Task(BaseTask):

    def __init__(self, task_info, *args, **kwargs):
        super().__init__(task_info, *args, **kwargs)
        self._validate()

        service_account_json = self.spec.get('service_account_json')
        creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_json, scopes=SCOPES)
        self.gc = gspread.authorize(creds)
        self.drive_svc = build('drive', 'v3', credentials=creds)
        self.sheet_svc = build('sheets', 'v4', credentials=creds)
        self.root_folder_id = self.spec.get('folder_id')

    @execute_wrapper
    def execute(self):
        path = self.spec.get('path')

        folders, sheet_name = self._get_folder_and_sheet(path)
        folder_id = self._get_folder_id(self.root_folder_id, folders)
        sheet_id = self._get_sheet_id(folder_id, sheet_name)
        sheet = self._get_sheets(sheet_id)

        self.clear_all_worksheet(sheet)
        self.export_data(sheet)
        time.sleep(3)

        copy = self.spec.get('copy')
        if copy:
            self._copy_sheet(copy, sheet_id)

    def _copy_sheet(self, copy_path, sheet_id):
        folders, sheet_name = self._get_folder_and_sheet(copy_path)
        folder_id = self._get_folder_id(self.root_folder_id, folders)
        self._delete_sheet(folder_id, sheet_name)

        echo(f'copy file: {sheet_id} -> {copy_path}')
        body = {
            'name': sheet_name,
            'parents': [folder_id]
        }
        self.drive_svc.files().copy(fileId=sheet_id, body=body, supportsAllDrives=True).execute()

    def _delete_sheet(self, parent_id, name):
        query = f"name = '{name}' and {FILE_QUERY} and '{parent_id}' in parents"
        results = self.drive_svc.files().list(**self._get_search_options(query)).execute()

        items = results.get('files', [])

        body = {'trashed': True}

        for item in items:
            echo(f'delete file: {item["id"]}')
            self.drive_svc.files().update(fileId=item['id'], body=body, supportsAllDrives=True).execute()

    def _get_sheet_id(self, parent_id, name):
        query = f"name = '{name}' and {FILE_QUERY} and '{parent_id}' in parents"
        echo(f'search sheet: {query}')

        results = self.drive_svc.files().list(**self._get_search_options(query)).execute()

        items = results.get('files', [])

        if len(items) > 0:
            return items[0]['id']
        else:
            return self._create_sheet(parent_id, name)

    def _create_sheet(self, parent_id, name):
        sh = self.gc.create(name)
        sheet_id = sh.id
        self._move_file(parent_id, sheet_id)

        return sheet_id

    def _move_file(self, parent_id, file_id):
        file = self.drive_svc.files().get(fileId=file_id, fields='parents').execute()
        previous_parents = ",".join(file.get('parents'))

        echo(f'move sheet: {file_id} ({previous_parents} -> {parent_id})')
        self.drive_svc.files().update(fileId=file_id, addParents=parent_id, removeParents=previous_parents,
                                      supportsAllDrives=True, fields='id, parents').execute()

    def _get_folder_id(self, parent_id, folders):
        if len(folders) == 0:
            return parent_id

        name = folders[0]
        query = f"name = '{name}' and {FOLDER_QUERY} and '{parent_id}' in parents"
        echo(f'search folder: {query}')
        results = self.drive_svc.files().list(**self._get_search_options(query)).execute()

        items = results.get('files', [])

        if len(items) > 0:
            folder_id = items[0]['id']
        else:
            folder_id = self._create_folder(parent_id, name)

        return self._get_folder_id(folder_id, folders[1:])

    def _create_folder(self, parent_id, name):
        echo(f'create folder: {name} in {parent_id}')
        metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent_id]
        }

        f = self.drive_svc.files().create(body=metadata, supportsAllDrives=True, fields='id').execute()
        folder_id = f.get('id')
        return folder_id

    @staticmethod
    def _get_search_options(query):
        return {
            'q': query,
            'includeItemsFromAllDrives': True,
            'supportsAllDrives': True,
            'pageSize': 10,
            'fields': 'nextPageToken, files(id, name)'
        }

    @staticmethod
    def _get_folder_and_sheet(path):
        if isinstance(path, list):
            items = path
        else:
            items = str(path).split('/')
        return items[:-1], items[-1:][0]

    def _get_sheets(self, sheet_id):
        echo(f'open sheet : {sheet_id}')
        return self.gc.open_by_key(sheet_id)

    @staticmethod
    def _set_auto_resize_columns(sheet, worksheet):
        body = {
            "requests": [
                {
                    "autoResizeDimensions": {
                        "dimensions": {
                            "sheetId": worksheet.id,
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": 26
                        }
                    }
                }
            ]
        }

        sheet.batch_update(body)

    def export_data(self, sheet):
        fill_na = self.spec.get('fill_na')
        for idx, raw_data in enumerate(self.spec.get('data', [])):
            if isinstance(raw_data, dict) and 'input' in raw_data:
                task = raw_data.get('input')
                options = raw_data.get('options', {})
            else:
                task = raw_data
                options = {}

            if task is None:
                echo(f'skip input: {raw_data}')
            else:
                output = task.get('output', [])

                worksheet_name = self.set_worksheet_name(task)

                if len(output) > 0:
                    worksheet = self.select_worksheet(sheet, idx, worksheet_name)

                    echo(f"export worksheet: {worksheet_name}")

                    self.export_worksheet(worksheet, output, fill_na, **options)
                    # self._set_auto_resize_columns(sheet, worksheet)
                    time.sleep(5)

                else:
                    echo(f'skip worksheet: {worksheet_name}')

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

    def export_worksheet(self, worksheet, data, fill_na=None, **options):
        df = pd.DataFrame(data)

        if fill_na is not None:
            df = df.fillna(fill_na)

        headers = df.columns.values.tolist()
        self._format_header(worksheet, DEFAULT_HEADER_CELL, headers)
        self._format_values(worksheet, options)
        export_values = []

        for row in list(df.values):
            changed_row = []
            for value in row:
                if isinstance(value, list):
                    changed_row.append('\n'.join(value))
                else:
                    changed_row.append(value)
            export_values.append(changed_row)

        worksheet.update(DEFAULT_HEADER_CELL, [headers] + export_values)

    def clear_all_worksheet(self, sheet):
        reset = self.spec.get('reset', False)

        if reset:
            echo(f'clear all worksheet: {sheet.id}')
            sheet.add_worksheet(title='', rows=1000, cols=26)

            for worksheet in sheet.worksheets()[:-1]:
                sheet.del_worksheet(worksheet)

    @staticmethod
    def set_worksheet_name(task):
        return task.get('name', '')

    @staticmethod
    def _format_values(worksheet, options):
        decimal = options.get('decimal')

        if decimal:
            worksheet.format('2:1000', {'numberFormat': {'type': 'NUMBER', 'pattern': f'0.{ "0"*(decimal-1) }#'}})

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
            raise Exception(f'Header Write Error => {e}')

    def _validate(self):
        if 'service_account_json' not in self.spec:
            raise ValueError(f'Required key: service_account_json\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'data' not in self.spec:
            raise ValueError(f'Required key: data\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'path' not in self.spec:
            raise ValueError(f'Required key: path\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')

        if 'folder_id' not in self.spec:
            raise ValueError(f'Required key: folder_id\n'
                             f'spec: {utils.dump_json(self.spec, 4)}')