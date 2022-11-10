from typing import Any, List
import os
import click
import jinja2
from pathlib import Path
import shutil

from spaceone.core import utils
from spacectl.lib.apply import store
from spacectl.lib.output import print_data
from spacectl.modules import MODULES


def to_data(value):
    json_value = utils.dump_json(value).strip()
    return f'<DATA>{json_value}</DATA>'


JINJA_ENV = jinja2.Environment(loader=jinja2.BaseLoader(), variable_start_string='${{', variable_end_string='}}')
JINJA_ENV.filters['to_data'] = to_data
TASK_KEYS = [
    'id',
    'name',
    'uses',
    'spec',
    'var',
    'if',
    'loop',
    'sub_tasks',
    'debug'
]


class TaskManager:

    task_queue: list = None

    def __init__(self, silent: bool, output: str = 'none'):
        self.task_queue = []
        self.silent = silent
        self.output = output
        self.terminal_width = shutil.get_terminal_size(fallback=(120, 50)).columns

    def load(self, file_path: str):
        data: dict = utils.load_yaml_from_file(file_path)

        for import_file in data.get('import', []):
            # import file path is relative to current file_path
            absolute_location = Path(file_path).parent
            self.load(os.path.join(absolute_location, import_file))

        store.set_var(data.get('var', {}))
        store.set_env(data.get('env', {}))

        for task in data.get('tasks', []):
            self._check_task(task)
            self.task_queue.append(task)

    def run(self):
        self._run_tasks(self.task_queue)
        self._finish_tasks()

    def _check_task(self, task_info: dict):
        task_json = f'>> Task: {utils.dump_json(task_info, 4)}'

        # When the type of task_info is not a dict
        if not isinstance(task_info, dict):
            raise ValueError(f'Task format is invalid.\n{task_json}')

        # Unsupported keys in task_info
        wrong_keys = list(set(task_info.keys()) - set(TASK_KEYS))
        if len(wrong_keys) > 0:
            raise ValueError(f'Unknown keys: {wrong_keys}\n{task_json}')

        uses = task_info.get('uses')
        sub_tasks = task_info.get('sub_tasks')

        # At least 1 key required (uses or sub_tasks)
        if not (uses or sub_tasks):
            raise ValueError(f'Required keys: uses or sub_tasks\n{task_json}')

        if sub_tasks:
            # When the type of sub_tasks is not a list
            if not isinstance(sub_tasks, list):
                raise ValueError(f'Type error: sub_tasks(list)\n{task_json}')

            # Recursive check of sub_tasks
            for sub_task in sub_tasks:
                self._check_task(sub_task)

    def _run_tasks(self, tasks: List[dict], depth: int = 0):
        for task_info in tasks:

            # Set task name
            task_name = task_info.get('name') or task_info.get('id') or utils.generate_id('task')
            task_info['name'] = task_name

            if 'loop' in task_info:
                loop_cond = self._parse_loop_condition(task_info['loop'], task_name)

                if not self.silent:
                    self._print_stage(task_name, 'LOOP', depth)

                for item in loop_cond:
                    self._execute_task(task_info, task_name, depth+1, item=item)

            else:
                self._execute_task(task_info, task_name, depth)

    def _execute_task(self, task_info: dict, task_name: str, depth: int, item: Any = None):
        self._update_var(task_info, task_name, item)

        task_name: str = self._render_template(task_name, item)
        if_cond: bool = self._parse_if_condition(task_info.get('if', True), task_name, item)
        is_loop: bool = True if item else False

        if if_cond:
            if 'sub_tasks' in task_info:
                if not self.silent:
                    self._print_stage(task_name, 'SUB-TASKS', depth)

                self._run_tasks(task_info['sub_tasks'], depth + 1)
            else:
                task_module = self._get_module_from_uses(task_info['uses'], task_name)
                task_info = self._change_template_values(task_info, task_name, item)

                t = task_module(task_info, silent=self.silent, depth=depth, is_loop=is_loop)
                t.execute()
        else:
            self._print_stage(task_name, 'SKIP', depth)
            store.increase_skip()

    def _update_var(self, task_info: dict, task_name: str, item: Any = None):
        if 'var' in task_info:
            try:
                data = self._render_template(task_info['var'], item)

            except Exception as e:
                raise ValueError(f'[{task_name}] Template Render Error: {e}\n'
                                 f'>> Task: {utils.dump_json(task_info, 4)}')

            store.set_var(data)

    def _get_module_from_uses(self, uses: str, task_name: str):
        try:
            uses = uses.strip()
            location, module = uses.split('/')
        except Exception as e:
            raise ValueError(f'[{task_name}] Module Load Error: uses = {uses}')

        if location == '@modules':
            self._check_default_module(module, task_name)
            return MODULES[module]
        else:
            self._check_remote_module(location, module)
            raise ValueError(f'[{task_name}] Module Load Error: external modules are not currently supported.')

    def _check_remote_module(self, location: str, module: str):
        pass

    @staticmethod
    def _check_default_module(module: str, task_name: str):
        if module not in MODULES:
            raise ValueError(f'[{task_name}] Not found module: uses = {module}')

    def _change_template_values(self, task_info: dict, task_name: str, item=None) -> dict:
        try:
            task_info = self._render_template(task_info, item)

        except Exception as e:
            raise ValueError(f'[{task_name}] Template Render Error: {e}\n'
                             f'>> Task: {utils.dump_json(task_info, 4)}')

        return task_info

    @staticmethod
    def _render_template(value: Any, item: Any = None) -> Any:
        kwargs = {
            'var': store.get_var(),
            'env': store.get_env(),
            'tasks': store.get_task_results()
        }

        if item:
            kwargs['item'] = item

        task_json: str = utils.dump_json(value)
        jinja_template = JINJA_ENV.from_string(task_json)

        template_applied_value: str = jinja_template.render(**kwargs)

        template_applied_value = template_applied_value.replace('"<DATA>', '')
        template_applied_value = template_applied_value.replace('</DATA>"', '')

        return utils.load_json(template_applied_value)

        # task_yaml: str = utils.dump_yaml(value)
        # jinja_template = JINJA_ENV.from_string(task_yaml)
        # template_applied_value: str = jinja_template.render(**kwargs)
        #
        # template_applied_value = template_applied_value.replace('None', 'null')
        # template_applied_value = template_applied_value.replace("\\\'", '"')
        #
        # return utils.load_yaml(template_applied_value)

    def _parse_if_condition(self, if_cond_str: str, task_name: str, item: Any) -> bool:
        try:
            if_cond_str = self._render_template(if_cond_str, item)
            if_cond = eval(str(if_cond_str))

        except Exception as e:
            click.echo(f'[{task_name}] If Condition Error: {if_cond_str}\n(Error) => {e}\n')
            if_cond = False

        if not isinstance(if_cond, bool):
            raise ValueError(f'[{task_name}] If Condition Error: {if_cond_str}\n'
                             f'(Type) => {type(if_cond)}\n'
                             f'(Value) => {if_cond}')

        return if_cond

    def _parse_loop_condition(self, loop_cond_str: str, task_name: str) -> list:
        try:
            loop_cond = self._render_template(loop_cond_str)

        except Exception as e:
            click.echo(f'[{task_name}] Loop Condition Error: {loop_cond_str}\n(Error) => {e}\n')
            loop_cond = []

        if loop_cond and not isinstance(loop_cond, list):
            raise ValueError(f'[{task_name}] Loop Condition Error: {loop_cond_str}\n'
                             f'(Type) => {type(loop_cond)}\n'
                             f'(Value) => {loop_cond}')

        return loop_cond or []

    def _finish_tasks(self):
        task_output = store.get_output()

        if not self.silent:
            click.echo(f'FINISHED [ ok={task_output["success"]}, skipped={task_output["skip"]} ] '
                       f'{"*" * 1000}'[:self.terminal_width])

        if not self.output == 'none':
            print_data(task_output, self.output)

        click.echo('')

    def _print_stage(self, name, action, depth):
        click.echo(f'{"  " * depth}{action} [{name}] {"*" * 1000}'[:self.terminal_width])
