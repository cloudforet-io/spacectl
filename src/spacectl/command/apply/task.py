import yaml
import spacectl.lib.parser.apply_template
from spacectl.modules.resource.conf import get_verb
class Task:
    fields_to_apply_template = ["id", "uses", "spec"]
    def __init__(self, manifest, resource_dict):

        self.id = resource_dict["id"]
        self.uses = resource_dict.get("uses", "@modules/resource")
        self.spec = {}

        self._dict = resource_dict
        self.manifest = manifest
        self.set_spec(resource_dict.get("spec"))

    def set_spec(self, spec):
        print("TASK SET SPEC")

class TaskList(list):

    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError as e:
            return [task for task in self if task.id == attr][0]
    # def apply_template(self):
    #     spec = self.spec # spec은 dict
    #     for key, value in spec.items():
    #         if type(value) == str and value.startswith("${{"):



