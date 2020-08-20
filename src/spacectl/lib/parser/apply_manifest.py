import click


# the way to express some statement
OPEN = '${{'
OPEN_LEN = len(OPEN)
CLOSE = '}}'
CLOSE_LEN = len(CLOSE)

def apply_template(original_data, current_data):
    fields = []
    if isinstance(current_data, str) or \
        isinstance(current_data, bool) or \
        isinstance(current_data, int) or \
        isinstance(current_data, float):
        return 0
    if isinstance(current_data, list):
        # 리스트면 바로 끝
        for item in current_data:
            apply_template(original_data, item)
        return 0

    elif isinstance(current_data, dict):
        fields = list(current_data.keys())

    elif hasattr(current_data, "fields_to_apply_template"):
        fields = current_data.fields_to_apply_template

    elif isinstance(current_data, bool):
        pass

    elif current_data == None:
        pass

    else:
        fields = current_data.__dict__

    for field in fields:
        value = _get_obj_value(current_data, field)
        if type(value) == str:
            text = value.strip()
            open_index = text.find(OPEN)
            while open_index != -1:
                close_index = text.find(CLOSE, open_index)
                if close_index == -1:
                    click.echo(f'WRONG {OPEN} ... {CLOSE} Format', err=True)

                expression = text[open_index+OPEN_LEN:close_index].strip()
                evaluated_value = _get_value_by_dot(original_data, original_data, expression)
                if field == 'apply_if':
                    if isinstance(evaluated_value, str):
                        evaluated_value = '"'+evaluated_value+'"'
                    if isinstance(evaluated_value, int) or isinstance(evaluated_value, float):
                        evaluated_value = str(evaluated_value)
                    text = text[:open_index]+evaluated_value+text[close_index+CLOSE_LEN:]
                    close_index = open_index + len(evaluated_value)
                else:
                    text = text[:open_index]+evaluated_value+text[close_index+CLOSE_LEN:]
                    close_index = open_index + len(evaluated_value) - CLOSE_LEN
                open_index = text.find(OPEN, close_index+CLOSE_LEN)
            if field == 'apply_if':
                text = evaluate_if(text, **original_data)
            _update_obj(current_data, field, text)
        else:
            apply_template(original_data, _get_obj_value(current_data, field))


def _get_obj_value(obj, key):
    # obj에서 key값에 해당하는 value를 가져옴.
    if(isinstance(obj, dict)):
        return obj.get(key)
    else:
        return getattr(obj, key)

def _update_obj(obj, key, value):
    # obj를 key, value에 대해 업데이트함..
    if isinstance(obj, dict):
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

        if type(value) == str or type(value) == int or type(value) == float:
            return value
        else:
            click.echo("You can use only text or number as a result of ${{ ... }}", err=True)

def evaluate_if(statement, **ctx):
    r = eval(statement)
    return r
