from spacectl.modules import shell, print, resource, export_google_sheets, date, join, concat

MODULES = {
    'shell': shell.Task,
    'print': print.Task,
    'resource': resource.Task,
    'export-google-sheets': export_google_sheets.Task,
    'date': date.Task,
    'join': join.Task,
    'concat': concat.Task
}