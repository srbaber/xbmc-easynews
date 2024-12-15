import base64
import json
import re
from types import SimpleNamespace

import constants
import xbmcgui


class Action:
    handler = None
    operation = None
    title = None
    thumbnail = None
    state = None
    list_item = None

    def __init__(self):
        pass

    def url(self):
        return constants.PLUGIN_URL + 'action=%s' % encode(self)

    def playable_item(self):
        item = self.directory_item()
        item.setProperty('IsPlayable', 'true')
        item.getVideoInfoTag().setTitle(self.title)
        item.setLabel(self.title)
        return item

    def directory_item(self):
        title = self.title
        path = self.state.get('url', '')

        if self.list_item is None:
            self.list_item = xbmcgui.ListItem(label=title, path=path)

        if self.thumbnail:
            self.list_item.setArt({'thumb': self.thumbnail,
                                   'icon': 'DefaultVideo.png',
                                   'poster': self.thumbnail})

        return self.list_item

    def tostring(self):
        list_item = self.list_item
        self.list_item = None

        if self.state is None:
            orig_url = ''
        else:
            orig_url = self.state.get('url', '')
            scrubbed_url = re.sub('^https://.*:.*@', 'https://USERNAME:PASSWORD@', orig_url)
            self.state['url'] = scrubbed_url


        string_value = json.dumps(self, default=lambda x: x.__dict__)
        self.list_item = list_item

        if orig_url != '':
            self.state['url'] = orig_url

        return string_value


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
    if action is None:
        return ''

    list_item = action.list_item
    action.list_item = None

    data = dumps(action)

    action.list_item = list_item
    return data


def dumps(data):
    data = json.dumps(data, default=lambda x: x.__dict__)
    data = data.encode('utf-8')
    data = base64.urlsafe_b64encode(data).decode('utf-8')
    return data


def decode(data):
    data = loads(data)
    if data is None:
        return None
    else:
        return of(data.handler, data.operation, data.title, data.thumbnail, data.state.__dict__)


def loads(data):
    data = base64.urlsafe_b64decode(data.encode('utf-8'))
    data = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    return data
