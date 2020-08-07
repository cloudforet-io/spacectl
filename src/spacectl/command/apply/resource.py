from spacectl.lib.dict_object import DictObject

class Resource:
    resource_type = "identity.Domain" # resource_type? type?
    manifest = "spaceone_apply_manifest" # manifest 의 env나 var, context 등을 이용할 수 있음
    condition = ""  # string or SpaceoneSyntaxCondition(SpaceoneSyntax)
    matches = {
        "and": {},  # or SpaceoneSyntaxMatch
        "or": {}  # or SpaceoneSyntaxMatch
    }
    verbs = ["create", "update", "recreate"]  # allowed verbs
    # count는 SpaceoneApplyResource를 상속받은 SpaceoneApplyReourceCount에서 설정
    ignores = ""  # string meaning fields in data
    data = DictObject({})
    result = True  # apply 수행 결과

    def __init__(self, manifest, config_dict):
        # self.resource_type = dict_obj.resource_type
        self.manifest = manifest
        self.data = DictObject(config_dict["input"], context={"manifest":manifest, "self":self})
        print(type(self.data))
        # for k in data_dict_obj.keys():
        #     self.__setattr__(k, data_dict_obj.__getitem__(k))
