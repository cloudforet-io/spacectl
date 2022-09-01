from spacectl.modules import shell, print, resource, export_google_sheets, date, join, concat, export_s3, export_mysql

MODULES = {
    'shell': shell.Task,
    'print': print.Task,
    'resource': resource.Task,
    'export-google-sheets': export_google_sheets.Task,
    'export-s3': export_s3.Task,
    'export-mysql': export_mysql.Task,
    'date': date.Task,
    'join': join.Task,
    'concat': concat.Task
}