from spacectl.lib.apply.dot_dict_list import TaskResultList
from spacectl.lib.output import echo
from spacectl.lib.parser.default import parse_key_value
from spaceone.core import utils
import os
import copy

_DATA = {
    "var": {},
    "env": {},
    "tasks": TaskResultList()
}


def apply_input(env, var, var_file):
    data = {}
    if var_file is not None:
        data = utils.load_yaml_from_file(var_file)
    set_var(data.get("var", {}))
    set_var(parse_key_value(var))

    set_env(data.get("env", {}))
    set_env(parse_key_value(env))

def get_var(key=None):
    if key is None:
        return _DATA["var"]
    else:
        return _DATA["var"]["key"]


def set_var(key, value=None):
    if value is None:
        var = key
        for k, v in var.items():
            _DATA["var"][k] = v
    else:
        _DATA["var"][key] = value


def get_env(key=None):
    if key is None:
        return _DATA["env"]
    else:
        return _DATA["env"]["key"]


def set_env(key=None, value=None):
    if key is None:  # initial
        _DATA["env"] = copy.deepcopy(os.environ)
    elif value is None:
        env = key
        for k, v in env.items():
            _DATA["env"][k] = v
    else:
        _DATA["env"][key] = value


def get_task_results():
    return _DATA["tasks"]


def get_task_result(task_id):
    return getattr(_DATA['tasks'], task_id)


def append_task_result(task):
    _DATA["tasks"].append(task.to_dict())


# def update(key, value):
#     _DATA.update({key: value})


def get_output():
    return {
        "var": _DATA["var"],
        "tasks": _DATA["tasks"].to_list()
    }
