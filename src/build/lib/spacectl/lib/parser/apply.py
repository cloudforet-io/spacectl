def get_obj_value(obj, key):
    if(isinstance(obj, dict)):
        return obj.get(key)
    else:
        return getattr(obj, key)

def update_obj(obj, key, value):
    if isinstance(obj, dict):
        obj.update({key: value})
    else:
        setattr(obj, key, value)

def get_dict_value(original_data, current_data, dotted_key: str):

    if '.' in dotted_key:
        key, rest = dotted_key.split(".", 1)
        value = None
        try:
            value = get_obj_value(current_data, key)
        except AttributeError:
            value = get_obj_value(original_data, key)


        return get_dict_value(original_data, value, rest)
    # dotted_key가 마지막 key일 때
    else:
        key = dotted_key
        value = get_obj_value(current_data, key)

        if value.startswith("${{"):
            # 또 다시 표현식인 경우는 재귀 # depth를 통해 무한 루프 탈출도 고려
            dotted_key = value.strip()[3:-2].strip()
            key, rest = dotted_key.split(".", 1)
            if key == "tasks": # self에 대한 수정이 필요
                next_self_key, rest = rest.split(".", 1)
                next_current_data = original_data["resources"].next_self_key
                original_data.update({"self":next_current_data})
                return get_dict_value(original_data, next_current_data, ".".join(["self", rest]))
            else:
                return get_dict_value(original_data, get_obj_value(current_data, key), ".".join(["self", rest]))

        else:
            return value

def apply_template(original_data, current_data):
    fields = []
    if type(current_data) == str: return 0
    if isinstance(current_data, list):
        # 리스트면 바로 끝
        for item in current_data:
            apply_template(original_data, item)
        return 0

    elif isinstance(current_data, dict):
        fields = list(current_data.keys())

    elif hasattr(current_data, "fields_to_apply_template"):
        fields = current_data.fields_to_apply_template

    else:
        fields = current_data.__dict__
    for field in fields:
        value = get_obj_value(current_data, field)
        if type(value) == str:
            if value.startswith("${{"):
                trimmed_value = value[3:-2].strip()
                converted_value = get_dict_value(original_data, original_data, trimmed_value)
                update_obj(current_data, field, converted_value)
            else:
                update_obj(current_data, field, value)
        else:
            apply_template(original_data, get_obj_value(current_data, field))
