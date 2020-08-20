class ResourceForEach(Resource):
    self["index"]
    # iteratable한 기능만 추가하면 될 듯.
    spaceone_apply_resources = ["spaceone_apply_resource"]
    # data, condition을 제외한 멤버변수를 사용
    data = {} #아마 쓸 일 없을 듯 for_each_resources[index].data를 쓸 듯.

