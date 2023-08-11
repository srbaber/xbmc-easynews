import action
import constants
import xbmc
import xbmcplugin
from easynewsgroupshandler import EasynewsGroupsHandler
from easynewskeywordhandler import EasynewsKeywordHandler
from easynewssearchhandler import EasynewsSearchHandler
from easynewssizehandler import EasynewsSizeHandler
from easynewszipmanagerhandler import EasynewsZipManagerHandler
from easynewssavedsearchhandler import EasynewsSavedSearchHandler
from filehandler import FileHandler
from historyhandler import HistoryHandler


#
# handler responsible for building the main menu
#
class MainMenuHandler():
    name = 'MainMenuHandler'

    searchByDate = 'Search By Date'
    searchBySize = 'Search By Size'
    searchKeyword = 'Keyword Search'
    searchHistory = 'Search History'
    searchGroup = 'Group Search'
    downloads = 'Downloads'
    zipManager = 'Zip Manager'
    savedSearches = 'Saved Searches'

    def __init__(self):
        pass

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s' % (self.name, addonhandle), 1)

        activity = action.of(EasynewsSearchHandler.name, EasynewsSearchHandler.search_by_date_operation, self.searchByDate)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(EasynewsSizeHandler.name, EasynewsSizeHandler.search_by_size_operation, self.searchBySize)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(EasynewsGroupsHandler.name, EasynewsGroupsHandler.search_groups_operation, self.searchGroup)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(EasynewsKeywordHandler.name, EasynewsKeywordHandler.search_operation, self.searchKeyword)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(HistoryHandler.name, HistoryHandler.show_history_operation, self.searchHistory)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(FileHandler.name, FileHandler.playback, self.downloads)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.list_queues_operation, self.zipManager)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(EasynewsSavedSearchHandler.name, EasynewsSavedSearchHandler.show_saved_searches_operation, self.savedSearches)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        xbmcplugin.endOfDirectory(addonhandle)
