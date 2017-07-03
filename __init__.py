
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

    def initialize(self):
        intent = IntentBuilder("TodoistIntent")\
            .require("Add")\
            .require("Task")\
            .require("Project")\
            .build()
        self.register_intent(intent, self.handle_intent)

    def handle_intent(self, message):
        LOGGER.debug('message: {0}'.format(message.serialize()))
        task = message.data.get('Task', None)
        project = message.data.get('Project', None)
        LOGGER.debug('adding task {0} to {1} project'.format(task, project))

        try:
            self.speak_dialog('add.task')
            params = {'client_id': '4585b6dcee2746aa9f2d0fcc26c0a2d1'
                      , 'scope': 'data:read_write'
                      , 'state': 'supersecret'}
            resp = requests.get('https://todoist.com/oauth/authorize', params=params)
            LOGGER.debug('auth resp: {0}'.format(resp.status_code))
            LOGGER.debug('auth resp: {0}'.format(resp.headers))
            LOGGER.debug('auth cookeies: {0}'.format(resp.cookies.keys))
            LOGGER.debug('auth history: {0}'.format(resp.history))
            LOGGER.debug('auth redirect: {0}'.format(resp.history[0].text))


            api = todoist.TodoistAPI('b7ece3720d9114693aa49dd30021f15a7011cb10')
            resp = api.sync()
            prj_id = None
            for prj in api.projects.all():
                LOGGER.debug(prj.data['name'] + ' : ' + str(prj.data['id']))
                if prj['name'].lower() == project:
                    prj_id = prj['id']
                    break

            if prj_id is None:
                # TODO: add project creation method
                LOGGER.debug('project {0} not found, please create it first in Todoist'.format(project))
                self.speak_dialog('project.notfound')
            else:
                LOGGER.debug('prj_id {0}'.format(prj_id))
                item = api.add_item(content=task, project_id=prj_id)
                LOGGER.debug('item: {0}'.format(item))
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
