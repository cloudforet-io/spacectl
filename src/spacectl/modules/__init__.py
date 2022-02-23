from spacectl.modules.resource.resource_task import ResourceTask
from spacectl.modules.shell.shell_task import ShellTask
from spacectl.modules.export_google_sheets.export_google_sheets_task import ExportGoogleSheetsTask

MODULES = {
    'resource': ResourceTask,
    'shell': ShellTask,
    'export-google-sheets': ExportGoogleSheetsTask
}