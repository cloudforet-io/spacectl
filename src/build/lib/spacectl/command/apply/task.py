import yaml
import spacectl.lib.parser.apply_template

class Task:
    output = {} # or SpaceoneApplyOutput 은 output.py를 이용할 수 있게..

    def __init__(self, manifest, resource_dict):
        self.id = resource_dict["id"]
        self.uses = resource_dict.get("uses", "@modules/resource")
        self.spec = resource_dict.get("spec", "")
        self.matches = resource_dict.get("matches", [])

        self._dict = resource_dict
        self.manifest = manifest


class TaskList(list):
    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError as e:
            return [task for task in self if task.id == attr][0]
