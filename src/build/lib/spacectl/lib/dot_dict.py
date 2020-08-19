def get_dotted_value(dict_obj, expression, context = None):
    print(dict_obj)
    if type(expression) == str:
        keys = expression.split(".")

    else: keys = expression
    if len(keys) == 0:
        return dict_obj
    else:
        key = keys[0]
        if type(dict_obj) == dict:
            return get_dotted_value(dict_obj.get(key), keys[1:])
        else:
            return get_dotted_value(dict_obj.__getattribute__(key), keys[1:])