def get_read_verb(resource_type):
    default_verb = "list"
    configuration = {
        "get": ['identity.DomainOwner']
    }
    for verb, resource_types in configuration.items():
        if resource_type in resource_types:
            return verb
    return default_verb


def get_create_verb(resource_type):
    default_verb = "create"
    configuration = {
        "register": ["repository.Repository", "repository.Plugin"],
        "publish": ["plugin.Supervisor"],

    }
    for verb, resource_types in configuration.items():
        if resource_type in resource_types:
            return verb
    return default_verb


def get_update_verb(resource_type):
    default_verb = "update"
    configuration = {
        # "register": ["repository.Repository", "repository.Plugin"],
        # "publish": ["plugin.Supervisor"],
    }
    for verb, resource_types in configuration.items():
        if resource_type in resource_types:
            return verb
    return default_verb


def get_verb(resource_type):
    return (
        get_read_verb(resource_type),
        get_create_verb(resource_type),
        get_update_verb(resource_type)
    )