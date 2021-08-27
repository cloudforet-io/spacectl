import click
from spacectl.lib.apply import store
from spacectl.lib.parser.apply_jinja import jinja_env
import jinja2.exceptions
from spacectl.lib.output import echo


def apply_template(obj, task_id):
    fields = []
    if isinstance(obj, (str, bool, int, float, bool)):
        return 0
    elif obj is None:
        return 0
    elif isinstance(obj, list):
        # if it's a list, apply template to its items
        for item in obj:
            apply_template(item, task_id)
        return 0

    elif isinstance(obj, dict):
        # if it's a dict, apply template to its items
        fields = list(obj.keys())

    elif hasattr(obj, "fields_to_apply_template"):
        # if it has "fields_to_apply_template" apply only the correspondent fields
        fields = obj.fields_to_apply_template

    else:
        fields = obj.__dict__

    for field in fields:
        value = _get_obj_value(obj, field)

        if isinstance(value, str):
            template = jinja_env.from_string(value)
            try:
                template_applied_value = template.render(
                    var=store.get_var(),
                    env=store.get_env(),
                    tasks=store.get_task_results()
                )
                if field == 'if':
                    obj[field] = _evaluate_if_statement(template_applied_value)
                else:
                    obj[field] = template_applied_value
            except jinja2.exceptions.UndefinedError as e:
                echo(
                    "While applying templates for Task(id={task_id}), an undefined error has occurred\n{error_message}".format(
                        error_message=e.message,
                        task_id=task_id
                    ), err=True, terminate=True)
        else:
            apply_template(value, task_id)


def _get_obj_value(obj, key):
    # obj에서 key값에 해당하는 value를 가져옴.
    if isinstance(obj, dict):
        if key not in obj:
            click.echo("key '{key} doesn't exist in {obj}'".format(key=key, obj=obj), err=True)
            exit(1)
        return obj.get(key)
    else:
        return getattr(obj, key)


def _evaluate_if_statement(statement, **ctx):
    r = bool(eval(statement))
    return r
