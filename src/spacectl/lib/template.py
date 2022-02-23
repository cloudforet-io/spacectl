from spaceone.core.utils import parse_endpoint, load_json, load_yaml_from_file

from spacectl.conf.global_conf import DEFAULT_PARSER
from spacectl.conf.my_conf import get_template

def load_template(service, resource, columns, template_path=None):
    if columns:
        template = {
            'template': {
                'list': columns.split(',')
            }
        }
    else:
        if template_path is not None:
            template = load_yaml_from_file(template_path)
        else:
            template = get_template(service, resource)
    return template

def load_parser(service, resource, template):
    parser = template.get('parser', DEFAULT_PARSER)
    template = template.get('template')

    if parser is None:
        raise Exception(f"'parser' is undefined in {service}.{resource} template.")

    if template is None:
        raise Exception(f"'template' is undefined in {service}.{resource} template.")

    try:
        module_name, class_name = parser.rsplit('.', 1)
        parser_module = __import__(module_name, fromlist=[class_name])
    except Exception:
        raise Exception(f'Parser is invalid. ({parser})')

    try:
        return getattr(parser_module, class_name)(template)
    except Exception:
        raise Exception(f'{service}.{resource} template format is invalid.')