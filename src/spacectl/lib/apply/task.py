import click
import abc
import os
import traceback
import shutil
from functools import wraps
from spaceone.core import utils
from spacectl.lib.apply import store


def execute_wrapper(func):
    # the instance which calls this func is bounded as self
    @wraps(func)
    def wrapper(self):
        if not self.silent:
            click.echo(f'{"  "*self.depth}TASK [{self.name}] {"*"*1000}'[:self.terminal_width])

        try:
            func(self)
        except Exception as e:
            if not self.silent:
                click.echo(f'(ERROR) =>\n{e}\n'
                           f'>> Spec: {utils.dump_json(self.spec)}',  err=True)
                click.echo('')

            _debug = os.environ.get('SPACECTL_DEBUG', 'false')

            if _debug.lower() == 'true':
                click.echo(traceback.format_exc(), err=True)

            store.increase_failure()
            exit(1)

        if not self.silent:
            if self.debug:
                if self.output_path:
                    output_data = self.output.get(self.output_path)
                else:
                    output_data = utils.dump_json(self.output, 4)

                click.echo(f'(DEBUG) =>\n{output_data}')
                click.echo('')

        store.increase_success()

        if self.is_loop:
            store.append_task_result(self.to_dict())
        else:
            store.set_task_result(self.to_dict())

    return wrapper


class BaseTask(metaclass=abc.ABCMeta):
    fields_to_apply_template = ["name", "uses", "spec", "apply_if"]

    output_path = None

    def __init__(self, task_info, silent=False, depth=0, is_loop=False):
        self.name = task_info['name']
        self.id = task_info.get('id')
        self.debug = task_info.get('debug', False)
        self.silent = silent
        self.depth = depth
        self.is_loop = is_loop
        self.state = 'IN_PROGRESS'
        self.terminal_width = shutil.get_terminal_size(fallback=(120, 50)).columns

        self.spec = {}
        self.output = {}

        self.set_spec(task_info.get('spec', {}))

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'state': self.state,
            'spec': self.spec,
            'output': self.output
        }

    def set_spec(self, spec):
        self.spec = spec

    @abc.abstractmethod
    @execute_wrapper
    def execute(self):
        pass
