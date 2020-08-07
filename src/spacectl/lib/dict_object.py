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
            print("$로 시작")
            print(value)
            context = self.context
            return "${{}} 수행해라"
        return value
