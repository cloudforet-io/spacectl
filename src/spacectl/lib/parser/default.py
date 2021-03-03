from spacectl.lib.parser import BaseParser
from spacectl.lib.output import echo


class DefaultParser(BaseParser):

    def load_template(self, template):
        keys = []
        for rule in template.get('list', []):
            key, name = get_key_and_name(rule)
            key = self._check_index_and_condition(key)
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
    match_option = 'contain'
    if len(dotted_key) > 1 and dotted_key[0] == "?":
        condition = True
        try:
            cond_option, rest = dotted_key[1:].split('=>', 1)
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
        try:
            # Get value by index
            if '.' in dotted_key:
                index, rest = dotted_key.split('.', 1)
                index = int(index)
                if index >= len(values):
                    return None
                else:
                    values = values[index]
            else:
                return values[int(dotted_key)]

        except Exception:
            rest = dotted_key

        condition = False
        cond_key = None
        cond_value = None

    results = []
    for value in values:
        # Get value from condition
        if not isinstance(value, dict) \
                or (condition and not _check_condition(match_option, value[cond_key], cond_value)):
            continue

        # Get value from dict key
        result = get_dict_value(value, rest)

        if result:
            if isinstance(result, list):
                results += result
            else:
                results.append(result)

    try:
        if len(results) > 0:
            return list(set(results))
        else:
            return None
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


def parse_key_value(inputs):
    result = {}
    for data in inputs:
        try:
            key, value = data.split("=", 1)
            if value.find("=") != -1:
                raise ValueError

            result[key] = value
        except ValueError:
            echo(f'[Error] input should be like <key>=<value>, not {data}',
                 err=True, terminate=True)

    return result


def parse_uses(uses):
    uses = uses.strip()
    _, module = uses.split("/")

    return module


if __name__ == '__main__':
    pass
