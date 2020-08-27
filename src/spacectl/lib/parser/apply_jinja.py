import jinja2
from jinja2 import Template, Environment
from spacectl.lib.apply import store

# the way to express some statement
OPEN = '${{'
OPEN_LEN = len(OPEN)
CLOSE = '}}'
CLOSE_LEN = len(CLOSE)


def bool_filter(value):
    return bool(value)


jinja_env = Environment(loader=jinja2.BaseLoader(), variable_start_string=OPEN, variable_end_string=CLOSE)
jinja_env.filters['bool'] = bool_filter