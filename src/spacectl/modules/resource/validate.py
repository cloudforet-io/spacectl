import click


def check_valid_verb(task_name, mode, custom_verb):
    if mode == 'DEFAULT':
        error_if_invalid_verb(task_name, mode, ['exec'], custom_verb)
    if mode == "READ_ONLY":
        error_if_invalid_verb(task_name, mode, ['create', 'update', 'exec'], custom_verb)
    if mode == "NO_UPDATE":
        error_if_invalid_verb(task_name, mode, ['update', 'exec'], custom_verb)
    if mode == 'EXEC':
        error_if_invalid_verb(task_name, mode, ['read', 'create', 'update'], custom_verb)


def error_if_invalid_verb(task_name, mode, verb_types, custom_verb):
    for verb_type in verb_types:
        if verb_type in custom_verb:
            click.echo("You cannot define {verb_name} as {verb_type} with {mode} in task-{task_name}".format(
                verb_name=custom_verb[verb_type],
                verb_type=verb_type,
                mode=mode,
                task_name=task_name
            ), err=True)
            exit(1)
