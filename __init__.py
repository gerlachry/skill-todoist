
from os.path import dirname

from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
import todoist

__author__ = 'gerlachry'

LOGGER = getLogger(__name__)


class TodoistSkill(MycroftSkill):
    def __init__(self):
        super(TodoistSkill, self).__init__(name="TodoistSkill")
        self.token = self.config.get('token')
        self.api = todoist.TodoistAPI(token=self.token)
        self.api.sync()

    def initialize(self):
        intent = IntentBuilder("TodoistIntent")\
            .require("Add")\
            .require("Task")\
            .require("Project")\
            .build()
        self.register_intent(intent, self.handle_intent)

    def _get_project(self, name):
        """lookup project by name, create if not found"""
        project = None
        for prj in self.api.projects.all():
            if prj['name'].lower() == name:
                project = prj
                break

        if not project:
            self.speak_dialog('add.project')
            LOGGER.debug('creating new project')
            project = self.api.projects.add(name)

        LOGGER.debug('using project {0}'.format(project))
        return project

    def handle_intent(self, message):
        task = message.data.get('Task', None)
        project = message.data.get('Project', None)
        LOGGER.debug('adding task {0} to {1} project'.format(task, project))

        try:
            self.speak_dialog('add.task')
            self.api.sync()
            prj = self._get_project(project)
            item = self.api.items.add(task, prj['id'])
            self.api.commit()

            if 'id' in item.data:
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
