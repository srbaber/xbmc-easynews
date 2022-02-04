from urllib.parse import parse_qsl
import constants
import action

from mainmenuhandler import MainMenuHandler
from easynewssearchhandler import EasynewsSearchHandler
from easynewssizehandler import EasynewsSizeHandler
from easynewskeywordhandler import EasynewsKeywordHandler
from easynewsgroupshandler import EasynewsGroupsHandler
from easynewsgrouphandler import EasynewsGroupHandler
from easynewshistoryhandler import EasynewsHistoryHandler
from downloadhandler import DownloadHandler
from historyhandler import HistoryHandler
from filehandler import FileHandler

handlers = {
    MainMenuHandler.name : MainMenuHandler(),
    EasynewsSearchHandler.name: EasynewsSearchHandler(),
    EasynewsSizeHandler.name: EasynewsSizeHandler(),
    EasynewsKeywordHandler.name: EasynewsKeywordHandler(),
    EasynewsGroupsHandler.name: EasynewsGroupsHandler(),
    EasynewsGroupHandler.name: EasynewsGroupHandler(),
    EasynewsHistoryHandler.name: EasynewsHistoryHandler(),
    DownloadHandler.name: DownloadHandler(),
    FileHandler.name: FileHandler(),
    HistoryHandler.name: HistoryHandler()
}

handle = int(sys.argv[1])
params = dict(parse_qsl(sys.argv[2].replace('?','')))
actionparam = params.get('action')

if (actionparam == None):
    activity = action.of(MainMenuHandler.name)
else:
    activity = action.decode(actionparam)

handlerName = activity.handler
handlers[handlerName].apply(handle, activity)

