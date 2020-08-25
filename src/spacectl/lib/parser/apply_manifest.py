import click


# the way to express some statement
OPEN = '${{'
OPEN_LEN = len(OPEN)
CLOSE = '}}'
CLOSE_LEN = len(CLOSE)

def apply_template(original_data, current_data):
    fields = []
    if isinstance(current_data, (str, bool, int, float, bool)):
        return 0
    elif current_data is None:
        return 0
    elif isinstance(current_data, list):
        # if it's a list, apply template to its items
        for item in current_data:
            apply_template(original_data, item)
        return 0

    elif isinstance(current_data, dict):
        # if it's a dict, apply template to its items
        fields = list(current_data.keys())

    elif hasattr(current_data, "fields_to_apply_template"):
        # if it has "fields_to_apply_template" apply only the correspondent fields
        fields = current_data.fields_to_apply_template

    else:
        fields = current_data.__dict__

    for field in fields:
        value = _get_obj_value(current_data, field)
        if type(value) == str:
            text = value.strip()
            open_index = text.find(OPEN)
            while open_index != -1:
                text, open_index = _parse_expression(text, open_index, original_data, field)

                # text, open_index, context, field

                # close_index = text.find(CLOSE, open_index)
                # if close_index == -1:
                #     click.echo(f'WRONG {OPEN} ... {CLOSE} Format', err=True)
                #
                # expression = text[open_index+OPEN_LEN:close_index].strip()
                # evaluated_value = _get_value_by_dot(original_data, original_data, expression)
                # if field == 'apply_if':
                #     if isinstance(evaluated_value, str):
                #         evaluated_value = '"'+evaluated_value+'"'
                #     if isinstance(evaluated_value, int) or isinstance(evaluated_value, float):
                #         evaluated_value = str(evaluated_value)
                #     text = text[:open_index]+evaluated_value+text[close_index+CLOSE_LEN:]
                #     close_index = open_index + len(evaluated_value)
                # else:
                #     text = text[:open_index]+evaluated_value+text[close_index+CLOSE_LEN:]
                #     close_index = open_index + len(evaluated_value) - CLOSE_LEN
                # open_index = text.find(OPEN, close_index+CLOSE_LEN)



            if field == 'apply_if':
                text = _evaluate_if(text, **original_data)
            _update_obj(current_data, field, text)
        else:
            apply_template(original_data, _get_obj_value(current_data, field))

def _apply_template_func(template_func, parsed_expression):
    if template_func == 'bool':
        return bool(parsed_expression)
    else:
        click.echo("No such template function-{func}".format(func=template_func), err=True)
def _parse_expression(text, open_index, context, field):
    # expression e.g. ${{ tasks.my_name.output | isFalse }}
    close_index = text.find(CLOSE, open_index)
    if close_index == -1:
        click.echo(f'WRONG {OPEN} ... {CLOSE} Format', err=True)

    # parsed expression e.g. tasks.my_name.output
    parsed_expression = text[open_index + OPEN_LEN:close_index].strip()
    template_func = None
    if '|' in parsed_expression:
        parsed_expression, template_func = parsed_expression.split("|")
        parsed_expression = parsed_expression.strip()
        template_func = template_func.strip()
    evaluated_value = _get_value_by_dot(context, context, parsed_expression)
    if template_func is not None:
        evaluated_value = _apply_template_func(template_func, evaluated_value)

    if field == 'apply_if':
        if isinstance(evaluated_value, str):
            evaluated_value = '"' + evaluated_value + '"'
        if isinstance(evaluated_value, (int, float, bool)):
            evaluated_value = str(evaluated_value)
        text = text[:open_index] + evaluated_value + text[close_index + CLOSE_LEN:]
        close_index = open_index + len(evaluated_value)
    else:
        text = text[:open_index] + evaluated_value + text[close_index + CLOSE_LEN:]
        close_index = open_index + len(evaluated_value) - CLOSE_LEN
    next_open_index = text.find(OPEN, close_index + CLOSE_LEN)

    return text, next_open_index

def _get_obj_value(obj, key):
    # obj에서 key값에 해당하는 value를 가져옴.
    if isinstance(obj, dict):
        if key not in obj:
            click.echo("key '{key} doesn't exist in {obj}'".format(key=key, obj=obj), err=True)
            exit(1)
        return obj.get(key)
    else:
        return getattr(obj, key)

def _update_obj(obj, key, value):
    # obj를 key, value에 대해 업데이트함..
    if isinstance(obj, dict):
        if key not in obj:
            click.echo("key '{key} doesn't exist in {obj}'".format(key=key, obj=obj), err=True)
            exit(1)
        obj.update({key: value})
    else:
        setattr(obj, key, value)

def _get_value_by_dot(original_data, current_data, dotted_key: str):
    # get value from dot expressions which removed ${{ }}
    if '.' in dotted_key:
        key, rest = dotted_key.split(".", 1)
        value = None
        try:
            value = _get_obj_value(current_data, key)
        except AttributeError:
            value = _get_obj_value(original_data, key)
        return _get_value_by_dot(original_data, value, rest)
    # dotted_key가 마지막 key일 때
    else:
        key = dotted_key
        value = _get_obj_value(current_data, key)
        return value
        # if isinstance(value, (str, int, float, bool)):
        #     return value
        # else:
        #     click.echo("You can use only text or number as a result of ${{ ... }}", err=True)
        #     click.echo("current_data: {current_data}".format(current_data=current_data), err=True)
        #     click.echo("key: {key}".format(key=key), err=True)

def _evaluate_if(statement, **ctx):
    r = bool(eval(statement))
    return r
