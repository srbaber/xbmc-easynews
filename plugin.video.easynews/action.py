import base64
import json
from types import SimpleNamespace

import constants
import xbmcgui


class Action:
    handler = None
    operation = None
    title = None
    thumbnail = None
    state = None

    def __init__(self):
        pass

    def url(self):
        return constants.PLUGIN_URL + 'action=%s' % encode(self)

    def playableitem(self):
        item = self.directoryitem()
        item.setProperty('IsPlayable', 'true')
        item.setLabel(self.title)
        return item

    def directoryitem(self):
        item = xbmcgui.ListItem(self.title)

        if self.thumbnail:
            item.setArt({'thumb': self.thumbnail,
                         'icon': 'DefaultVideo.png',
                         'poster': self.thumbnail})
        return item

    def tostring(self):
        return json.dumps(self, default=lambda x: x.__dict__)


def copy(action):
    return of(action.handler, action.operation, action.title, action.thumbnail, action.state)


def of(handler=None, operation=None, title=None, thumbnail=None, state=None):
    a = Action()
    a.handler = handler
    a.operation = operation
    a.thumbnail = thumbnail
    a.title = title
    if not state:
        a.state = {}
    else:
        a.state = state

    return a


def encode(action):
    data = json.dumps(action, default=lambda x: x.__dict__)
    data = data.encode('utf-8')
    data = base64.urlsafe_b64encode(data).decode('utf-8')
    return data


def decode(data):
    data = base64.urlsafe_b64decode(data.encode('utf-8'))
    dict = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    if (dict == None):
        return None
    else:
        return of(dict.handler, dict.operation, dict.title, dict.thumbnail, dict.state.__dict__)
