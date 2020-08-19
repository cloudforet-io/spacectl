import yaml, json
from spacectl.command.apply.manifest import Manifest
from spacectl.lib.parser import apply_template

import click
import fnmatch

from google.protobuf.json_format import MessageToDict
from spaceone.core.error import ERROR_BASE
from spaceone.core import pygrpc
from spaceone.core.utils import parse_endpoint, load_json, load_yaml_from_file

from spacectl.lib.output import print_data
from spacectl.conf.global_conf import RESOURCE_ALIAS, EXCLUDE_APIS, DEFAULT_PARSER
from spacectl.conf.my_conf import get_config, get_endpoint, get_template

from spacectl.modules import resource, shell

@click.group()
def cli():
    pass

@cli.command()
@click.option("-f", '--file-path', help = 'manifest yaml file to apply')
def apply(file_path):
    with open(file_path) as f:
        yaml_dict = yaml.safe_load(f)
    mf = Manifest(yaml_dict)

    for task in mf.tasks:
        context = {
            "var": mf.var,
            "env": mf.env,
            "tasks": mf.tasks,
            "self": task,
        }
        # print(context["var"])
        apply_template.apply_template(context, task)
        module = task.uses.split("/", 1)[-1]
        if module == "resource":  #resource인 경우
            resource.apply(task)
        elif module == "shell":
            shell.apply(task)






#
# def apply(file_path):
#     with open(file_path) as f:
#         yaml_dict = yaml.safe_load(f)
#     mf = Manifest(yaml_dict)
#
#     for task in mf.tasks:
#         context = {
#             "var": mf.var,
#             "env": mf.env,
#             "tasks" : mf.tasks,
#             "self": task,
#         }
#         # print(context["var"])
#         apply_template(context, task)
#         print(task.spec)
#     return mf
# m = apply("/Users/mzc01-jsday/fork/spacectl-fork/manifests/example.yaml")
# tasks = m.tasks
# task = tasks[0]
# context ={
#     "var": {
#         "my_domain_name": "homeplus"
#     },
#     "tasks" : m.tasks,
#     "self": task,
# }

# apply_template(context, task)
# 이건 되는데
# print( "result", get_dict_value(context, context, "self.spec.data.name") )
# # 이건 안 됨.
# print( "result", get_dict_value(context, context, "tasks.my_domain.spec.data.name") )
#