from spaceone.core import utils
from spacectl.lib.parser import BaseParser


class DefaultParser(BaseParser):

    def load_template(self, template):
        keys = []
        for rule in template.get('list', []):
            key, name = get_key_and_name(rule, self.use_name_alias)
            key = self._check_index_and_condition(key)
            keys.append(key)
            self._sort_map[name] = key

        self._keys = list(set(keys))

    def parse_data(self, raw_data):
        parsed_data = {}
        for rule in self.template.get('list', []):
            key, name = get_key_and_name(rule, self.use_name_alias)

            if key.startswith('tags.'):
                parsed_data[name] = get_tags_value(raw_data, key)
            else:
                parsed_data[name] = utils.get_dict_value(raw_data, key)

        return parsed_data

    @staticmethod
    def _check_index_and_condition(key):
        index_keys = key.split('.')

        i = 0
        for key in index_keys:
            try:
                if len(key) > 1 and key[0] == "?":
                    break
                else:
                    int(key)
                    break
            except Exception as e:
                pass

            i += 1

        return '.'.join(index_keys[:i])


def get_key_and_name(rule, use_name_alias=True):
    if '|' in rule:
        key, name = rule.split('|')

        if not use_name_alias:
            name = key.rsplit('.', 1)[-1]

    else:
        key = rule
        name = rule

    return key.strip(), name.strip()


def get_tags_value(data, key):
    # Remove prefix key (tags.)
    sub_key = key[5:]

    tags = data.get('tags', {})
    return utils.get_dict_value(tags, sub_key)


if __name__ == '__main__':
    pass
