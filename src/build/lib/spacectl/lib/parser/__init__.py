from abc import *


class BaseParser(metaclass=ABCMeta):

    def __init__(self, template):
        self._template = template
        self._keys = []
        self._sort_map = {}
        self.load_template(template)

    @property
    def template(self):
        return self._template

    @property
    def keys(self):
        return self._keys

    @abstractmethod
    def load_template(self, template):
        pass

    @abstractmethod
    def parse_data(self, raw_data):
        pass

    def get_sort_key(self, key):
        return self._sort_map.get(key, key)
