
from os.path import dirname

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import todoist
import requests

__author__ = 'gerlachry'

LOGGER = getLogger(__name__)


class TodoistSkill(MycroftSkill):
    def __init__(self):
        super(TodoistSkill, self).__init__(name="TodoistSkill")
        self.token = self.config.get('token')

    def initialize(self):
        intent = IntentBuilder("TodoistIntent")\
            .require("Add")\
            .require("Task")\
            .require("Project")\
            .build()
        self.register_intent(intent, self.handle_intent)

    def handle_intent(self, message):
        task = message.data.get('Task', None)
        project = message.data.get('Project', None)
        LOGGER.debug('adding task {0} to {1} project'.format(task, project))

        try:
            self.speak_dialog('add.task')
            api = todoist.TodoistAPI(self.token)
            api.sync()
            prj_id = None
            for prj in api.projects.all():
                if prj['name'].lower() == project:
                    prj_id = prj['id']
                    break

            if prj_id is None:
                # TODO: add project creation method
                LOGGER.debug('project {0} not found, please create it first in Todoist'.format(project))
                self.speak_dialog('project.notfound')
            else:
                item = api.add_item(content=task, project_id=prj_id)
                if 'id' in item:
                    self.speak_dialog('add.task.complete')
                else:
                    LOGGER.error('Failed to add task {0} to project {1}'.format(task, project))
                    LOGGER.error(item)
                    self.speak_dialog('add.task.failure')

        except Exception as e:
            LOGGER.exception("Error: {0}".format(e))

    def stop(self):
        pass


def create_skill():
    return TodoistSkill()
