class DictObject(dict):
    def __init__(self, *arg, **kwargs):
        # super(DictObject, self).__init__(*arg, **kwargs)
        super().__init__(*arg, **kwargs)
        self.context = kwargs.get("context", {})

    # def __getitem__(self, key):
    #     value = super()[key]
    #     if type(value) == dict:
    #         return DictObject(value)
    #     else:
    #         return value
    def __setattr__(self, key, value):
        if type(value) == dict:
            if key is "resources":
                super().__setattr__(key, DictObject(
                    value,
                    {
                        "manifest": self.context.manifest,
                        "self": self.context.resources[key]
                    }
                ))
        else:
            super().__setattr__(key, value)

    def __getattr__(self, key):
        value = self.__getitem__(key)
        if type(value) == str and value.startswith("$"):
            expression = value[3:-2].strip()
            print(self.context)
            resources = self.context["manifest"].resources
            _self = self.context["self"]
            # self 자체로는 접근할 수 없어 => _self 라는 변수를 만듦.
            # config상의 self는 dict_object 자기 자신이 아닌, Resource

            if expression.startswith("self"):
                expression="_"+expression
            return eval(expression)
        return value
