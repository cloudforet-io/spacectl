import click
import copy
from spacectl.lib.output import echo


class DotDictList(list):
    """
    You can access attributes of each item by '.'
    """
    key = "id"

    def dot_access_error_handler(self, attr):
        echo("An attr named {attr} doesn't exist in {self}".format(self=self, attr=attr), err=True, terminate=True)

    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError as e:
            try:
                return [item for item in self if item[self.key] == attr][0]
            except IndexError:
                self.dot_access_error_handler(attr)

    def to_list(self):
        return list(self)
    # def to_list(self):
    #     return [task.to_dict() for task in self]


class TaskResultList(DotDictList):
    def get_task_ids(self):
        return [task["id"] for task in self]

    def dot_access_error_handler(self, task_id):
        echo('You cannot access to a Task(id={task_id}). Accessible Task IDs are {task_ids}'.format(
            task_id=task_id, task_ids=self.get_task_ids()
        ), err=True, terminate=True)