import sys
from urllib.parse import parse_qsl

import action
from downloadhandler import DownloadHandler
from easynewscleanuphandler import EasynewsCleanupHandler
from easynewsgrouphandler import EasynewsGroupHandler
from easynewsgroupshandler import EasynewsGroupsHandler
from easynewshistoryhandler import EasynewsHistoryHandler
from easynewskeywordhandler import EasynewsKeywordHandler
from easynewssavedsearchhandler import EasynewsSavedSearchHandler
from easynewssearchhandler import EasynewsSearchHandler
from easynewszipmanagerhandler import EasynewsZipManagerHandler
from filehandler import FileHandler
from historyhandler import HistoryHandler
from mainmenuhandler import MainMenuHandler

handlers = {
    MainMenuHandler.name: MainMenuHandler(),
    EasynewsSearchHandler.name: EasynewsSearchHandler(),
    EasynewsKeywordHandler.name: EasynewsKeywordHandler(),
    EasynewsGroupsHandler.name: EasynewsGroupsHandler(),
    EasynewsGroupHandler.name: EasynewsGroupHandler(),
    EasynewsHistoryHandler.name: EasynewsHistoryHandler(),
    EasynewsCleanupHandler.name: EasynewsCleanupHandler(),
    EasynewsZipManagerHandler.name: EasynewsZipManagerHandler(),
    EasynewsSavedSearchHandler.name: EasynewsSavedSearchHandler(),
    DownloadHandler.name: DownloadHandler(),
    FileHandler.name: FileHandler(),
    HistoryHandler.name: HistoryHandler()
}

handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2].replace('?', '')))
action_param = params.get('action')

if action_param is None:
    activity = action.of(MainMenuHandler.name)
else:
    activity = action.decode(action_param)

handlerName = activity.handler
handlers[handlerName].apply(handle, activity)
