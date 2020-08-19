# import click
#
# __all__ = ['cli']
#
#
# @click.group()
# def cli():
#
#     pass
#
#
# @cli.command()
# def apply():
#     """
#     Manifest를 만든다.
#     재귀적으로 Manifest는 Resource, ResourceForEach도 만든다.
#     manifest.apply()는 자신의 resource들에 대한 api를 날림.
#     이후 그 resource들은 자신의 api 수행 결과를 data에 merge
#
#     최종적으로 manifest에서 필요한 내용들을 click.echo
#     click.echo도 그냥 manifest나 resource가 알아서 그 때 그 때?
#
#     """
#     pass

import yaml
from manifest import Manifest
from spacectl.lib.dot_dict import get_dotted_value
from spacectl.lib.parser.apply_manifest import get_dict_value

def apply(file_path):
    with open(file_path) as f:
        yaml_dict = yaml.safe_load(f)
    manifest = Manifest(yaml_dict)
    print(manifest)
    return manifest
m = apply("/Users/mzc01-jsday/fork/spacectl-fork/manifests/example.yaml")
tasks = m.tasks
task = tasks[0]
context = {
    "var": {
        "my_domain_name": "homeplus"
    },
    "tasks" : m.tasks,
    "self": task,
}
# 이건 되는데
# print( get_dict_value(context, context, "self.spec.data.name") )
# 이건 안 됨.
print( get_dict_value(context, context, "tasks.my_domain.spec.data.name") )