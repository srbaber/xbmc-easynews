import json
import base64

from types import SimpleNamespace
import xbmcgui
import constants

from downloadhandler import DownloadHandler
from filehandler import FileHandler
from easynewscleanuphandler import EasynewsCleanupHandler

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
        item.setInfo('Video', {'Title': self.title})
        return item

    def videoitem(self):
        download = of(DownloadHandler.name, DownloadHandler.download, DownloadHandler.download, self.thumbnail, self.state)
        cm = [(DownloadHandler.download, 'RunPlugin(%s)' % download.url())]

        item = self.playableitem()
        item.addContextMenuItems(cm)
        return item

    def historyitem(self):
        remove = of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.removeHistory, EasynewsCleanupHandler.removeHistory, self.thumbnail, self.state)
        cm = [(EasynewsCleanupHandler.removeHistory, 'RunPlugin(%s)' % remove.url())]

        item = self.playableitem()
        item.addContextMenuItems(cm)
        return item

    def fileitem(self):
        delete = of(FileHandler.name, FileHandler.delete, FileHandler.delete, self.thumbnail, self.state)
        cm = [(FileHandler.delete, 'RunPlugin(%s)' % delete.url())]

        item = self.playableitem()
        item.addContextMenuItems(cm)
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

