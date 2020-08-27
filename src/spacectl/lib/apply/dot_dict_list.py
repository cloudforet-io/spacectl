import click
import copy

class DotDictList(list):
    """
    You can access attributes of each item by '.'
    """
    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError as e:
            try:
                return [task for task in self if task["id"] == attr][0]
            except IndexError:
                click.echo("The task id {attr} doesn't exist.".format(attr=attr), err=True)
                exit(1)

    def to_list(self):
        return list(self)
    # def __getstate__(self):
    #     return [copy.deepcopy(dot_dict) for dot_dict in self]
    # def to_list(self):
    #     return [task.to_dict() for task in self]

