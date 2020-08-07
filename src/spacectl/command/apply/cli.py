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

def apply(file_path):
    with open(file_path) as f:
        yaml_dict = yaml.safe_load(f)
    manifest = Manifest(yaml_dict)
    print(manifest)
    return manifest
m = apply("/Users/mzc01-jsday/fork/spacectl-fork/manifests/initailize.yaml")
r = m.resources.my_domain