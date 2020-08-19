from spacectl.lib.parser import BaseParser


class DefaultParser(BaseParser):

    def load_template(self, template):
        keys = []
        for rule in template.get('list', []):
            key, name = get_key_and_name(rule)
            key = self._check_condition(key)
            keys.append(key)
            self._sort_map[name] = key

        self._keys = list(set(keys))

    def parse_data(self, raw_data):
        parsed_data = {}
        for rule in self.template.get('list', []):
            key, name = get_key_and_name(rule)
            parsed_data[name] = get_dict_value(raw_data, key)

        return parsed_data

    @staticmethod
    def _check_condition(key):
        condition_keys = key.split('$', 1)

        if len(condition_keys) == 2:
            return condition_keys[0]
        else:
            return key


def get_key_and_name(rule):
    if '|' in rule:
        key, name = rule.split('|')
    else:
        key = rule
        name = rule

    return key.strip(), name.strip()


def get_dict_value(data: dict, dotted_key: str):
    if '.' in dotted_key:
        key, rest = dotted_key.split(".", 1)

        if isinstance(data, dict) and key in data:
            if isinstance(data[key], list):
                return get_list_values(data[key], rest)
            else:
                return get_dict_value(data[key], rest)

        else:
            return None
    else:
        if isinstance(data, dict):
            return data.get(dotted_key)
        else:
            return None


def get_list_values(values: list, dotted_key: str):
    list_values = []
    try:
        # Get value by index
        if '.' in dotted_key:
            index, rest = dotted_key.split('.', 1)
            index = int(index)
            if index >= len(values):
                return None
            else:
                list_values.append(values[index])
        else:
            return values[int(dotted_key)]

    except Exception:
        list_values = values
        rest = dotted_key

    # Check condition (cond_key:cond_value=>get_key)
    match_option = 'contain'
    if len(rest) > 1 and rest[0] == "$":
        condition = True
        try:
            cond_option, rest = rest[1:].split('=>', 1)
            cond_key, cond_value = cond_option.split(':')
        except Exception as e:
            # Syntax Error
            return None

        if cond_value[:1] == '=':
            match_option = 'eq'
            cond_value = cond_value[1:]

        elif cond_value[:1] == '!':
            match_option = 'not'
            cond_value = cond_value[1:]

    else:
        condition = False
        cond_key = None
        cond_value = None

    results = []
    for value in list_values:
        # Get value from condition
        if condition and not _check_condition(match_option, value[cond_key], cond_value):
            continue

        # Get value from dict key
        result = get_dict_value(value, rest)

        if result:
            if isinstance(result, list):
                results += result
            else:
                results.append(result)

    try:
        return list(set(results))
    except Exception:
        return results


def _check_condition(match_option: str, val1, val2):
    val1 = str(val1).lower()
    val2 = str(val2).lower()

    if match_option == 'eq':
        if val1 == val2:
            return True

    elif match_option == 'not':
        if val1.find(val2) < 0:
            return True

    else:
        if val1.find(val2) >= 0:
            return True

    return False


if __name__ == '__main__':
    pass
