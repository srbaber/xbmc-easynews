import sys
from urllib.parse import parse_qsl

import action
from downloadhandler import DownloadHandler
from easynewscleanuphandler import EasynewsCleanupHandler
from easynewsgrouphandler import EasynewsGroupHandler
from easynewsgroupshandler import EasynewsGroupsHandler
from easynewshistoryhandler import EasynewsHistoryHandler
from easynewskeywordhandler import EasynewsKeywordHandler
from easynewssearchhandler import EasynewsSearchHandler
from easynewssizehandler import EasynewsSizeHandler
from easynewszipmanagerhandler import EasynewsZipManagerHandler
from filehandler import FileHandler
from historyhandler import HistoryHandler
from mainmenuhandler import MainMenuHandler

handlers = {
    MainMenuHandler.name: MainMenuHandler(),
    EasynewsSearchHandler.name: EasynewsSearchHandler(),
    EasynewsSizeHandler.name: EasynewsSizeHandler(),
    EasynewsKeywordHandler.name: EasynewsKeywordHandler(),
    EasynewsGroupsHandler.name: EasynewsGroupsHandler(),
    EasynewsGroupHandler.name: EasynewsGroupHandler(),
    EasynewsHistoryHandler.name: EasynewsHistoryHandler(),
    EasynewsCleanupHandler.name: EasynewsCleanupHandler(),
    EasynewsZipManagerHandler.name: EasynewsZipManagerHandler(),
    DownloadHandler.name: DownloadHandler(),
    FileHandler.name: FileHandler(),
    HistoryHandler.name: HistoryHandler()
}

handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2].replace('?', '')))
actionparam = params.get('action')

if (actionparam == None):
    activity = action.of(MainMenuHandler.name)
else:
    activity = action.decode(actionparam)

handlerName = activity.handler
handlers[handlerName].apply(handle, activity)
