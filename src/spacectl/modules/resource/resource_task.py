from spacectl.modules.resource.conf import get_verb
from spacectl.command.apply.task import Task

class ResourceTask(Task):
    def __init__(self, manifest, resource_dict):
        super().__init__(manifest, resource_dict)
        # self.set_spec(resource_dict)

    def set_spec(self, spec):
        self.spec = spec
        if not self.spec.get("matches"):
            self.spec["matches"] = []

        read_verb, create_verb, update_verb = get_verb(self.spec["resource_type"])
        verb = {
            "read": read_verb,
            "create": create_verb,
            "update": update_verb
        }
        for default_verb, custom_verb in spec.get("verb", {}).items():
            verb.update({default_verb: custom_verb})
        self.spec["verb"] = verb

        self.spec["no_verification"] = self.spec.get("no_verification") \
            if self.spec.get("no_verification") else True