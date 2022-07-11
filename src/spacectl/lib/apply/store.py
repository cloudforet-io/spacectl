import os
from spaceone.core import utils

_DATA = {
    'var': {},
    'env': {},
    'tasks': {},
    'results': [],
    'success': 0,
    'skip': 0,
    'failure': 0,
}


def init_env(env: tuple):
    _DATA['env'] = dict(os.environ)
    set_env(_parse_inputs(env))


def init_var(var_file: str, var: tuple):
    if var_file:
        data = utils.load_yaml_from_file(var_file)

        if isinstance(data, dict):
            set_var(data.get('var', {}))

    set_var(_parse_inputs(var))


def get_var(key: str = None, default=None):
    if key:
        return _DATA['var'].get(key, default)
    else:
        return _DATA['var']


def set_var(data: dict):
    _DATA['var'].update(data)


def get_env(key: str = None, default=None):
    if key:
        return _DATA['env'].get(key, default)
    else:
        return _DATA['env']


def set_env(data: dict):
    _DATA['env'].update(data)


def get_task_results():
    return _DATA['tasks']


def get_task_result(task_id: str):
    return _DATA['tasks'].get(task_id)


def append_task_result(task_result: dict):
    task_id = task_result.get('id')
    if task_id:
        if task_id not in _DATA['tasks']:
            _DATA['tasks'][task_id] = []

        _DATA['tasks'][task_id].append(task_result)

    # _DATA['results'].append(task_result)


def set_task_result(task_result: dict):
    task_id = task_result.get('id')
    if task_id:
        _DATA['tasks'][task_id] = task_result

    # _DATA['results'].append(task_result)


def increase_success():
    _DATA['success'] += 1


def increase_failure():
    _DATA['failure'] += 1


def increase_skip():
    _DATA['skip'] += 1


def get_output():
    return {
        'var': _DATA['var'],
        'results': _DATA['results'],
        'success': _DATA['success'],
        'skip': _DATA['skip']
    }


def _parse_inputs(inputs: tuple):
    result = {}
    for data in inputs:
        i_split = data.split('=')
        if len(i_split) == 2:
            result[i_split[0]] = i_split[1]
        else:
            raise ValueError(f'Input parameter({data}) is invalid. (format: key=value)')

    return result
