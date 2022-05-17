from spacectl.modules import shell, print, resource, export_google_sheets

MODULES = {
    'shell': shell.Task,
    'print': print.Task,
    'resource': resource.Task,
    'export-google-sheets': export_google_sheets.Task
}