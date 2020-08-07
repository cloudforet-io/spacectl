from spacectl.lib.dict_object import DictObject

import yaml
from resource import Resource
class Manifest:
    _dict = {}  # dict로 변환된 yaml
    spaceone = {}
    env = {}
    var = {}
    resources = DictObject({})  # or [SpaceoneApplyResource]

    output = {} # or SpaceoneApplyOutput 은 output.py를 이용할 수 있게..

    def __init__(self, _dict, spaceone={}):

        self._dict = _dict
        self.spaceone=spaceone
        for resource_dict in _dict["resources"]:
            resource_name = list(resource_dict.keys())[0]
            resource = Resource(self, resource_dict[resource_name])
            self.resources[resource_name] = resource




        '''
        vars 오버라이딩, 설정
        envs 오버라이딩, 설정
        spaceone context를 설정
        syntax.read_yaml을 통해 yaml 우리의 로직에 맞게 validate 후 yaml_dict에 넣음
        yaml dict를 통해
        env, vars 설정 및 오버라이딩되기로해서 무시해야할 변수들 무시

        self.yaml_dict["resoruces"] 이용해 Resource 생성
        '''

    def execute_expression(self, expression):
        # self 의 attr을 local var로
        resources = self.resources
        var = self.var
        env = self.env
        spaceone = self.spaceone

        result = eval(expression)
        if str(result).startswith("$"):
            # 만약에 찾아간 value가 또 어떤 resource의 지역 expression이라면 걔의 get value 호출
            return self.execute_expression(result)
        else:
            return result
